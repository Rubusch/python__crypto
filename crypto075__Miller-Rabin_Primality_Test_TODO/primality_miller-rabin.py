#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-September-12

Miller-Rabin's Primality Test

given the decomposition of an odd prime candidate p~
    p~ - 1 = 2^u * r

where r is odd; if we can find an integer a such that
    a^r != 1 mod p~    and   a^{r * 2^j} != p~ - 1 mod p~

for all j = {0, 1, ..., u-1}, then p~ is composite, otherwise
it is probably a prime


TEST:

Input
    prime candidate p~ with p~ - 1 = 2^u * r
    and security parameter s

Output
    statement "p~ composite" or "p~ is likely prime"

Algorithm
    for i = 1 to s:
        choose random a element of {2, 3, ..., p~ - 2}
TODO r??    
        z = a^r mod p~
        if z != 1 and z != p~ - 1:
            for j = 1 to p~:
TODO j is not used?     
                z = z^2 mod p~
                if z = 1:
                    return "p~ is composite"
            if z != p~-1:
                return "p~ is composite"
    return "p~ is likely prime"

    Input: n > 3, an odd integer to be tested for primality;
    Input: k, a parameter that determines the accuracy of the test
    Output: composite if n is composite, otherwise probably prime
    write n − 1 as 2s·d with d odd by factoring powers of 2 from n − 1
    WitnessLoop: repeat k times:
       pick a random integer a in the range [2, n − 2]
       x ← ad mod n
       if x = 1 or x = n − 1 then do next WitnessLoop
       repeat s − 1 times:
          x ← x2 mod n
          if x = 1 then return composite
          if x = n − 1 then do next WitnessLoop
       return composite
    return probably prime

"""

import sys
import random

### tools ###

def die(msg):
    if 0 < len(msg): print(msg)
    sys.exit(1)


def square_and_multiply(base, exp, modulus=0):
    strexp = bin(exp)[2:]
    res = 1
    for char in strexp:
        ## debug message
        print("binary: %s..." % char)
        res = res*res
        if 0 != modulus: res = res % modulus
        if char == '1':
            res = res*base
            if 0 != modulus: res = res % modulus
            ## debugging
            print("\tidentified as '1', res = (res^2)*base = %d"%res)
        else:
            print("\tidentified as '0': res = (res^2) = %d"%res)
    print ""
    return res


### main ###
def main(argv=sys.argv[1:]):
    print("Miller-Rabin's Primality Test")
    arg=545

    ## get arguments, or set default values
    if 1 == len(argv):
        if 0 < len(argv[0]):
            try:
                arg=int(argv[0])
            except:
                die("usage: %s <arg>\nOR call without arguments"%sys.argv[0] )
    if 4 >= arg: die("FATAL: arg must be greater than 4")

    k = 3 # 3 iterations, precision
    print("arg = %d" % arg) # number to test
    print("k = %d" % k)# number of iterations for precision

#    base=random.randrange(2, arg-2)    



    ## get s, the logarithm to base 2 which still divides arg-1
    s = 1
    while 0 == (arg-1) % (2**s):
        s+=1
        print("2**s = %d\t| %d"%(2**s, arg-1))
    s-=1
    ## for 545 it will be 5


    ## get the factor d
    d = (arg-1)/(2**s)
    ## for 545 it will be 17


    ## select a witness by random
#    w = random.randrange(2, arg-2)
    w = 492   

    for rnd in range(k):
        print("%d ** %d mod %d = %d\t== 0 ?"%(w, d, arg, w**d%arg))
        if 0 == w**d % arg:
            
            print("passed! TODO")
            break
        d*=2
# http://www.johannes-bauer.com/compsci/millerrabin/index.php?zahl=545&iterationen=3&calculate=1

    die("XXX d = %d" % d)    
        
    

#    z = square_and_multiply(base, r, arg)
#    if z != 1 and z != r-1:
#        for idx in range(arg-1):
#

    
    die("XXX arg %d" % arg)     
    


### start ###
if __name__ == '__main__':
    main()
print("READY.\n")
