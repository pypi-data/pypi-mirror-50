# encoding=utf8
# The data encrypt
import base64

from Crypto.Cipher import AES
from Crypto import Random
import hashlib
from binascii import b2a_hex, a2b_hex
import json


def pad(s, blockSize):
    """
    Pad string
    """
    return s + (blockSize - len(s) % blockSize) * chr(blockSize - len(s) % blockSize)


def unpad(s):
    """
    Unpad string
    """
    return s[: -ord(s[len(s) - 1:])]


class AESCipher(object):
    """The AES cipher
    """

    def __init__(self, key):
        """Create a new AEC cipher
        """
        if not isinstance(key, basestring):
            raise ValueError('AES key must be a string')
        if len(key) != 16 and len(key) != 24 and len(key) != 32:
            raise ValueError('AES key must be either 16, 24, or 32 bytes long, got [%d]' % len(key))
        self.key = key

    def encrypt(self, raw):
        """Encrypt
        Will auto generate random number and convert to base64 encoding
        """
        raw = pad(raw, AES.block_size)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b32encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        """Decrypt
        Will auto decode as base64 string and read random number from it
        """
        enc = base64.b32decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))


def encryptText(skey, text):
    """Encrypt text
    Returns:
        String
    """
    aes = AESCipher(skey)
    return aes.encrypt(text)


def decryptText(skey, text):
    """Decrypt text
    Returns:
        String
    """
    aes = AESCipher(skey)
    return aes.decrypt(text)


def encryptPassword(id, password):
    """Encrypt password
    Parameters:
        id                  The user id
        password            The user password
    Return:
        The encrypted password string
    """
    return hashlib.sha1(password + '@' + id).hexdigest()


def encryptJson(skey, obj):
    cryptor = AES.new(skey, AES.MODE_CBC, b'0000000000000000')
    text = json.dumps(obj)
    length = 16
    count = len(text)
    if count < length:
        add = (length-count)
        text = text + ('\0' * add)
    elif count > length:
        add = (length-(count % length))
        text = text + ('\0' * add)
    ciphertext = cryptor.encrypt(text)
    return b2a_hex(ciphertext)


def decryptJson(skey, text):
    cryptor = AES.new(skey, AES.MODE_CBC, b'0000000000000000')
    text = a2b_hex(text)
    plain_text  = cryptor.decrypt(text)
    return json.loads(plain_text.rstrip('\0'))
