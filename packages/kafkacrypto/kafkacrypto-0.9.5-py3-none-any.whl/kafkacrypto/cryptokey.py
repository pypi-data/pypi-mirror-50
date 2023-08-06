from time import time
import traceback
import pysodium
import msgpack
import logging
from kafkacrypto.chain import process_chain

class CryptoKey(object):
  """Class utilizing file-backed storage to encrypt and decrypt encryption keys
     to/from group members.

  Keyword Arguments:
          file (str,file): Filename or File IO object for storing crypto info.
                           Must be seekable, with read/write permission, and
                           honor sync requests.
  """
  RANDOM_BYTES = 32
  #
  # Per instance, defined in init
  #      __file: File object
  #       __rot: Root of Trust for received messages
  #  __chainrot: Root of Trust for our trust chain
  #    __maxage: Maximum age (seconds)
  # __spk_chain: signing public key chain to root of trust, as array
  #       __spk: signing public key
  #       __ssk: signing private (secret) key
  # Generated ephemerially, on demand:
  #       __epk: dict of encrypting public keys (by topic)
  #       __esk: dict of encrypting private (secret) keys (by topic)
  #
  def __init__(self, file):
    self._logger = logging.getLogger(__name__)
    if (isinstance(file, (str))):
      file = open(file, 'rb+', 0)
    self.__file = file
    self.__file.seek(0,0)
    data = self.__file.read()
    datalen = len(data)
    contents = None
    while len(data) and contents is None:
      try:
        contents = msgpack.unpackb(data)
      except msgpack.exceptions.ExtraData:
        data = data[:-1]
    if len(data) != datalen:
      self._logger.warning("Cryptokey file had extraneous bytes at end, attempting load anyways.")
    self.__maxage = contents[0]
    self.__rot = contents[1]
    self.__chainrot = contents[2]
    self.__esk = {}
    self.__epk = {}
    self.__ssk = contents[3]
    self.__spk = pysodium.crypto_sign_sk_to_pk(self.__ssk)
    self.__spk_chain = []
    self.__crypto_opaque = msgpack.packb([])
    if (len(contents) > 5):
      self.__crypto_opaque = contents[5]
    # update chain last (since it might rewrite file)
    self.__update_spk_chain(contents[4])

  def encrypt_keys(self, keyidxs, keys, topic, msgkey=None, msgval=None):
    if (isinstance(topic,(str))):
      topic = bytes(topic, 'utf-8')
    #
    # msgval should be a msgpacked chain.
    # The public key in the array is the public key to send the key to, using a
    # common DH-derived key between that public key and our private encryption key.
    # Then there is at least one more additional item, random bytes:
    # (3) random bytes
    # There then might be additional public keys:
    # (4) public key
    # ...
    # Which, if present, are multiplied by our secret key and returned along
    # with our public key in the response. This is only safe because:
    #  1. A fresh ephemeral secret key is used for each call of encrypt_keys
    #  2. We validate that the additional public keys are not equal to the
    #     one used to derive the shared secret for this call
    # Together, these ensure that an attacker cannot use the additional public
    # keys feature to learn the common DH shared secret for another session.
    #
    try:
      pk = process_chain(topic,self.__rot,msgval,b'key-encrypt-request')
      # Construct shared secret as sha256(topic || random0 || random1 || our_private*their_public)
      self.__generate_esk(topic)
      random1 = pysodium.randombytes(self.RANDOM_BYTES)
      ss = pysodium.crypto_hash_sha256(topic + pk[3] + random1
           + pysodium.crypto_scalarmult_curve25519(self.__esk[topic],pk[2]))[0:pysodium.crypto_secretbox_KEYBYTES]
      nonce = pysodium.randombytes(pysodium.crypto_secretbox_NONCEBYTES)
      # encrypt keys and key indexes (MAC appended, nonce prepended)
      msg = []
      for i in range(0,len(keyidxs)):
        msg.append(keyidxs[i])
        msg.append(keys[i])
      msg = msgpack.packb(msg)
      msg = nonce + pysodium.crypto_secretbox(msg,nonce,ss)
      # this is then put in a msgpack array with the appropriate max_age, poison, and public key(s)
      poison = msgpack.packb([[b'topics',[topic]],[b'usages',[b'key-encrypt']]])
      pks = [self.__epk[topic]]
      for extrapk in pk[4:]:
        if (extrapk != pk[3]):
          pks.append(pysodium.crypto_scalarmult_curve25519(self.__esk[topic],extrapk))
      msg = msgpack.packb([time()+self.__maxage,poison,pks,[pk[3],random1],msg])
      # and signed with our signing key
      msg = pysodium.crypto_sign(msg, self.__ssk)
      # and finally put as last member of a msgpacked array chaining to ROT
      tchain = self.__spk_chain.copy()
      tchain.append(msg)
      msg = msgpack.packb(tchain)
      # remove ephemeral key
      self.__remove_esk(topic)
    except Exception as e:
      self._logger.warning("".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
      return (None, None)
    return (msgkey, msg)

  def decrypt_keys(self, topic, msgkey=None, msgval=None):
    if (isinstance(topic,(str))):
      topic = bytes(topic, 'utf-8')
    #
    # msgval should be a msgpacked chain.
    # The public key in the array is a set of public key(s) to combine with our
    # encryption key to get the secret to decrypt the key. If we do not
    # have an encryption key for the topic, we cannot do it until we have one.
    # The next item is then the pair of random values for generating the shared
    # secret, followed by the actual key message.
    #
    try:
      if (not topic in self.__esk.keys()):
        raise ValueError
      pk = process_chain(topic,self.__rot,msgval,b'key-encrypt')
      if (len(pk) < 5):
        raise ValueError
      random0 = pk[3][0]
      random1 = pk[3][1]
      nonce = pk[4][0:pysodium.crypto_secretbox_NONCEBYTES]
      msg = pk[4][pysodium.crypto_secretbox_NONCEBYTES:]
      for cpk in pk[2]:
        # Construct candidate shared secrets as sha256(topic || our_private*their_public)
        ss = pysodium.crypto_hash_sha256(topic + random0 + random1
             + pysodium.crypto_scalarmult_curve25519(self.__esk[topic],cpk))[0:pysodium.crypto_secretbox_KEYBYTES]
        # decrypt and return key
        try:
          msg = msgpack.unpackb(pysodium.crypto_secretbox_open(msg,nonce,ss))
          rvs = {}
          for i in range(0,len(msg),2):
            rvs[msg[i]] = msg[i+1]
          if len(rvs) < 1 or 2*len(rvs) != len(msg):
            raise ValueError
        except:
          pass
        else:
          self.__remove_esk(topic)
          return rvs
      raise ValueError
    except Exception as e:
      self._logger.warning("".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
      pass
    return None

  def signed_epk(self, topic, epk=None):
    #
    # returns the public key of the current encryption key for the specified topic
    # (generating a new one if not present), signed by our signing key,
    # with a fresh random value, and with the chain to the ROT prepended.
    #
    try:
      if not (epk is None) and isinstance(epk,(bytes,bytearray)):
        self.__epk[topic] = epk
      if not (topic in self.__epk):
        self.__generate_esk(topic)
      random0 = pysodium.randombytes(self.RANDOM_BYTES)
      # we allow either direct-to-producer or via-controller key establishment
      poison = msgpack.packb([[b'topics',[topic]],[b'usages',[b'key-encrypt-request',b'key-encrypt-subscribe']]])
      msg = msgpack.packb([time()+self.__maxage,poison,self.__epk[topic],random0])
      # and signed with our signing key
      msg = pysodium.crypto_sign(msg, self.__ssk)
      # and finally put as last member of a msgpacked array chaining to ROT
      tchain = self.__spk_chain.copy()
      tchain.append(msg)
      msg = msgpack.packb(tchain)
      return (self.__spk, msg)
    except Exception as e:
      self._logger.warning("".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
      pass
    return (None, None)

  def store_crypto_opaque(self, crypto_opaque):
    self.__crypto_opaque = msgpack.packb([crypto_opaque])
    self.__update_file()

  def load_crypto_opaque(self):
    v = msgpack.unpackb(self.__crypto_opaque)
    if (len(v) > 0):
      return v[0]
    else:
      return None

  def __generate_esk(self, topic):
    # ephemeral keys are use once only, so always ok to overwrite
    self.__esk[topic] = pysodium.randombytes(pysodium.crypto_scalarmult_curve25519_BYTES)
    self.__epk[topic] = pysodium.crypto_scalarmult_curve25519_base(self.__esk[topic])

  def __remove_esk(self, topic):
    self.__esk.pop(topic)
    self.__epk.pop(topic)

  def __update_file(self):
    self.__file.seek(0,0)
    self.__file.write(msgpack.packb([self.__maxage, self.__rot, self.__chainrot, self.__ssk, msgpack.packb(self.__spk_chain), self.__crypto_opaque]))
    self.__file.flush()
    self.__file.truncate()
    self.__file.flush()

  def __update_spk_chain(self, newchain):
    #
    # We have a new candidate chain to replace the current one (if any). We
    # first must check it is a valid chain ending in our signing public key.
    #
    try:
      pk = process_chain(b'',self.__chainrot,newchain,b'')
      if (len(pk) < 3 or pk[2] != self.__spk):
        raise ValueError
      # If we get here, it is a valid chain. So now we need
      # to see if it is "superior" than our current chain.
      # This means a larger minimum max_age.
      min_max_age = 0
      for cpk in self.__spk_chain:
        if (min_max_age == 0 or cpk[0]<min_max_age):
          min_max_age = cpk[0]
      for cpk in newchain:
        if (min_max_age != 0 and cpk[0]<min_max_age):
          raise ValueError
      self.__spk_chain = msgpack.unpackb(newchain)
      self.__update_file()
    except Exception as e:
      self._logger.warning("".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
      pass
