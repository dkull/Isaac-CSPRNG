"""
        Isaac CSPRNG
        Usage:
            import Isaac()
            x = Isaac.Isaac(noblock=False)
            y = x.rand(42) # 0<= y <= 41
        Warning: If you don't have /dev/random(noblock=False) nor /dev/urandom(noblock=True) Pythons builtin Random() will be used
"""
import random
import os
try:
    import psyco
    psyco.full()
except:
    pass

class Isaac(object):
    def __init__(self, noblock = True):
        self.mm = [0]*256
        self.randrsl = [0]*256
        self.randcnt = None
        self.aa = 0
        self.bb = 0
        self.cc = 0
        random.seed()

        # If noblock is set to "False" on init it will seed from /dev/random
        rnd_source = '/dev/urandom' if noblock else '/dev/random'
        if os.path.exists(rnd_source):
            f = open(rnd_source, 'r')
            for x in xrange(256):
                z = f.read(4)
                # String to binary and back to larger integer
                y = int("".join([bin(ord(i))[2:].rjust(8,"0") for i in list(z)]), base=2)

                self.randrsl[x] = y
            f.close()
        else:
            for x in xrange(256):
                self.randrsl[x] = random.randint(1,4294967294)
            
        self.randinit(True)

    def rand(self, num):
        if self.randcnt == 1:
            self.isaac()
            self.randcnt = 256

        self.randcnt -= 1

        return self.randrsl[self.randcnt]%num

    def isaac(self):
        x = 0
        y = 0
        i = 0
        
        self.cc += 1
        self.bb += self.cc
        self.bb &= 0xffffffff

    
        while i < 256:
            x = self.mm[i]
            self.aa = (self.mm[(i + 128) & 255] + (self.aa^(self.aa << 13)) ) & 0xffffffff
            self.mm[i] = y = (self.mm[(x>>2)&255] + self.aa + self.bb ) & 0xffffffff
            self.randrsl[i] = self.bb = (self.mm[(y>>10)&255] + x ) & 0xffffffff
            i += 1
     
            x = self.mm[i]
            self.aa = (self.mm[(i+128)&255] + (self.aa^(0x03ffffff & (self.aa >> 6))) ) & 0xffffffff
            self.mm[i] = y = (self.mm[(x>>2)&255] + self.aa + self.bb ) & 0xffffffff
            self.randrsl[i] = self.bb = (self.mm[(y>>10)&255] + x ) & 0xffffffff
            i += 1
     
            x = self.mm[i]
            self.aa = (self.mm[(i + 128)&255] + (self.aa^(self.aa << 2)) ) & 0xffffffff
            self.mm[i] = y = (self.mm[(x>>2)&255] + self.aa + self.bb ) & 0xffffffff
            self.randrsl[i] = self.bb = (self.mm[(y>>10)&255] + x ) & 0xffffffff
            i += 1
     
            x = self.mm[i]
            self.aa = (self.mm[(i+128)&255] + (self.aa^(0x0000ffff & (self.aa >> 16))) ) & 0xffffffff
            self.mm[i] = y = (self.mm[(x>>2)&255] + self.aa + self.bb ) & 0xffffffff
            self.randrsl[i] = self.bb = (self.mm[(y>>10)&255] + x ) & 0xffffffff
            i += 1

    def randinit(self, flag):
        a=b=c=d=e=f=g=h = int("9e3779b9", base=16)
        self.aa = self.bb = self.cc = 0

        for x in xrange(4):
            a ^= b<<1
            d += a
            b += c
            b ^= 0x3fffffff & (c>>2)
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
                a+=int(self.randrsl[i])
                b+=int(self.randrsl[i+1])
                c+=self.randrsl[i+2]
                d+=self.randrsl[i+3]
                e+=self.randrsl[i+4]
                f+=self.randrsl[i+5]
                g+=self.randrsl[i+6]
                h+=self.randrsl[i+7]

            a^=b<<11
            d+=a
            b+=c
            b^=0x3fffffff & (c>>2)
            e+=b
            c+=d
            c^=d<<8
            f+=c
            d+=e
            d^=0x0000ffff & (e>>16)
            g+=d
            e+=f
            e^=f<<10
            h+=e
            f+=g
            f^=0x0fffffff & (g>>4)
            a+=f
            g+=h
            g^=h<<8
            b+=g
            h+=a
            h^=0x007fffff & (a>>9)
            c+=h
            a+=b
            self.mm[i]=a
            self.mm[i+1]=b
            self.mm[i+2]=c
            self.mm[i+3]=d
            self.mm[i+4]=e
            self.mm[i+5]=f
            self.mm[i+6]=g
            self.mm[i+7]=h
            i += 8

        if flag:
            i = 0
            while i < 256:
                a+=self.mm[i]
                b+=self.mm[i+1]
                c+=self.mm[i+2]
                d+=self.mm[i+3]
                e+=self.mm[i+4]
                f+=self.mm[i+5]
                g+=self.mm[i+6]
                h+=self.mm[i+7]
                a^=b<<11
                d+=a
                b+=c
                b^=0x3fffffff & (c>>2)
                e+=b
                c+=d
                c^=d<<8
                f+=c
                d+=e
                d^=0x0000ffff & (e>>16)
                g+=d
                e+=f
                e^=f<<10
                h+=e
                f+=g
                f^=0x0fffffff & (g>>4)
                a+=f
                g+=h
                g^=h<<8
                b+=g
                h+=a
                h^=0x007fffff & (a>>9)
                c+=h
                a+=b
                self.mm[i]=a
                self.mm[i+1]=b
                self.mm[i+2]=c
                self.mm[i+3]=d
                self.mm[i+4]=e
                self.mm[i+5]=f
                self.mm[i+6]=g
                self.mm[i+7]=h
                i += 8
        self.isaac()
        self.randcnt=256

