# -*- coding: utf-8 -*-
#
# Copyright (C) 2014-2015  Pako <lubos.ruckl@gmail.com>
#
# This file is part of the PushBullet plugin for EventGhost.
#

from os.path import isfile, join
from binascii import b2a_hex
from base64 import b64decode, b64encode
from hashlib import sha256
from struct import pack, unpack
from Crypto.Cipher import AES
from Crypto.Util import strxor
from Crypto.Hash import HMAC, SHA as SHA1
from os import urandom
from textwrap import fill
from PIL import Image
import wx
from math import sqrt
from cStringIO import StringIO
import eg
import requests

SEP = "   <#>   "


def get_key_fingerprint(key):
    if key is not None:
        fp_hash = sha256()
        fp_hash.update(key)
        return b64encode(fp_hash.digest())


def check(num):
    num = num.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
    if num[0] == "+":
        front = "+"
        num = num[1:]
    else:
        front = ""
    tmp = [c for c in num if "0" <= c <= "9"]
    if len(tmp) != len(num):
        return
    return front + num


def get_nm_nr(recip):
    return ("", recip.strip()) if SEP not in recip else \
        (recip.split(SEP)[0].strip(), recip.split(SEP)[1].strip())


def wrap(txt, width):
    txt = txt.rstrip()
    lst = txt.splitlines()
    for i, item in enumerate(lst):
        lst[i] = fill(item, width)
    txt = "\n".join(lst)
    return txt


def pil_to_bitmap(pil):
    img = wx.Image(pil.size[0], pil.size[1])
    img.SetData(pil.convert("RGB").tobytes())
    if (
        pil.mode in ('RGBA', 'LA') or
        (pil.mode == 'P' and 'transparency' in pil.info)
    ):
        img.SetAlphaData(pil.convert("RGBA").tobytes()[3::4])
    return img.ConvertToBitmap()


def image_to_pil(img):
    w, h = img.GetWidth(), img.GetHeight()
    data = img.get_data()
    pil = Image.new('RGB', (w, h))
    pil.frombytes(data)
    if img.HasAlpha():
        a_pil = Image.new("L", (w, h))
        a_pil.frombytes(img.GetAlphaData())
        pil = Image.merge('RGBA', pil.split() + (a_pil,))
    return pil


def resize(pil, new_size):
    w, h = pil.size
    if w > new_size or h > new_size:
        factor = max(w, h) / float(new_size)
        m = int(min(w, h) / factor)
        w, h = (new_size, m) if w >= h else (m, new_size)
        pil = pil.resize((w, h), Image.ANTIALIAS)
    image = Image.new('RGBA', (new_size, new_size))
    image.paste(pil, ((new_size - w) / 2, (new_size - h) / 2))
    return image


def grayed(bmp):
    img = bmp.ConvertToImage()
    pil_img = Image.new('RGB', (img.GetWidth(), img.GetHeight()))
    pil_img.frombytes(str(img.GetData()))
    pil_img = pil_img.convert("L")
    m = pil_img.load()
    s = pil_img.size
    for x in xrange(s[0]):
        for y in xrange(s[1]):
            g = m[x, y]
            if g > 0xf0:
                g = 0xf0
            elif g < 0xc0:
                g = 0xc0
            m[x, y] = g
    return pil_to_bitmap(pil_img)


def grdnt(r, d):
    w = 0.20
    if d / r < 1 - w:
        return 255
    elif d > r:
        return 0
    return int(0.5 + 255 * (r - d) / (r * w))


def fluffy_circle_mask(sz):
    r = sz / 2
    data = []
    for x in range(sz):
        tmp = sz * [chr(0)]
        for y in range(sz):
            dist = sqrt((x - r) ** 2 + (y - r) ** 2)
            alph = grdnt(r, dist)
            tmp[y] = chr(alph)
        row = "".join(tmp)
        data.append(row)
    strng = "".join(data)
    return strng


