from BitVector import *
def binDivision(dividend, divisor, modulus):
    dividend = dividend % modulus
    divisor = divisor % modulus #force both pos
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
    factor1 %= modulus
    factor2 %= modulus
    if(factor1 > factor2):
        skeleton = BitVector(intVal = factor2)
        mover = factor1
    else:
        skeleton = BitVector(intVal = factor1)
        mover = factor1
    power = skeleton.size
    acc = 0
    for bit in skeleton:
        if bit:
            acc += (mover << power)
        power -= 1
    return (acc % modulus)
    
    

# print(binDivision(70, 21, 100))
print(binMult(65536, 31415926, 9223372036854775807))