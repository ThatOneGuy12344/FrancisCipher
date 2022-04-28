from Idea import encryption,decryption
from ElGamalHex import eldecrypt,elencrypt, Keymaker
from rc6 import rcencrypt,rcdecrypt



##This is the key to encrypt using RC6


key = 0xdaa75740bd016cd60765fbf22883d1a8


##


print("The current key to be used for Francis encryption is " , str(hex(key)) , " if you would like to change it please read README.txt")
option = -1
while option != 0:
        option = int(input("Enter 1 for El Gamal and 2 for Francis Cipher (0 to exit): "))
        if option == 1:
            #El Gamal
            print("Input 0 if you want to use default values")
            print("---------------------------------------------------")
            print("Key exchange with El Gamal") 


            p = int(input("Please enter a prime number above 10^39, default(506520198124071737570316816152142491534807): "))
            if p == 0:
                p = 506520198124071737570316816152142491534807

            g = int(input("Please enter a number between 0 and the prime non inclusive,default(51312165445642184845151315343)"))
            if g == 0:
                g = 51312165445642184845151315343

            x = int(input("Please enter a random number, the bigger the better. Default(231546519423165747324651232132): "))
            if x == 0:
                x = 231546519423165747324651232132

            elkey = Keymaker(p,g,x)
            print("The El gamal public key is: ",elkey[0])
            print("The El gamal private key is: ",elkey[1])
            elencrypted = elencrypt(key,elkey[0])
            print("The El gamal encrypted string is ",elencrypted)
            eldecrypted = eldecrypt(elencrypted,x,elkey[0])
            print("The El gamal decrypted string is ",eldecrypted)

        if option == 2:
            #Francis Encryption

            optiontwo = -1
            while optiontwo != 1 and optiontwo != 2:
                optiontwo = int(input("Input 1 for Encryption and 2 for Decryption: "))
            sentence = input("Please enter your sentence (in hex) default(0xdaa75740bd016cd60765fbf22883d1a8): ")
            if sentence == "0":
                sentence = "0xdaa75740bd016cd60765fbf22883d1a8"
            sentence = sentence[2:]
            chunks = [sentence[i:i+32] for i in range(0, len(sentence), 32)]
            finaldecrypted = ""
            finalencrypted = ""
            for x in chunks:
                if x == "" or x == " ":
                    break
                x = "0x" + x
                x = int(x,0)
                if optiontwo == 1:
                    cipher = rcencrypt(x,key)
                    finalencrypted += hex(cipher)[2::]
                elif optiontwo == 2:
                    orgi = rcdecrypt(x,key)
                    finaldecrypted += hex(orgi)[2::]
            finaldecrypted = "0x" + finaldecrypted
            finalencrypted = "0x" + finalencrypted
            if optiontwo == 1:
                print("The Encrypted String is: ",finalencrypted)
            elif optiontwo == 2:
                print("The Decrypted String is: ",finaldecrypted)