def get_icon(err, icon=None):
    icon = icon if icon else join(eg.Icons.IMAGES_PATH, "logo.png")
    if isfile(icon):
        try:
            pil = Image.open(icon)
        except IOError:
            eg.PrintError(err % icon)
            pil = Image.open(join(eg.Icons.IMAGES_PATH, "logo.png"))
    else:
        try:
            pil = Image.open(StringIO(b64decode(icon)))
        except IOError:
            eg.PrintError(err % icon[:128])
            pil = Image.open(join(eg.Icons.IMAGES_PATH, "logo.png"))
    w, h = pil.size
    if w > 96 or h > 96:
        factor = max(w, h) / 96.0
        x = int(min(w, h) / factor)
        size = (96, x) if w >= h else (x, 96)
        pil = pil.resize(size, Image.ANTIALIAS)
        image = Image.new('RGBA', (96, 96))
        image.paste(pil, ((96 - size[0]) / 2, (96 - size[1]) / 2))
        pil = image
    io_file = StringIO()
    pil.save(io_file, format = 'PNG')
    #pil.save(io_file, format='JPEG')
    io_file.seek(0)
    data = io_file.read()
    return b64encode(data)


# -------------------------------------------------------------------------------
# obtained from gcm.py --- start
def inc32(block):
    counter, = unpack('>L', block[12:])
    counter += 1
    return block[:12] + pack('>L', counter)


def gcm_rightshift(vec):
    for x in range(15, 0, -1):
        c = vec[x] >> 1
        c |= (vec[x - 1] << 7) & 0x80
        vec[x] = c
    vec[0] >>= 1
    return vec


def gcm_gf_mult(val_a, val_b):
    mask = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]
    poly = [0x00, 0xe1]
    z = [0] * 16
    v = [c for c in val_a]
    for x in range(128):
        if val_b[x >> 3] & mask[x & 7]:
            z = [v[y] ^ z[y] for y in range(16)]
        bit = v[15] & 1
        v = gcm_rightshift(v)
        v[0] ^= poly[bit]
    return z


def ghash(h, data):
    u = (16 - len(data)) % 16
    x = data + chr(0) * u
    x += pack('>QQ', 0, len(data) * 8)
    y = [0] * 16
    vec_h = [ord(c) for c in h]
    for i in range(0, len(x), 16):
        block = [ord(c) for c in x[i:i + 16]]
        y = [y[j] ^ block[j] for j in range(16)]
        y = gcm_gf_mult(y, vec_h)
    return ''.join(chr(c) for c in y)


def gctr(k, icb, plaintext):
    y = ''
    if len(plaintext) == 0:
        return y
    aes = AES.new(k, AES.MODE_EAX)
    cb = icb
    for i in range(0, len(plaintext), aes.block_size):
        cb = inc32(cb)
        encrypted = aes.encrypt(cb)
        plaintext_block = plaintext[i:i + aes.block_size]
        y += strxor.strxor(plaintext_block, encrypted[:len(plaintext_block)])
    return y


def gcm_decrypt(k, msg):
    bmsg = b64decode(msg)
    version = bmsg[0]
    # tag = bmsg[1:17]  # 128 bits
    iv = bmsg[17:29]  # 96 bits
    encrypted = bmsg[29:]
    if version != "1":
        return
    # aes = AES.new(k, AES.MODE_EAX)
    y0 = iv + "\x00\x00\x00\x01"
    decrypted = gctr(k, y0, encrypted)
    return decrypted


def gcm_encrypt(k, plaintext):
    aes = AES.new(k, AES.MODE_EAX)
    h = aes.encrypt(chr(0) * aes.block_size)
    iv = urandom(12)
    y0 = iv + "\x00\x00\x00\x01"
    encrypted = gctr(k, y0, plaintext)
    s = ghash(h, encrypted)
    t = aes.encrypt(y0)
    tag = strxor.strxor(s, t)
    res = "1" + tag + iv + encrypted
    return b64encode(res)

# obtained from gcm.py --- end

# -------------------------------------------------------------------------------

# part of pbkdf2.py --- start


_0xffffffffL = long(1) << 32


