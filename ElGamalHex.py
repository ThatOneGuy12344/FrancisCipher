import random
import math
from Idea import extendeu

def primemaker():
    prime = False
    while not prime:
        num = random.randint(2647,8 * pow(10, 6))
        prime = True
        if num%2 == 0:
            prime = False
        else:
            count = 3
            while count <= int(math.sqrt(num)):
                if (num % count) == 0:
                    prime = False
                    break
                count += 2
    return num

def HCF(a,b): # highest common factor
    if a%b == 0:
        return b
    else:
        return HCF(b,a%b)
    
def bigrando(p): #to get big encryption nums
    key = random.randint(p,pow(10, 200)) 
    while HCF(p, key) != 1: 
        key = random.randint(p,pow(10, 200)) #making sure that the large number generated is not divisible by p

    return key

def Keymaker(p,g,x): #p is a prime, 0 < g < p , x .
    y = pow(g,x,p)
    return[[g,p,y],x] #public,private


def elencrypt(msg,key): #key is in list format [g,p,y]
    k = bigrando(key[1])
    a = pow(key[0],k,key[1]) #if you don't understand don't worry about it  - (g^k)%p
    b = pow(key[2],k,key[1]) #just need to know it works - (y^k)%p
    character = (msg * b)%key[1]
    encryptedmsg = a #Adding the initial info for decryption
    return [encryptedmsg,character]

def eldecrypt(cypher,key,public): # key is x, public is [g,p,y]
    a = cypher[0]
    a = pow(a,key,public[1]) #finding the decryption key from the public and private keys - (b^x)%p
    inversea = extendeu(a,public[1])
    encryptedmsg = cypher[1] #seperating the message from initial info
    msg = (encryptedmsg*inversea)%public[1] #decryption using the key
    return msg

#message = 0xffffffffffffffffffffffffffffffff
# while message == 0xffffffffffffffffffffffffffffffff:
#     prime = 365586476590046061890473535204643656701
#     key = Keymaker(prime,random.randint(1,prime - 1) ,random.randint(1,pow(10, 20)))
#     #print(key)
#     encrypted = encrypt(message,key[0])
#     #print(message)
#     message = decrypt(encrypted,key[1],key[0])
#     print(hex(message))
#     for i in encrypted:
#         print(hex(i))