from BitVector import *
def binDivision(dividend, divisor, modulus):
    dividend = dividend % modulus
    divisor = divisor % modulus #force both pos
    if divisor > dividend: return (0, dividend) #self-explanatory
    
    remainder = dividend % divisor  
    clean_dividend = dividend - remainder #strip off the remainder so clean_dividend will divide exactly by divisor
    # bit_clean_dividend = BitVector(intVal = clean_dividend)
    # bit_divisor = BitVector(intVal = divisor)
    power = bit_clean_dividend.size - bit_divisor.size
    padded_divisor = bit_divisor.deep_copy()
    padded_divisor.pad_from_right(power)
    # padded_divisor = bit_divisor.pad_from_right(power) #since bitvector uses min # bits this aligns both Most Significant 1's
    #this is why we wanted to modulo right away for pos vals
    quotient = 0 
    while(bit_clean_dividend.int_val() > 0):
        if(bit_clean_dividend >= padded_divisor):
            newVal = bit_clean_dividend.int_val() - padded_divisor.int_val()
            bit_clean_dividend.set_value(intVal = newVal)
            quotient += 1 << power
        power -= 1
        padded_divisor.shift_right(1)
    return (quotient, remainder)

print(binDivision(123, 21, 9223372036854775807))