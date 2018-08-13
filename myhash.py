# coding=utf-8

import math
#在第i步中，ti是4294967296*abs(sin(i))的整数部分,i的单位是弧度
tList = [int(4294967296*abs(math.sin(i))) for i in xrange(1,65)]
s = [7,12,17,22,7,12,17,22,7,12,17,22,7,
        12,17,22,5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
        4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,6,10,
        15,21,6,10,15,21,6,10,15,21,6,10,15,21]
#循环左移
def LL(X,offset,base=32):
    tmp = (1<<base)-1
    return ((X<<offset)&tmp)+((X&tmp)>>(base-offset))

def F(X,Y,Z):
    return ((X&Y)|((~X)&Z))&0xffffffff
def G(X,Y,Z):
    return ((X&Z)|(Y&(~Z)))&0xffffffff
def H(X,Y,Z):
    return (X^Y^Z)&0xffffffff
def I(X,Y,Z):
    return (Y^(X|(~Z)))&0xffffffff

# 打包整数X为字符串
def pack(X,base=32):
    return hex(X)[2:].rstrip('L').rjust(base,'0').decode('hex')[::-1]
def unpack(X,base=32):
    return int(X.ljust(base/8,'\x00')[::-1].encode('hex'),16)

# 分割32位的hash值为链变量
def hash_split(X):
    t = [X[i*8:i*8+8].decode('hex')[::-1] for i in xrange(4)]
    return [int(i.encode('hex'),16) for i in t]

# 填充文本
def md5_fill(text,length=False):
    if length is False:
        length = len(text)*8
    lenPad = hex(length)[2:].rstrip('L').rjust(16,'0').decode('hex')[::-1]
    if len(text) % 64 == 56:
        text += lenPad
        return text
    text += '\x80'
    if len(text) % 64 == 56:
        text += lenPad
        return text
    while True:
        text += '\x00'
        if len(text) % 64 == 56:
            text += lenPad
            return text

class MD5:
    def __init__(self,text='',A=0x67452301,B=0xefcdab89,C=0x98badcfe,D=0x10325476):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.text = text
        self.raw = text
        self.hash = ''

    def set_text(self,text):
        self.raw = text

    def __fill(self,length=False):
        if self.text != self.raw:
            return
        self.text = self.raw
        self.text = md5_fill(self.text,length)

    def __mainLoop(self):
        groups = [self.text[i*64:i*64+64] for i in xrange(len(self.text)/64)]
        aa = self.A
        bb = self.B
        cc = self.C
        dd = self.D
        for g in groups:
            a = aa
            b = bb
            c = cc
            d = dd
            for i in xrange(64):
                if i<16:
                    f = F(b,c,d)
                    j = i
                elif i<32:
                    f = G(b,c,d)
                    j = (5*i+1)%16
                elif i<48:
                    f = H(b,c,d)
                    j = (3*i+5)%16
                else:
                    f = I(b,c,d)
                    j = (7*i)%16
                #print f
                M = int(g[j*4:j*4+4][::-1].encode('hex'),16)
                a = b+LL(a+f+M+tList[i],s[i])
                tmp = d
                d = c
                c = b
                b = a
                a = tmp
            aa = (aa+a) & 0xffffffff
            bb = (bb+b) & 0xffffffff
            cc = (cc+c) & 0xffffffff
            dd = (dd+d) & 0xffffffff
        return aa,bb,cc,dd
    
    def get_padding_text(self):
        return self.text

    def md5(self,fillLength=False):
        self.__fill(fillLength)
        a,b,c,d = self.__mainLoop()
        self.hash = ''.join(hex(i).rstrip('L')[2:].rjust(8,'0').decode('hex')[::-1] for i in [a,b,c,d]).encode('hex')
        return self.hash

def md5(text,fillLength=False):
    m = MD5(text)
    return m.md5()

