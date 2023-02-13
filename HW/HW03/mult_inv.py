#!/usr/bin/env python
## FindMI.py



import sys
from BitVector import *
def binDivision(dividend, divisor, modulus):
    dividend = dividend % modulus
    divisor = divisor % modulus #force both pos
    if not dividend: dividend = modulus
    if not divisor: divisor = modulus
    if divisor > dividend: return (0, dividend) #self-explanatory
    
    remainder = dividend % divisor  
    clean_dividend = dividend - remainder #strip off the remainder so clean_dividend will divide exactly by divisor
    bit_clean_dividend = BitVector(intVal = clean_dividend)
    bit_divisor = BitVector(intVal = divisor)
    power = bit_clean_dividend.size - bit_divisor.size
    padded_divisor = bit_divisor.deep_copy()
    padded_divisor.pad_from_right(power)
    #this is why we wanted to modulo right away for pos vals
    quotient = 0 
    while(bit_clean_dividend.int_val() > 0): 
        if(bit_clean_dividend >= padded_divisor):
            newVal = bit_clean_dividend.int_val() - padded_divisor.int_val()
            bit_clean_dividend.set_value(intVal = newVal)
            quotient += 1 << power 
        power -= 1 #may be possible to optimize to make more than one step based on spaces between 1s
        padded_divisor.shift_right(1)
    return (quotient % modulus, remainder % modulus)

def binMult(factor1, factor2, modulus): 
    if factor1 % modulus: factor1 %= modulus
    if factor2 % modulus: factor2 %= modulus
    
    # factor2 %= modulus
    if(factor1 > factor2):
        skeleton = BitVector(intVal = factor2)
        mover = BitVector(intVal = factor1)
    else:
        skeleton = BitVector(intVal = factor1)
        mover = BitVector(intVal = factor2)
    power = skeleton.size - 1
    mover.pad_from_right(power)
    acc = 0
    for bit in skeleton:
        if bit:
            acc += mover.int_val()
        power -= 1
        mover.shift_right(1)
    return (acc % modulus)

def MI(num, mod):
    '''
    This function uses ordinary integer arithmetic implementation of the
    Extended Euclid’s Algorithm to find the MI of the first-arg integer
    vis-a-vis the second-arg integer.
    '''
    if (not mod) or (not num % mod): 
        print("Additive Identity Entered, no MI")
        return 0 #num is a direct multiple of mod
    
    NUM = num; MOD = mod
    x, x_old = 0, 1
    y, y_old = 1, 0
    while mod:

        num, (q, mod) = mod, binDivision(num, mod, MOD)
        
        
        x, x_old = x_old - binMult(q, x, MOD), x
        
        # x, x_old = x_old - q * x, x
        y, y_old = y_old - binMult(q, y, MOD), y
    if num != 1:
        print("\nNO MI. However, the GCD of %d and %d is %u\n" % (NUM, MOD, num))
    else:
        MI = (x_old + MOD) % MOD
        print("\nMI of %d modulo %d is: %d\n" % (NUM, MOD, MI))


if len(sys.argv) != 3:
    sys.stderr.write("Usage: %s <integer> <modulus>\n" % sys.argv[0])
    sys.exit(1)

NUM, MOD = int(sys.argv[1]), int(sys.argv[2])
MI(NUM, MOD)
