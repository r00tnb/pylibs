from struct import unpack, pack
import math
import binascii


class MD5:
    @staticmethod
    def F(X: int, Y: int, Z: int):
        return ((X & Y) | ((~X) & Z))

    @staticmethod
    def G(X: int, Y: int, Z: int):
        return ((X & Z) | (Y & (~Z)))

    @staticmethod
    def H(X: int, Y: int, Z: int):
        return (X ^ Y ^ Z)

    @staticmethod
    def I(X: int, Y: int, Z: int):
        return (Y ^ (X | (~Z)))

    @staticmethod
    def LL(X: int, offset: int):
        '''将32bits整数循环向左移动offset位，base指定最大位数
        '''
        X &= 0xffffffff
        return ((X << offset) & 0xffffffff) | (X >> (32-offset))

    def __init__(self, data=b'', A=0x67452301, B=0xefcdab89, C=0x98badcfe, D=0x10325476):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.raw = data
        self.hash: bytes = None

    def fill(self, data: bytes) -> bytes:
        '''填充数据使其能够进行md5摘要运算
        '''
        bist_length = len(data)*8
        if len(data) % 64 == 56:
            data += pack('<Q', bist_length)
            return data
        data += b'\x80'
        if len(data) % 64 >= 56:
            data += pack('<Q', bist_length)
            return data
        while True:
            data += b'\x00'
            if len(data) % 64 == 56:
                data += pack('<Q', bist_length)
                return data

    def digest(self) -> bytes:
        '''返回md5 hash值
        '''
        self.hash = self.__loop(self.fill(self.raw))
        return self.hash

    def hexdigest(self) -> str:
        '''返回16进制编码的结果
        '''
        return binascii.hexlify(self.digest()).decode()

    def __loop(self, filledData: bytes) -> bytes:
        '''摘要计算循环，返回最终结果
        '''
        tList = [int(4294967296*abs(math.sin(i))) for i in range(1, 65)]
        s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7,
             12, 17, 22, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
             4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 6, 10,
             15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
        aa, bb, cc, dd = self.A, self.B, self.C, self.D

        for i in range(0, len(filledData), 64):
            group = filledData[i:i+64]
            a, b, c, d = aa, bb, cc, dd
            f, g = 0, 0
            for k in range(64):
                if k < 16:
                    f = MD5.F(b, c, d)
                    g = k
                elif k < 32:
                    f = MD5.G(b, c, d)
                    g = (5*k+1) % 16
                elif k < 48:
                    f = MD5.H(b, c, d)
                    g = (3*k+5) % 16
                else:
                    f = MD5.I(b, c, d)
                    g = (7*k) % 16

                a, b, c, d = d, b + \
                    MD5.LL(a+f+tList[k]+unpack('<I',
                           group[g*4:g*4+4])[0], s[k]), b, c
            aa, bb, cc, dd = a+aa, b+bb, c+cc, d+dd

        return pack('<4I', aa & 0xffffffff, bb & 0xffffffff, cc & 0xffffffff, dd & 0xffffffff)
