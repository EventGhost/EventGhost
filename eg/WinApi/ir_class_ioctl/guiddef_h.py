
from comtypes import GUID


def DEFINE_GUID(l, w1, w2, b1, b2, b3, b4, b5, b6, b7, b8):
    w0 = hex(l)[2:].upper().rstrip('L').zfill(8)
    w1 = hex(w1)[2:].upper().rstrip('L').zfill(4)
    w2 = hex(w2)[2:].upper().rstrip('L').zfill(4)
    w3 = hex((b1 << 8) | b2)[2:].upper().rstrip('L').zfill(4)
    w4 = hex(
        (((b3 << 8) | b4) << 32) |
        (((b5 << 8) | b6) << 16) |
        ((b7 << 8) | b8)
    )[2:].upper().rstrip('L').zfill(12)

    return GUID('{' + '-'.join([w0, w1, w2, w3, w4]) + '}')

