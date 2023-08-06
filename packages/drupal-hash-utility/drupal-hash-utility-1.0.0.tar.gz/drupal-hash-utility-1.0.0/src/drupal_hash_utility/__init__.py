from hashlib import md5
from hashlib import sha512
from random import choice
from string import ascii_letters
from string import digits

__version__ = '1.0.0'


class DrupalHashUtilityInvalidHashException(Exception):
    pass


class DrupalHashUtility:
    _DRUPAL_HASH_LENGTH = 55
    _DRUPAL_HASH_COUNT = 15
    _DRUPAL_SALT_COUNT = 8

    _digests = {
        '$S$': sha512,
        '$H$': md5,
        '$P$': md5
    }

    _i2b64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    def _get_settings(self, encoded):
        settings_bin = encoded[:12]
        count_log2 = self._i2b64.index(settings_bin[3])
        count = 1 << count_log2
        salt = settings_bin[4:12]
        return {
            'count': count,
            'salt': salt
        }

    def _drupal_b64(self, data):
        output = ""
        count = len(data)
        i = 0
        while True:
            value = data[i]
            i += 1
            output += self._i2b64[value & 0x3f]
            if i < count:
                value |= data[i] << 8
            output += self._i2b64[(value >> 6) & 0x3f]
            i += 1
            if i >= count:
                break
            if i < count:
                value |= data[i] << 16
            output += self._i2b64[(value >> 12) & 0x3f]
            i += 1
            if i >= count:
                break
            output += self._i2b64[(value >> 18) & 0x3f]
        return output

    def _apply_hash(self, password, digest, settings):
        password_hash = digest(bytes(settings["salt"], 'utf-8') + bytes(password, 'utf-8')).digest()
        for i in range(settings["count"]):
            password_hash = digest(password_hash + bytes(password, 'utf-8')).digest()
        return self._drupal_b64(password_hash)[:self._DRUPAL_HASH_LENGTH - 12]

    def _salt(self):
        return ''.join([choice(ascii_letters + digits) for _ in range(self._DRUPAL_SALT_COUNT)])

    def encode(self, password):
        """
        Encode a password to a Drupal7 hash.
        :param password: Password string to encode.
        :return: Encoded Drupal7 hash of the given password string.
        """
        salt = self._salt()
        digest = '$S$'
        settings = {
            'count': 1 << self._DRUPAL_HASH_COUNT,
            'salt': salt
        }
        encoded_hash = self._apply_hash(password, self._digests[digest], settings)
        return digest + self._i2b64[self._DRUPAL_HASH_COUNT] + salt + encoded_hash

    def verify(self, password, encoded):
        """
        Verifies a password against a Drupal7 hash.
        :param password: Password string to test against.
        :param encoded: Encoded Drupal7 hash string.
        :return: Boolean True:False
        """
        digest = encoded[:3]

        if digest not in self._digests:
            raise DrupalHashUtilityInvalidHashException()

        digest = self._digests[digest]
        settings = self._get_settings(encoded)

        encoded_hash = encoded[12:]
        password_hash = self._apply_hash(password, digest, settings)

        return password_hash == encoded_hash

    def summary(self, encoded):
        """
        Get a summary of a Drupal7 hash.
        :param encoded: Encoded Drupal7 hash string.
        :return: Dictionary including iterations, salt, and hash.
        """
        encoded = encoded.split("$", 1)[1]
        settings = self._get_settings(encoded)
        return {
            "iterations": f'{settings["count"]}',
            "salt": f'{settings["salt"]}',
            "hash": f'{encoded[12:]}'
        }
