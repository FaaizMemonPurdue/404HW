import sys
from PrimeGenerator import PrimeGenerator
from BitVector import BitVector

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