def isunicode(s):
    return isinstance(s, unicode)


def isbytes(s):
    return isinstance(s, str)


def isinteger(n):
    return isinstance(n, (int, long))


def b(s):
    return s


def binxor(val_a, val_b):
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(val_a, val_b)])


class PBKDF2(object):
    """PBKDF2.py : PKCS#5 v2.0 Password-Based Key Derivation

    This implementation takes a passphrase and a salt (and optionally an
    iteration count, a digest module, and a MAC module) and provides a
    file-like object from which an arbitrarily-sized key can be read.

    If the passphrase and/or salt are unicode objects, they are encoded as
    UTF-8 before they are processed.

    The idea behind PBKDF2 is to derive a cryptographic key from a
    passphrase and a salt.

    PBKDF2 may also be used as a strong salted password hash.  The
    'crypt' function is provided for that purpose.

    Remember: Keys generated using PBKDF2 are only as strong as the
    passphrases they are derived from.
    """

    def __init__(self, passphrase, salt, iterations=1000, digestmodule=SHA1, macmodule=HMAC):
        self.__buf = None
        self.__blockNum = None
        self.closed = False
        self.__macmodule = macmodule
        self.__digestmodule = digestmodule
        self._setup(passphrase, salt, iterations, self._pseudorandom)

    def _pseudorandom(self, key, msg):
        """Pseudorandom function.  e.g. HMAC-SHA1"""
        # noinspection PyTypeChecker
        return self.__macmodule.new(
            key=key,
            msg=msg,
            digestmod=self.__digestmodule
        ).digest()

    def read(self, bytes_cnt):
        """Read the specified number of key bytes."""
        if self.closed:
            raise ValueError("file-like object is closed")

        size = len(self.__buf)
        blocks = [self.__buf]
        i = self.__blockNum
        while size < bytes_cnt:
            i += 1
            if i > _0xffffffffL or i < 1:
                # We could return "" here, but
                raise OverflowError("derived key too long")
            block = self.__f(i)
            blocks.append(block)
            size += len(block)
        buf = b("").join(blocks)
        retval = buf[:bytes_cnt]
        self.__buf = buf[bytes_cnt:]
        self.__blockNum = i
        return retval

    def __f(self, i):
        # i must fit within 32 bits
        assert 1 <= i <= _0xffffffffL
        u = self.__prf(self.__passphrase, self.__salt + pack("!L", i))
        result = u
        for j in xrange(2, 1 + self.__iterations):
            u = self.__prf(self.__passphrase, u)
            result = binxor(result, u)
        return result

    def hexread(self, octets):
        """Read the specified number of octets. Return them as hexadecimal.

        Note that len(obj.hexread(n)) == 2*n.
        """
        return b2a_hex(self.read(octets))

    def _setup(self, passphrase, salt, iterations, prf):
        # Sanity checks:
        # passphrase and salt must be str or unicode (in the latter
        # case, we convert to UTF-8)
        if isunicode(passphrase):
            passphrase = passphrase.encode("UTF-8")
        elif not isbytes(passphrase):
            raise TypeError("passphrase must be str or unicode")
        if isunicode(salt):
            salt = salt.encode("UTF-8")
        elif not isbytes(salt):
            raise TypeError("salt must be str or unicode")

        # iterations must be an integer >= 1
        if not isinteger(iterations):
            raise TypeError("iterations must be an integer")
        if iterations < 1:
            raise ValueError("iterations must be at least 1")

        # prf must be callable
        if not callable(prf):
            raise TypeError("prf must be callable")

        self.__passphrase = passphrase
        self.__salt = salt
        self.__iterations = iterations
        self.__prf = prf
        self.__blockNum = 0
        self.__buf = b("")
        self.closed = False

    def close(self):
        """Close the stream."""
        if not self.closed:
            del self.__passphrase
            del self.__salt
            del self.__iterations
            del self.__prf
            del self.__blockNum
            del self.__buf
            self.closed = True


# part of pbkdf2.py --- end
# -------------------------------------------------------------------------------
