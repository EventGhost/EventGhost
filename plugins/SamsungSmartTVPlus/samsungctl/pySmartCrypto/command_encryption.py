# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
import binascii
import json

# Padding for the input string --not
# related to encryption itself.
BLOCK_SIZE = 16  # Bytes


def pad(s):
    return (
        s +
        (BLOCK_SIZE - len(s) % BLOCK_SIZE) *
        chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
    )


def unpad(s):
    return s[:-ord(s[len(s) - 1:])]


class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key, session_id):
        self.key = binascii.unhexlify(key)
        self.session_id = session_id

    def decrypt(self, enc):
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(binascii.unhexlify(enc)))

    def encrypt(self, raw):
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.encrypt(bytes(pad(raw)).encode('utf8'))

    def generate_command(self, key_press):
        command = dict(
            method='POST',
            body=dict(
                plugin='RemoteControl',
                param1='uuid:12345',
                param2='Click',
                param3=key_press,
                param4=False,
                api='SendRemoteKey',
                version='1.000'
            )
        )

        command_array = ','.join(
            map(str, self.encrypt(json.dumps(command)))
        )

        res = {
            '5::/com.samsung.companion': dict(
                name='callCommon',
                args=[
                    dict(
                        Session_Id=str(self.session_id),
                        body=[command_array]
                    )
                ]
            )
        }

        return json.dumps(res)
