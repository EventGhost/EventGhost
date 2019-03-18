# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.

"""
Common API for all public keys.
"""

import base64
from binascii import hexlify, unhexlify
import os
from hashlib import md5

from Crypto.Cipher import DES3, AES

from paramiko import util
from paramiko.common import o600, zero_byte
from paramiko.py3compat import u, encodebytes, decodebytes, b
from paramiko.ssh_exception import SSHException, PasswordRequiredException


class PKey (object):
    """
    Base class for public keys.
    """

    # known encryption types for private key files:
    _CIPHER_TABLE = {
        'AES-128-CBC': {'cipher': AES, 'keysize': 16, 'blocksize': 16, 'mode': AES.MODE_CBC},
        'DES-EDE3-CBC': {'cipher': DES3, 'keysize': 24, 'blocksize': 8, 'mode': DES3.MODE_CBC},
    }

    def __init__(self, msg=None, data=None):
        """
        Create a new instance of this public key type.  If ``msg`` is given,
        the key's public part(s) will be filled in from the message.  If
        ``data`` is given, the key's public part(s) will be filled in from
        the string.

        :param .Message msg:
            an optional SSH `.Message` containing a public key of this type.
        :param str data: an optional string containing a public key of this type

        :raises SSHException:
            if a key cannot be created from the ``data`` or ``msg`` given, or
            no key was passed in.
        """
        pass

    def asbytes(self):
        """
        Return a string of an SSH `.Message` made up of the public part(s) of
        this key.  This string is suitable for passing to `__init__` to
        re-create the key object later.
        """
        return bytes()

    def __str__(self):
        return self.asbytes()

    # noinspection PyUnresolvedReferences
    def __cmp__(self, other):
        """
        Compare this key to another.  Returns 0 if this key is equivalent to
        the given key, or non-0 if they are different.  Only the public parts
        of the key are compared, so a public key will compare equal to its
        corresponding private key.

        :param .Pkey other: key to compare to.
        """
        hs = hash(self)
        ho = hash(other)
        if hs != ho:
            return cmp(hs, ho)
        return cmp(self.asbytes(), other.asbytes())

    def __eq__(self, other):
        return hash(self) == hash(other)

    def get_name(self):
        """
        Return the name of this private key implementation.

        :return:
            name of this private key type, in SSH terminology, as a `str` (for
            example, ``"ssh-rsa"``).
        """
        return ''

    def get_bits(self):
        """
        Return the number of significant bits in this key.  This is useful
        for judging the relative security of a key.

        :return: bits in the key (as an `int`)
        """
        return 0

    def can_sign(self):
        """
        Return ``True`` if this key has the private part necessary for signing
        data.
        """
        return False

    def get_fingerprint(self):
        """
        Return an MD5 fingerprint of the public part of this key.  Nothing
        secret is revealed.

        :return:
            a 16-byte `string <str>` (binary) of the MD5 fingerprint, in SSH
            format.
        """
        return md5(self.asbytes()).digest()

    def get_base64(self):
        """
        Return a base64 string containing the public part of this key.  Nothing
        secret is revealed.  This format is compatible with that used to store
        public key files or recognized host keys.

        :return: a base64 `string <str>` containing the public part of the key.
        """
        return u(encodebytes(self.asbytes())).replace('\n', '')

    def sign_ssh_data(self, data):
        """
        Sign a blob of data with this private key, and return a `.Message`
        representing an SSH signature message.

        :param str data: the data to sign.
        :return: an SSH signature `message <.Message>`.
        """
        return bytes()

    def verify_ssh_sig(self, data, msg):
        """
        Given a blob of data, and an SSH message representing a signature of
        that data, verify that it was signed with this key.

        :param str data: the data that was signed.
        :param .Message msg: an SSH signature message
        :return:
            ``True`` if the signature verifies correctly; ``False`` otherwise.
        """
        return False

    def from_private_key_file(cls, filename, password=None):
        """
        Create a key object by reading a private key file.  If the private
        key is encrypted and ``password`` is not ``None``, the given password
        will be used to decrypt the key (otherwise `.PasswordRequiredException`
        is thrown).  Through the magic of Python, this factory method will
        exist in all subclasses of PKey (such as `.RSAKey` or `.DSSKey`), but
        is useless on the abstract PKey class.

        :param str filename: name of the file to read
        :param str password: an optional password to use to decrypt the key file,
            if it's encrypted
        :return: a new `.PKey` based on the given private key

        :raises IOError: if there was an error reading the file
        :raises PasswordRequiredException: if the private key file is
            encrypted, and ``password`` is ``None``
        :raises SSHException: if the key file is invalid
        """
        key = cls(filename=filename, password=password)
        return key
    from_private_key_file = classmethod(from_private_key_file)

    def from_private_key(cls, file_obj, password=None):
        """
        Create a key object by reading a private key from a file (or file-like)
        object.  If the private key is encrypted and ``password`` is not ``None``,
        the given password will be used to decrypt the key (otherwise
        `.PasswordRequiredException` is thrown).

        :param file file_obj: the file to read from
        :param str password:
            an optional password to use to decrypt the key, if it's encrypted
        :return: a new `.PKey` based on the given private key

        :raises IOError: if there was an error reading the key
        :raises PasswordRequiredException: if the private key file is encrypted,
            and ``password`` is ``None``
        :raises SSHException: if the key file is invalid
        """
        key = cls(file_obj=file_obj, password=password)
        return key
    from_private_key = classmethod(from_private_key)

    def write_private_key_file(self, filename, password=None):
        """
        Write private key contents into a file.  If the password is not
        ``None``, the key is encrypted before writing.

        :param str filename: name of the file to write
        :param str password:
            an optional password to use to encrypt the key file

        :raises IOError: if there was an error writing the file
        :raises SSHException: if the key is invalid
        """
        raise Exception('Not implemented in PKey')

    def write_private_key(self, file_obj, password=None):
        """
        Write private key contents into a file (or file-like) object.  If the
        password is not ``None``, the key is encrypted before writing.

        :param file file_obj: the file object to write into
        :param str password: an optional password to use to encrypt the key

        :raises IOError: if there was an error writing to the file
        :raises SSHException: if the key is invalid
        """
        raise Exception('Not implemented in PKey')

    def _read_private_key_file(self, tag, filename, password=None):
        """
        Read an SSH2-format private key file, looking for a string of the type
        ``"BEGIN xxx PRIVATE KEY"`` for some ``xxx``, base64-decode the text we
        find, and return it as a string.  If the private key is encrypted and
        ``password`` is not ``None``, the given password will be used to decrypt
        the key (otherwise `.PasswordRequiredException` is thrown).

        :param str tag: ``"RSA"`` or ``"DSA"``, the tag used to mark the data block.
        :param str filename: name of the file to read.
        :param str password:
            an optional password to use to decrypt the key file, if it's
            encrypted.
        :return: data blob (`str`) that makes up the private key.

        :raises IOError: if there was an error reading the file.
        :raises PasswordRequiredException: if the private key file is
            encrypted, and ``password`` is ``None``.
        :raises SSHException: if the key file is invalid.
        """
        with open(filename, 'r') as f:
            data = self._read_private_key(tag, f, password)
        return data

    def _read_private_key(self, tag, f, password=None):
        lines = f.readlines()
        start = 0
        while (start < len(lines)) and (lines[start].strip() != '-----BEGIN ' + tag + ' PRIVATE KEY-----'):
            start += 1
        if start >= len(lines):
            raise SSHException('not a valid ' + tag + ' private key file')
        # parse any headers first
        headers = {}
        start += 1
        while start < len(lines):
            l = lines[start].split(': ')
            if len(l) == 1:
                break
            headers[l[0].lower()] = l[1].strip()
            start += 1
        # find end
        end = start
        while (lines[end].strip() != '-----END ' + tag + ' PRIVATE KEY-----') and (end < len(lines)):
            end += 1
        # if we trudged to the end of the file, just try to cope.
        try:
            data = decodebytes(b(''.join(lines[start:end])))
        except base64.binascii.Error as e:
            raise SSHException('base64 decoding error: ' + str(e))
        if 'proc-type' not in headers:
            # unencryped: done
            return data
        # encrypted keyfile: will need a password
        if headers['proc-type'] != '4,ENCRYPTED':
            raise SSHException('Unknown private key structure "%s"' % headers['proc-type'])
        try:
            encryption_type, saltstr = headers['dek-info'].split(',')
        except:
            raise SSHException("Can't parse DEK-info in private key file")
        if encryption_type not in self._CIPHER_TABLE:
            raise SSHException('Unknown private key cipher "%s"' % encryption_type)
        # if no password was passed in, raise an exception pointing out that we need one
        if password is None:
            raise PasswordRequiredException('Private key file is encrypted')
        cipher = self._CIPHER_TABLE[encryption_type]['cipher']
        keysize = self._CIPHER_TABLE[encryption_type]['keysize']
        mode = self._CIPHER_TABLE[encryption_type]['mode']
        salt = unhexlify(b(saltstr))
        key = util.generate_key_bytes(md5, salt, password, keysize)
        return cipher.new(key, mode, salt).decrypt(data)

    def _write_private_key_file(self, tag, filename, data, password=None):
        """
        Write an SSH2-format private key file in a form that can be read by
        paramiko or openssh.  If no password is given, the key is written in
        a trivially-encoded format (base64) which is completely insecure.  If
        a password is given, DES-EDE3-CBC is used.

        :param str tag: ``"RSA"`` or ``"DSA"``, the tag used to mark the data block.
        :param file filename: name of the file to write.
        :param str data: data blob that makes up the private key.
        :param str password: an optional password to use to encrypt the file.

        :raises IOError: if there was an error writing the file.
        """
        with open(filename, 'w', o600) as f:
            # grrr... the mode doesn't always take hold
            os.chmod(filename, o600)
            self._write_private_key(tag, f, data, password)

    def _write_private_key(self, tag, f, data, password=None):
        f.write('-----BEGIN %s PRIVATE KEY-----\n' % tag)
        if password is not None:
            cipher_name = list(self._CIPHER_TABLE.keys())[0]
            cipher = self._CIPHER_TABLE[cipher_name]['cipher']
            keysize = self._CIPHER_TABLE[cipher_name]['keysize']
            blocksize = self._CIPHER_TABLE[cipher_name]['blocksize']
            mode = self._CIPHER_TABLE[cipher_name]['mode']
            salt = os.urandom(blocksize)
            key = util.generate_key_bytes(md5, salt, password, keysize)
            if len(data) % blocksize != 0:
                n = blocksize - len(data) % blocksize
                #data += os.urandom(n)
                # that would make more sense ^, but it confuses openssh.
                data += zero_byte * n
            data = cipher.new(key, mode, salt).encrypt(data)
            f.write('Proc-Type: 4,ENCRYPTED\n')
            f.write('DEK-Info: %s,%s\n' % (cipher_name, u(hexlify(salt)).upper()))
            f.write('\n')
        s = u(encodebytes(data))
        # re-wrap to 64-char lines
        s = ''.join(s.split('\n'))
        s = '\n'.join([s[i: i + 64] for i in range(0, len(s), 64)])
        f.write(s)
        f.write('\n')
        f.write('-----END %s PRIVATE KEY-----\n' % tag)
