"""

        BSD-Licensed implementation of the Isaac CSPRNG for Python3
        Usage:
            import Isaac()
            x = Isaac.Isaac(seed_vector = 32bint*256)
            y = x.rand(42) # 0<= y <= 41

"""
from math import ceil


class Isaac(object):
    def __init__(self, seed_vector=[0] * 256):
        self.mm = [0] * 256
        self.randrsl = seed_vector
        self.randcnt = None
        self.aa = 0
        self.bb = 0
        self.cc = 0

        self.__randinit__(True)

    def rand(self, num):
        if self.randcnt == 1:
            self.__isaac__()
            self.randcnt = 256

        self.randcnt -= 1

        return self.randrsl[self.randcnt] % num

    def bits(self, num):
        count = ceil(num / 32)
        bitlist = ""

        for x in range(count):
            bitlist += (bin(self.rand(4294967294))[2:].rjust(32, "0"))
        return bitlist[:num]

    def __isaac__(self):
        x = 0
        y = 0
        i = 0

        self.cc += 1
        self.bb += self.cc
        self.bb &= 0xffffffff

        while i < 256:
            x = self.mm[i]
            self.aa = (self.mm[(i + 128) & 255] +
                       (self.aa ^ (self.aa << 13))) & 0xffffffff
            self.mm[i] = y = (self.mm[(x >> 2) & 255] +
                              self.aa + self.bb) & 0xffffffff
            self.randrsl[i] = self.bb = (
                self.mm[(y >> 10) & 255] + x) & 0xffffffff
            i += 1

            x = self.mm[i]
            self.aa = (self.mm[(i + 128) & 255] + (self.aa ^
                                                   (0x03ffffff & (self.aa >> 6)))) & 0xffffffff
            self.mm[i] = y = (self.mm[(x >> 2) & 255] +
                              self.aa + self.bb) & 0xffffffff
            self.randrsl[i] = self.bb = (
                self.mm[(y >> 10) & 255] + x) & 0xffffffff
            i += 1

            x = self.mm[i]
            self.aa = (self.mm[(i + 128) & 255] +
                       (self.aa ^ (self.aa << 2))) & 0xffffffff
            self.mm[i] = y = (self.mm[(x >> 2) & 255] +
                              self.aa + self.bb) & 0xffffffff
            self.randrsl[i] = self.bb = (
                self.mm[(y >> 10) & 255] + x) & 0xffffffff
            i += 1

            x = self.mm[i]
            self.aa = (self.mm[(i + 128) & 255] + (self.aa ^
                                                   (0x0000ffff & (self.aa >> 16)))) & 0xffffffff
            self.mm[i] = y = (self.mm[(x >> 2) & 255] +
                              self.aa + self.bb) & 0xffffffff
            self.randrsl[i] = self.bb = (
                self.mm[(y >> 10) & 255] + x) & 0xffffffff
            i += 1

    def __randinit__(self, flag):
        a = b = c = d = e = f = g = h = int("9e3779b9", base=16)
        self.aa = self.bb = self.cc = 0

        for x in range(4):
            a ^= b << 1
            d += a
            b += c
            b ^= 0x3fffffff & (c >> 2)
            e += b
            c += d
            c ^= d << 8
            f += c
            d += e
            d ^= 0x0000ffff & (e >> 16)
            g += d
            e += f
            e ^= f << 10
            h += e
            f += g
            f ^= 0x0fffffff & (g >> 4)
            a += f
            g += h
            g ^= h << 8
            b += g
            h += a
            h ^= 0x007fffff & (a >> 9)
            c += h
            a += b

        i = 0
        while i < 256:
            if flag:
                a += int(self.randrsl[i])
                b += int(self.randrsl[i + 1])
                c += self.randrsl[i + 2]
                d += self.randrsl[i + 3]
                e += self.randrsl[i + 4]
                f += self.randrsl[i + 5]
                g += self.randrsl[i + 6]
                h += self.randrsl[i + 7]

            a ^= b << 11
            d += a
            b += c
            b ^= 0x3fffffff & (c >> 2)
            e += b
            c += d
            c ^= d << 8
            f += c
            d += e
            d ^= 0x0000ffff & (e >> 16)
            g += d
            e += f
            e ^= f << 10
            h += e
            f += g
            f ^= 0x0fffffff & (g >> 4)
            a += f
            g += h
            g ^= h << 8
            b += g
            h += a
            h ^= 0x007fffff & (a >> 9)
            c += h
            a += b
            self.mm[i] = a
            self.mm[i + 1] = b
            self.mm[i + 2] = c
            self.mm[i + 3] = d
            self.mm[i + 4] = e
            self.mm[i + 5] = f
            self.mm[i + 6] = g
            self.mm[i + 7] = h
            i += 8

        if flag:
            i = 0
            while i < 256:
                a += self.mm[i]
                b += self.mm[i + 1]
                c += self.mm[i + 2]
                d += self.mm[i + 3]
                e += self.mm[i + 4]
                f += self.mm[i + 5]
                g += self.mm[i + 6]
                h += self.mm[i + 7]
                a ^= b << 11
                d += a
                b += c
                b ^= 0x3fffffff & (c >> 2)
                e += b
                c += d
                c ^= d << 8
                f += c
                d += e
                d ^= 0x0000ffff & (e >> 16)
                g += d
                e += f
                e ^= f << 10
                h += e
                f += g
                f ^= 0x0fffffff & (g >> 4)
                a += f
                g += h
                g ^= h << 8
                b += g
                h += a
                h ^= 0x007fffff & (a >> 9)
                c += h
                a += b
                self.mm[i] = a
                self.mm[i + 1] = b
                self.mm[i + 2] = c
                self.mm[i + 3] = d
                self.mm[i + 4] = e
                self.mm[i + 5] = f
                self.mm[i + 6] = g
                self.mm[i + 7] = h
                i += 8
        self.__isaac__()
        self.randcnt = 256
