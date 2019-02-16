# -*- coding: utf-8 -*-

from __future__ import print_function
from Crypto.Cipher import AES
import hashlib
import keys
import struct
from .pyrijndael.rijndael import Rijndael

BLOCK_SIZE = 16
SHA_DIGEST_LENGTH = 20


def EncryptParameterDataWithAES(input):
    iv = b"\x00" * BLOCK_SIZE
    output = b""
    for num in range(0, 128, 16):
        cipher = AES.new(
            bytes(bytearray.fromhex(keys.wbKey)),
            AES.MODE_CBC,
            iv
        )
        output += cipher.encrypt(input[num:num+16])
    return output


def DecryptParameterDataWithAES(input):
    iv = b"\x00" * BLOCK_SIZE
    output = b""
    for num in range(0, 128, 16):
        cipher = AES.new(
            bytes(bytearray.fromhex(keys.wbKey)),
            AES.MODE_CBC,
            iv
        )

        output += cipher.decrypt(input[num:num+16])
    return output


def apply_samygo_key_transform(input):
    r = Rijndael(bytes(bytearray.fromhex(keys.transKey)))
    return r.encrypt(input)


def generate_server_hello(user_id, pin):
    sha1 = hashlib.sha1()
    sha1.update(pin.encode('utf-8'))
    pin_hash = sha1.digest()
    aes_key = pin_hash[:16]
    print("AES key:", hex(int(aes_key)))

    iv = b"\x00" * BLOCK_SIZE
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)

    encrypted = cipher.encrypt(bytes(bytearray.fromhex(keys.publicKey)))
    print("AES encrypted:", encrypted.hex())

    swapped = EncryptParameterDataWithAES(encrypted)
    print("AES swapped:", hex(int(swapped)))

    data = struct.pack(">I", len(user_id)) + user_id.encode('utf-8') + swapped
    print("data buffer:", '0x' + hex(int(data))[2:].upper())

    sha1 = hashlib.sha1()
    sha1.update(data)
    data_hash = sha1.digest()
    print("hash: " + data_hash.hex())

    server_hello = (
        b"\x01\x02" +
        (b"\x00" * 5) +
        struct.pack(">I", len(user_id) + 132) +
        data +
        (b"\x00" * 5)
    )

    return server_hello, data_hash, aes_key


def parse_client_hello(client_hello, data_hash, aes_key, g_user_id):
    USER_ID_POS = 15
    USER_ID_LEN_POS = 11
    GX_SIZE = 0x80
    data = bytes(bytearray.fromhex(client_hello))

    first_len = struct.unpack(">I", data[7:11])[0]
    user_id_len = struct.unpack(">I", data[11:15])[0]

    # Always equals firstLen????:)
    dest_len = user_id_len + 132 + SHA_DIGEST_LENGTH
    third_len = user_id_len + 132

    print("thirdLen:", str(third_len))
    print("hello:", hex(int(data)))

    start = USER_ID_LEN_POS
    stop = third_len + USER_ID_LEN_POS
    dest = data[start:stop] + data_hash
    print("dest:", hex(int(dest)))

    start = USER_ID_POS
    stop = user_id_len + USER_ID_POS
    user_id = data[start:stop]
    print("userId:", user_id.decode('utf-8'))

    start = stop
    stop += GX_SIZE
    p_enc_wbgx = data[start:stop]
    print("pEncWBGx:", hex(int(p_enc_wbgx)))

    p_enc_gx = DecryptParameterDataWithAES(p_enc_wbgx)
    print("pEncGx:", hex(int(p_enc_gx)))

    iv = b"\x00" * BLOCK_SIZE
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    pgx = cipher.decrypt(p_enc_gx)
    print("pGx:", hex(int(pgx)))

    bn_pgx = int(pgx, 16)
    bn_prime = int(keys.prime, 16)
    bn_private_key = int(keys.privateKey, 16)

    secret_hex = hex(pow(bn_pgx, bn_private_key, bn_prime))[2:].upper()
    secret = bytes(bytearray.fromhex(secret_hex.replace('L', '')))
    print("secret:", hex(int(secret)))

    start = stop
    stop += SHA_DIGEST_LENGTH

    data_hash2 = data[start:stop]
    print("hash2:", hex(int(data_hash2)))

    secret2 = user_id + secret
    print("secret2:", hex(int(secret2)))

    sha1 = hashlib.sha1()
    sha1.update(secret2)
    data_hash3 = sha1.digest()
    print("hash3:", hex(int(data_hash3)))

    if data_hash2 != data_hash3:
        print("Pin error!!!")
        return False

    print("Pin OK :)\n")

    start = stop
    stop += 1
    if ord(data[start:stop]):
        print("First flag error!!!")
        return False

    start = stop
    stop += 4
    if struct.unpack(">I", data[start:stop])[0]:
        print("Second flag error!!!")
        return False

    sha1 = hashlib.sha1()
    sha1.update(dest)
    dest_hash = sha1.digest()
    print("dest_hash:", hex(int(dest_hash)))

    final_buffer = (
        user_id +
        g_user_id.encode('utf-8') +
        pgx +
        bytes(bytearray.fromhex(keys.publicKey)) +
        secret
    )
    sha1 = hashlib.sha1()
    sha1.update(final_buffer)
    sk_prime = sha1.digest()
    print("SKPrime:", hex(int(sk_prime)))

    sha1 = hashlib.sha1()
    sha1.update(sk_prime + b"\x00")
    sk_prime_hash = sha1.digest()
    print("SKPrimeHash:", hex(int(sk_prime_hash)))

    ctx = apply_samygo_key_transform(sk_prime_hash[:16])
    return hex(int(ctx)), sk_prime


def generate_server_acknowledge(sk_prime):
    sha1 = hashlib.sha1()
    sha1.update(sk_prime + b"\x01")
    sk_prime_hash = sha1.digest()

    return (
        "0103000000000000000014" +
        hex(int(sk_prime_hash)).upper() +
        "0000000000"
    )


def parse_client_acknowledge(client_ack, sk_prime):
    sha1 = hashlib.sha1()
    sha1.update(sk_prime + b"\x02")
    sk_prime_hash = sha1.digest()
    tmp_client_ack = (
        "0104000000000000000014" +
        hex(int(sk_prime_hash)).upper() +
        "0000000000"
    )

    return client_ack == tmp_client_ack
