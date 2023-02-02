from BitVector import *   
from cryptBreak import cryptBreak
keyint = 10
key = str(keyint)                                               #(O)
BLOCKSIZE = 16                                                              #(D)
numbytes = BLOCKSIZE // 8        
                                           #(E)
sol = ""
keyspace = 2**BLOCKSIZE
for keyint in range(0, keyspace):
    key_bv = BitVector(intVal = keyint)                                 #(P)
    sol = cryptBreak("ciphertext.txt", key_bv)
    if "Sir Lewis" in sol:
        break

print(sol)
print(key)