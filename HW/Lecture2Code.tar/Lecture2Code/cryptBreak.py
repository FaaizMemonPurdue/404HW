#!/usr/bin/env python

from BitVector import *                                                     #(A)
def cryptBreak(ciphertextFile, key_bv): 
    # The following code is entirely taken from "decryptForFun.py," having removed
    # the code relating to turning a string input to key_bv and changing the BLOCKSIZE
    # down to 16 from 64
    # Arguments:
    # * ciphertextFile: String containing file name of the ciphertext
    # * key_bv: 16-bit BitVector for the decryption key
    #
    # Function Description:
    # Attempts to decrypt the ciphertext within ciphertextFile file using
    # key_bv and returns the original plaintext as a string
    PassPhrase = "Hopes and dreams of a million years"                          #(C)

    BLOCKSIZE = 16                                                              #(D)
    numbytes = BLOCKSIZE // 8                                                   #(E)

    # Reduce the passphrase to a bit array of size BLOCKSIZE:
    bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)                                  #(F)
    for i in range(0,len(PassPhrase) // numbytes):                              #(G)
        textstr = PassPhrase[i*numbytes:(i+1)*numbytes]                         #(H)
        bv_iv ^= BitVector( textstring = textstr )                              #(I)

    # Create a bitvector from the ciphertext hex string:
    FILEIN = open(ciphertextFile)                                                  #(J)
    encrypted_bv = BitVector( hexstring = FILEIN.read() )                       #(K)
    # Create a bitvector for storing the decrypted plaintext bit array:
    msg_decrypted_bv = BitVector( size = 0 )                                    #(T)

    # Carry out differential XORing of bit blocks and decryption:
    previous_decrypted_block = bv_iv                                            #(U)
    for i in range(0, len(encrypted_bv) // BLOCKSIZE):                          #(V)
        bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE]                          #(W)
        temp = bv.deep_copy()                                                   #(X)
        bv ^=  previous_decrypted_block                                         #(Y)
        previous_decrypted_block = temp                                         #(Z)
        bv ^=  key_bv                                                           #(a)
        msg_decrypted_bv += bv                                                  #(b)

    # Extract plaintext from the decrypted bitvector:    
    outputtext = msg_decrypted_bv.get_text_from_bitvector()                     #(c)

    # Write plaintext to the output file:
    return outputtext

if __name__ == "__main__":
    sol = ""
    BLOCKSIZE = 16
    keyspace = 2**BLOCKSIZE
    for keyint in range(0, keyspace):
        key_bv = BitVector(intVal = keyint, size = 16)                                 
        sol = cryptBreak("ciphertext.txt", key_bv)
        if "Sir Lewis" in sol:
            break

    print(sol)
    print(keyint)