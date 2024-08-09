# Reference: https://gist.github.com/eoli3n/d6d862feb71102588867516f3b34fef1


import json
from Crypto.Cipher import AES
from Crypto import Random
import base64
import hashlib
import binascii


class AESEncryption:
    def __init__(self, password, file_location):
        self.__password, self.__file_loc = password, file_location

    @staticmethod
    def _convert(data, switch: bool = True):

        """
        Function is used to encode or decode byte data to string or string data to byte. Ref: _get_data function
        :param data:
        :param switch:
        :return str:Encoded Or Decoded Data
        """

        if switch:
            return base64.b64encode(data).decode()
        return base64.b64decode(data)

    def _get_data(self, mode=True):
        """
        Function returns file contents as byte or string, depending on the mode
        :param mode:
        :return:
        """

        with open(self.__file_loc, 'rb') as main_file:
            if mode:
                return self._convert(main_file.read())
            return main_file.read()

    def _dump_data(self, data):
        """
        Function writes byte data to file
        :param data:
        :return:
        """

        with open(self.__file_loc, 'wb') as main_file:
            main_file.write(data)

    def _32_B_KEY(self, salt=None, iterations=100000):
        """
        Functions generates and returns a 32-bit key
        :param salt:
        :param iterations:
        :return:
        """

        if salt is None:
            salt = hashlib.sha256(self.__password.encode()).digest()
        key = hashlib.pbkdf2_hmac('sha256', self.__password.encode(), salt, iterations, dklen=32)
        return binascii.hexlify(key).decode()

    def _encrypt(self, data):
        """
        Function to encrypt string data
        :param data:
        :return: Encrypted data in byte format
        """
        passphrase = self._32_B_KEY()
        try:
            key = binascii.unhexlify(passphrase)
            pad = lambda s: s + chr(16 - len(s) % 16) * (16 - len(s) % 16)
            iv = Random.get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            encrypted_64 = base64.b64encode(cipher.encrypt(pad(data).encode())).decode('ascii')
            iv_64 = base64.b64encode(iv).decode('ascii')
            json_data = {
                'iv': iv_64,
                'data': encrypted_64
            }
            clean = base64.b64encode(json.dumps(json_data).encode('ascii'))
        except Exception as e:
            return 404
        return clean

    def _decrypt(self, data):
        """
        Function to decrypt data
        :param data:
        :return: Encrypted data in byte format
        """
        passphrase = self._32_B_KEY()
        try:
            unpad = lambda s: s[:-ord(s[len(s) - 1:])]
            key = binascii.unhexlify(passphrase)
            encrypted = json.loads(base64.b64decode(data).decode('utf-8'))
            encrypted_data = base64.b64decode(encrypted['data'])
            iv = base64.b64decode(encrypted['iv'])
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(encrypted_data)
            clean = unpad(decrypted).decode('utf-8').rstrip()
        except Exception:
            return 404
        return clean

    def PerformTask(self, encryption: bool, dump_data: bool = True) -> bytes | int:
        """
        Main Entry point for encryption and decryption
        :param encryption:
        :param dump_data:
        :return:
        """
        if encryption:
            data = self._get_data()
            e_data = self._encrypt(data)
            if e_data != 404 and dump_data is True:
                self._dump_data(e_data)
                return 200
            elif e_data != 404 and dump_data is False:
                return e_data
            else:
                return 0
        else:
            data = self._get_data(mode=False)
            d_data = self._decrypt(data)
            if d_data != 404:
                d_data = self._convert(d_data, switch=False)
                if dump_data:
                    self._dump_data(d_data)
                    return 200
                else:
                    return d_data
            else:
                return 0


if __name__ == "__main__":
    pass
