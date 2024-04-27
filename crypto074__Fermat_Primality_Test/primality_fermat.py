#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-September-08

Fermat's Primality Test

    a^{C-1} = 1 mod C


Fermat's little theorem holds for all primes. Hence if a number does not fulfill
Fermat's Little Theorem, it is certainly not a prime.
    a^{prime} = a mod prime
    a^{prime-1} = 1 mod prime   ; as result of multiplying by its inverse

NOTE: The test fails for the rare Carmichael Numbers, e.g. 561

Composite numbers known as Fermat pseudoprimes (or sometimes simply
"pseudoprimes") have zero residue for some as and so are not identified as
composite. Worse still, there exist numbers known as Carmichael numbers (the
smallest of which is 561) which give zero residue for any choice of the base a
relatively prime to p. However, Fermat's little theorem converse provides a
criterion for certifying the primality of a number. A table of the smallest
pseudoprimes P for the first 100 bases a follows (OEIS A007535; Beiler 1966,
p. 42 with typos corrected).
[http://mathworld.wolfram.com/FermatsLittleTheorem.html]



Input
    prime candidate p~ and security parameter s

Output
    statement "p~ is composite" or "p~ is likely prime"

Algorithm
    for i = 1 to s:
        choose random a element of {2, 3, ..., p~ -2}
        if a^{p~ - 1} != 1 mod p~:
            return "p~ is a composite"
    return "p~ is likely prime"
"""

import sys
import random

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
        if 0 != modulus: res = res % modulus
        if char == '1':
            res = res*base
            if 0 != modulus: res = res % modulus
            ## debugging
            print "\tidentified as '1', res = (res^2)*base = %d"%res
        else:
            print "\tidentified as '0': res = (res^2) = %d"%res
    print ""
    return res


## (Alford et al. 1994), which proves that there are infinitely many Carmichael numbers.
carmichael_numbers = {561,1105,1729,2465,2821,6601,8911,10585,15841,29341,41041,46657,52633,62745,63973,75361} #...


### main ###
def main(argv=sys.argv[1:]):
    print "Fermat's Primality Test"
    arg=545 ## seems to be a Fermat Pseudoprime to 328

    ## get arguments, or set default values
    if 1 == len(argv):
        if 0 < len(argv[0]):
            try:
                arg=int(argv[0])
            except:
                die("usage: %s <arg>\nOR call without arguments"%sys.argv[0] )
    if 4 >= arg: die("FATAL: arg must be greater than 4")

    ## take fixed base of 2, since other bases may have different issues
    base = 2
    if arg == 341: die("%d is a Fermat Pseudoprime number to the base %d -> the test would fail!!"%(arg, base))
    if arg in carmichael_numbers: die("%d is a Carmichael Number, which behaves Fermat Pseudoprime in this test"%arg)
    ## to play around with it, use a random base
#    base=random.randrange(2, arg-2) # pick a random number as base

    print "arg = %d, base = %d"%(arg, base)
    print "Is %d a prime number, by Fermat's Primality Test?\n"%arg

    ## the actual test
    if 1 != square_and_multiply(base, arg-1, arg):
        print "%d is not a prime!"%arg
    else:
        print "%d can be a prime!"%arg


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
