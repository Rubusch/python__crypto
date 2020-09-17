#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-May-20

Square and Multiply algorithm

algorithm to facilitate calculating exponents by disassembling the operation into
a sequence of squaring and multiplication


example

4^13 = ?

take 13 as binary
    0b1101

for each '1' now compute square-multiply-by-base, for each '0' compute a squaring
only; start with 1^2*base for the first '1'

in case apply at each step a mod(n) operation

0b    1     1    0    1
((( 1^2*4 )^2*4 )^2 )^2*4 = 67108864

or with mod(123)
((( 1^2*4 )^2*4 )^2 )^2*4 = 64 mod(123)

source

http://www.youtube.com/watch?v=rdMaG7s-lE4
http://en.wikipedia.org/wiki/Modular_exponentiation
"""

import sys

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)

def square_and_multiply(base, exp, modulus=0):
    strexp = bin(exp)[2:]
    res = 1
    for char in strexp:
        ## debug message
        print "binary: %s..."%char
        res = res*res
        if 0 != modulus:
            res = res % modulus
            # modulo operation "by foot" due to space limitations
        if char == '1':
            res = res*base
            if 0 != modulus: res = res % modulus
            ## debugging
            print "\tidentified as '1', res = [(res * res) * base ]modulus = %d"%res
        else:
            print "\tidentified as '0': res = [(res * res) ]modulus = %d"%res
    print ""
    return res


### main ###
def main(argv=sys.argv[1:]):
    base=4
    exp=13
    modulus=0 # equal to the result outside of a finite field
    if 2 <= len(argv):
        if 0 < len(argv[0]) and 0 < len(argv[1]):
            try:
                base=int(argv[0])
                exp=int(argv[1])
                if 3 == len(argv):
                    if 0 < len(argv[2]): modulus=int(argv[2])
            except:
                die("usage: %s <base> <exp>\nOR %s <base> <exp> <modulus>\nOR call without arguments"%sys.argv[0])

    ## get the greatest common divisor
    print "What is the result of %d^%d mod %d?\n"%(base, exp, modulus)
    print "%d^%d mod(%d) = %d"%(base, exp, modulus, square_and_multiply(base, exp, modulus))


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
