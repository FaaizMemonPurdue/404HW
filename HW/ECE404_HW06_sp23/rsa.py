import sys
from PrimeGenerator import PrimeGenerator
from BitVector import BitVector
e = 65537
PTSIZE = 128
CTSIZE = 256
#mathematical functions

def gcd(a : int, b : int) -> int: #from Lecture 5
    while b:
        a,b = b, a%b
    return a

def generation():
    generator = PrimeGenerator(bits=128)
    p = generator.findPrime()
    q = generator.findPrime()
    #no need to check 1st two bits, defined by the original
    while(gcd(p-1, e) != 1):
        p = generator.findPrime()
    while(gcd(q-1, e) != 1):
        q = generator.findPrime()
    if(p == q):
        return generation() #bananas case
    return p, q

#helpers
def readpq(pFilename : str, qFilename : str): 
    with open(pFilename, "r") as pFile, open(qFilename, "r") as qFile:
        p = int(pFile.read()); q = int(qFile.read())
    return p, q

def writepq(pFilename : str, qFilename : str, genp : int, genq : int): 
    with open(pFilename, "w") as pFile, open(qFilename, "w") as qFile:
        pFile.write(str(genp)); qFile.write(str(genq))


#real guys
def encrypt(n : int, ptFilename : str, ctFilename : str): 
    #data block size = 128 bits = q size = p size
    # pow(x,y,z)
    pt_ovr_bv = BitVector(filename = ptFilename)
    with open(ctFilename, "w") as ctFile:
        while pt_ovr_bv.more_to_read:
            pt_bv_read = pt_ovr_bv.read_bits_from_file(PTSIZE)  #try to read in 128 bits                              
            pt_bv_read.pad_from_right(PTSIZE - len(pt_bv_read)) #do the pad from right, fill to 128 bits
            pt_bv_read.pad_from_left(PTSIZE) #pad from left by 128 bits
            messageInt = int(pt_bv_read)
            cipherInt = pow(messageInt, e, n)
            ct_bv = BitVector(intVal = cipherInt, size=256)
            ctFile.write(ct_bv.get_bitvector_in_hex())        

def decrypt(p : int, q : int, n : int, ctFilename : str, ptFilename : str):
    
    #e n d operations
    bv_e = BitVector(intVal = e)
    bv_totient = BitVector(size = 256, intVal = (p-1) * (q-1))
    bv_d = bv_e.multiplicative_inverse(bv_totient) # calc d
    
    d = int(bv_d)
    d_p = d % (p-1)
    d_q = d % (q-1)

    #pq operations
    bv_p = BitVector(size = 128, intVal = p)
    bv_q = BitVector(size = 128, intVal = q)

    bv_MI_p_mod_q = bv_p.multiplicative_inverse(bv_q)
    MI_p_mod_q = int(bv_MI_p_mod_q)
    Xq = p * MI_p_mod_q

    bv_MI_q_mod_p = bv_q.multiplicative_inverse(bv_p)
    MI_q_mod_p = int(bv_MI_q_mod_p)
    Xp = q * MI_q_mod_p

    with open(ctFilename, "r") as ctFile:
        ct_ovr_bv = BitVector(hexstring = ctFile.read())

    blocksToDecrypt = len(ct_ovr_bv) // 256
    with open(ptFilename, "w") as ptFile:
        for encrypted in range(blocksToDecrypt):
            ct_bv_read = ct_ovr_bv[256*encrypted:256*(encrypted+1)]  #try to read in 256 bits  

            if len(ct_bv_read) != 256: return #something has gone terribly wrong in encryption

            cipherInt = int(ct_bv_read)

            Vp = pow(cipherInt, d_p, p)
            Vq = pow(cipherInt, d_q, q)

            messageInt = (Vp * Xp + Vq * Xq) % n
            
            pt_bv_sliced = BitVector(intVal = messageInt, size=256)[128:256]
            #after mod exponent, skim off the first 128 bits (should have recovered 0 padding by now)
            ptFile.write(pt_bv_sliced.get_bitvector_in_ascii())      

if sys.argv[1] == "-e":
    p, q = readpq(sys.argv[3], sys.argv[4])
    encrypt(p * q, ptFilename=sys.argv[2], ctFilename=sys.argv[5])

elif sys.argv[1] == "-d":
    p, q = readpq(sys.argv[3], sys.argv[4])
    decrypt(p, q, p * q, ctFilename=sys.argv[2], ptFilename=sys.argv[5])
    
elif sys.argv[1] == "-g":
    genp, genq = generation()
    writepq(sys.argv[2], sys.argv[3], genp, genq)
else:
    print('whoops')