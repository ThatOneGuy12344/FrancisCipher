def extendeu(num1,num2):
    a = num1
    m = num2
    m1 = m
    e = 1
    y = 0
    while a > 1:
        y,e = e - int(a/m1) * y,y
        m1,a = a % m1,m1
    if e < 0:
        e += m
    return e

def tth(pt):
    ct = 0x0000000000000000
    for i in range(5):
        num = ord(pt[i])
        if num < 255:
            ct += num*(16**(2*i))
    return ct

def htt(ct):
    pt = ''
    for i in range(8):
        number = ct >> (i * 8) & 0xff
        pt += chr(number)
    return pt

def keyrounds(key):
    sub_keys = []
    for i in range(7):
        #print(hex(key))
        for j in range(8 + i - i):
            if len(sub_keys) != 52:
                sub_keys += [(key >> 112 - 16 * j) & 0xffff]
        key = ((key << 25) | (key >> 103)) % 0x100000000000000000000000000000000
        #print(hex(key))
    return sub_keys

def dekeyrounds(key):
    key = keyrounds(key)
    sub_keys = []
    for i in range(9):
        for k in range(6):
            if k%6 == 0 or k%6 == 3:
                inverse = extendeu(key[48 - i * 6 + k],65537) #multiplicitive inverse
                sub_keys += [inverse]
            elif k%6 == 1 or k%6 == 2:
                sub_keys += [key[48 - i * 6 + k] * -1] #addition inverse
            elif i != 8:
                sub_keys += [key[42 - i * 6 + k]]
    return sub_keys

def XOR(hex1,hex2):
    return hex1 ^ hex2

def ADD(hex1,hex2):
    return (hex1 + hex2)%0x10000

def MUL(hex1,hex2):
    if hex1 == 0x0000:
        hex1 = 0x10000
    elif hex1 == 0x10000:
        hex1 = 0x0000
    if hex2 == 0x0000:
        hex2 = 0x10000
    elif hex2 == 0x10000:
        hex2 = 0x0000
    if (hex1 * hex2)%(0x10001) == 0x10000:
        return 0
    return (hex1 * hex2)%(0x10001)

def top(text,keys): #Top half of IDEA round
    #print(keys)
    text[0],text[1],text[2],text[3] = MUL(text[0],keys[0]),ADD(text[1],keys[1]),ADD(text[2],keys[2]),MUL(text[3],keys[3])
    return text

def bot(text,keys): #Bottom half of IDEA round
    #print(keys)
    temp1,temp2 = XOR(text[0],text[2]),XOR(text[1],text[3])
    temp1 = MUL(temp1,keys[0])
    temp2 = MUL(ADD(temp1,temp2),keys[1])
    temp1 = ADD(temp1,temp2)
    text[0],text[1],text[2],text[3] = XOR(temp2,text[0]),XOR(temp1,text[1]),XOR(temp2,text[2]),XOR(temp1,text[3])
    return text

def encryption(pt,k):
    k = keyrounds(k)
    text = []
    for i in range(4):
        text += [pt >> 48 - (16 * i) & 0xffff]
    for i in range(8):
        keys = k[i * 6:i * 6 + 6]
        text = top(text,keys[0:4])
        text = bot(text,keys[4:6])
        text[1],text[2] = text[2],text[1]
    text[1],text[2] = text[2],text[1]
    text = top(text,k[48:52])
    ct = 0x0000
    for i in range(len(text)):
        ct += text[i]
        ct = ct << 16
    return ct >> 16

def decryption(ct,k):
    k = dekeyrounds(k)
    text = []
    for i in range(4):
        text += [ct >> 48 - (16 * i) & 0xffff]
    for i in range(8):
        keys = k[i * 6:i * 6 + 6]
        text = top(text,keys[0:4])
        if i != 0:
            text[1],text[2] = text[2],text[1]
        text = bot(text,keys[4:6])
    text = top(text,k[48:52])
    pt = 0x0000
    for i in range(len(text)):
        pt += text[i]
        pt = pt << 16
    return pt >> 16

