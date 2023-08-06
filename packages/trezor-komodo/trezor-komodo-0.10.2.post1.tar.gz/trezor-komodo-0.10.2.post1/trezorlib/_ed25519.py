# orignal version downloaded from https://ed25519.cr.yp.to/python/ed25519.py
# modified for Python 3 by Jochen Hoenicke <hoenicke@gmail.com>

import hashlib
from typing import Tuple, NewType

Point = NewType("Point", Tuple[int, int])

b = 256
q = 2 ** 255 - 19
l = 2 ** 252 + 27742317777372353535851937790883648493


def H(m: bytes) -> bytes:
    return hashlib.sha512(m).digest()


def expmod(b: int, e: int, m: int) -> int:
    if e < 0:
        raise ValueError('negative exponent')
    if e == 0:
        return 1
    t = expmod(b, e >> 1, m) ** 2 % m
    if e & 1:
        t = (t * b) % m
    return t


def inv(x: int) -> int:
    return expmod(x, q - 2, q)


d = -121665 * inv(121666)
I = expmod(2, (q - 1) >> 2, q)


def xrecover(y: int) -> int:
    xx = (y * y - 1) * inv(d * y * y + 1)
    x = expmod(xx, (q + 3) >> 3, q)
    if (x * x - xx) % q != 0:
        x = (x * I) % q
    if x % 2 != 0:
        x = q - x
    return x


By = 4 * inv(5)
Bx = xrecover(By)
B = Point((Bx % q, By % q))


def edwards(P: Point, Q: Point) -> Point:
    x1 = P[0]
    y1 = P[1]
    x2 = Q[0]
    y2 = Q[1]
    x3 = (x1 * y2 + x2 * y1) * inv(1 + d * x1 * x2 * y1 * y2)
    y3 = (y1 * y2 + x1 * x2) * inv(1 - d * x1 * x2 * y1 * y2)
    return Point((x3 % q, y3 % q))


def scalarmult(P: Point, e: int) -> Point:
    if e == 0:
        return Point((0, 1))
    Q = scalarmult(P, e >> 1)
    Q = edwards(Q, Q)
    if e & 1:
        Q = edwards(Q, P)
    return Q


def encodeint(y: int) -> bytes:
    bits = [(y >> i) & 1 for i in range(b)]
    return bytes([sum([bits[i * 8 + j] << j for j in range(8)]) for i in range(b >> 3)])


def encodepoint(P: Point) -> bytes:
    x = P[0]
    y = P[1]
    bits = [(y >> i) & 1 for i in range(b - 1)] + [x & 1]
    return bytes([sum([bits[i * 8 + j] << j for j in range(8)]) for i in range(b >> 3)])


def bit(h: bytes, i: int) -> int:
    return (h[i >> 3] >> (i & 7)) & 1


def publickey(sk: bytes) -> bytes:
    h = H(sk)
    a = 2 ** (b - 2) + sum(2 ** i * bit(h, i) for i in range(3, b - 2))
    A = scalarmult(B, a)
    return encodepoint(A)


def Hint(m: bytes) -> int:
    h = H(m)
    return sum(2 ** i * bit(h, i) for i in range(2 * b))


def signature(m: bytes, sk: bytes, pk: bytes) -> bytes:
    h = H(sk)
    a = 2 ** (b - 2) + sum(2 ** i * bit(h, i) for i in range(3, b - 2))
    r = Hint(bytes([h[i] for i in range(b >> 3, b >> 2)]) + m)
    R = scalarmult(B, r)
    S = (r + Hint(encodepoint(R) + pk + m) * a) % l
    return encodepoint(R) + encodeint(S)


def isoncurve(P: Point) -> bool:
    x = P[0]
    y = P[1]
    return (-x * x + y * y - 1 - d * x * x * y * y) % q == 0


def decodeint(s: bytes) -> int:
    return sum(2 ** i * bit(s, i) for i in range(0, b))


def decodepoint(s: bytes) -> Point:
    y = sum(2 ** i * bit(s, i) for i in range(0, b - 1))
    x = xrecover(y)
    if x & 1 != bit(s, b - 1):
        x = q - x
    P = Point((x, y))
    if not isoncurve(P):
        raise ValueError('decoding point that is not on curve')
    return P


def checkvalid(s: bytes, m: bytes, pk: bytes) -> None:
    if len(s) != b >> 2:
        raise ValueError('signature length is wrong')
    if len(pk) != b >> 3:
        raise ValueError('public-key length is wrong')
    R = decodepoint(s[0:b >> 3])
    A = decodepoint(pk)
    S = decodeint(s[b >> 3:b >> 2])
    h = Hint(encodepoint(R) + pk + m)
    if scalarmult(B, S) != edwards(R, scalarmult(A, h)):
        raise ValueError('signature does not pass verification')
