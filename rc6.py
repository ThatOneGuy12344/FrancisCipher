import math
import sys
from Idea import encryption,decryption
from ElGamalHex import eldecrypt,elencrypt

#rotate right input x, by n bits
def ROR(x, n, bits = 32):
    mask = (2**n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (bits - n))

#rotate left input x, by n bits
def ROL(x, n, bits = 32):
    return ROR(x, bits - n,bits)

#generate key s[0... 2r+3] from given input string userkey
def generateKey(userkey):
    r=12
    w=32
    modulo = 2**32
    s=(2*r+4)*[0]
    s[0]=0xB7E15163
    for i in range(1,2*r+4):
        s[i]=(s[i-1]+0x9E3779B9)%(2**w)
    encoded = userkey
    D = encoded &0xffffffff
    C = (encoded >> w) & 0xffffffff
    B = (encoded >> w*2) & 0xffffffff
    A = (encoded >> w*3) & 0xffffffff
    #print encoded
    l = [A,B,C,D] 
    v = 3*(2*r+4)
    A=B=i=j=0
    
    for k in range(0,v):
        A = s[i] = ROL((s[i] + A + B)%modulo,3,32)
        B = l[j] = ROL((l[j] + A + B)%modulo,(A+B)%32,32)
        i = (i + 1) % (2*r + 4)
        j = ((j + 1) % 4) + k - k
    return s

def seperate(encoded,w):
    D = encoded & 0xffffffff
    C = (encoded >> w) & 0xffffffff
    B = (encoded >> w * 2) & 0xffffffff
    A = (encoded >> w * 3) & 0xffffffff
    return A,B,C,D

def join(A,B,C,D,w):
    cipher = A
    cipher = (cipher << w) + B
    cipher = (cipher << w) + C
    cipher = (cipher << w) + D
    return cipher

def rcencrypt(sentence,key,r = 12,w = 32):
    encoded = sentence
    s = generateKey(key)
    A,B,C,D = seperate(encoded,w)
    modulo = 2**w
    lgw = int(math.log2(w))
    B = (B + s[0])%modulo
    D = (D + s[1])%modulo 
    for i in range(1,r+1):
        t_temp = (B*(2*B + 1))%modulo 
        u_temp = (D*(2*D + 1))%modulo
        t = ROL(t_temp,lgw,w)
        u = ROL(u_temp,lgw,w)
        tmod=t%w
        umod=u%w
        A = (ROL(A^t,umod,w) + s[2*i])%modulo
        C = (ROL(C^u,tmod,w) + s[2*i+ 1])%modulo
        (A, B, C, D)  =  (B, C, D, A)
        #IDEA
        stuff = (B << w) + D
        text = encryption(stuff,key)
        t_temp = text >> w
        u_temp = text % 0xffffffff
        #print(A,B,C,D)
    A = (A + s[2*r + 2])%modulo 
    C = (C + s[2*r + 3])%modulo
    cipher = join(A,B,C,D,w)
    return cipher


def rcdecrypt(esentence,key,r = 12,w = 32):
    encoded = esentence
    s = generateKey(key)
    A,B,C,D = seperate(encoded,w)
    modulo = 2**w
    lgw = int(math.log2(w))
    C = (C - s[2*r+3])%modulo
    A = (A - s[2*r+2])%modulo
    for j in range(1,r+1):
        i = r+1-j
        #print(A,B,C,D)
        (A, B, C, D) = (D, A, B, C)
        u_temp = (D*(2*D + 1))%modulo
        t_temp = (B*(2*B + 1))%modulo
        u = ROL(u_temp,lgw,w)
        t = ROL(t_temp,lgw,w)
        tmod=t%w
        umod=u%w
        C = ROR((C-s[2*i+1])%modulo,tmod,w)  ^u
        A = ROR((A-s[2*i])%modulo,umod,w)   ^t
        #IDEA
        stuff = (B << w) + D
        text = decryption(stuff,key)
        t_temp = text >> w
        u_temp = text % 0xffffffff
    D = (D - s[1])%modulo
    B = (B - s[0])%modulo
    orgi = join(A,B,C,D,w)
    return orgi


# key = 0xdaa75740bd016cd60765fbf22883d1a8
# sentence = 0xdaa75740bd016cd60765fbf22883d1a8
# s = generateKey(key)    
# cipher = encrypt(sentence,s,key)
# print("\nOriginal String list: ",hex(sentence))
# print("\nEncrypted String list: ",hex(cipher))
# orgi = decrypt(cipher,s,key)
# print("\nDecrypted:",hex(orgi))