#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-May-20

Fermat's Little Theorem is one way to compute the inverse to a value in a finite field.
   a^{-1} = a^{p-2} mod p


Fermat's Little Theorem

let a be an integer and p be a prime, then
    a^p = a mod p

the inverse thus is:
    a^{-1} = a^{p-2} mod p

One application is the computation of the inverse in a finite field; arithmetic
in finit fields (i.e. Galois fields) GF(p) is done by modulo p, and hence the
theorem holds for all integers a which are elements of a finite field GF(p)

On the other side it can prove a number being a prime.

the inverse property is defined by resulting in 1 mod p when multiplying
    a * a^-1 = 1 mod p

Euler's theorem generalizes Fermat's little theorem

Performing the exponentiation to obtain the inverse, is usually slower than using
the extended Euclidean algorithm. However, there are situations where it is
advantageous to use Fermat's Little Theorem, e.g., on smart cards or other
devices which have a hardware accelerator for fast exponentiation anyway. This is
not uncommon because many public-key algorithms require exponentiation, anyway.


example: obtaining the inverse

let p = 7 and a = 2, we can compute the inverse of a as
    a^{p-2} = 2^5 = 32 = 4 mod 7

so the inverse to a=2 in mod 7 is 4, prove
    2*4 mod 7 = 1 mod 7


source

[p. 167; Understanding Cryptography; Paar / Pelzel; Springer 2010]
"""


import sys

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)


def inverse(arg, prime):
    return (arg**(prime-2) % prime)

def prove(arg, invarg, prime):
    res = ((arg*invarg) % prime)
    if res != 1: die("FAILURE: the value provided as prime, was NOT a prime!!!")
    return res

### main ###
def main(argv=sys.argv[1:]):
    arg = 2 # find inverse a^{-1}
    prime = 7 # the prime
    if 2 == len(argv):
        if 0 < len(argv[0]) and 0 < len(argv[1]):
            try:
                arg=int(argv[0])
                prime=int(argv[1])
            except:
                die("usage: for finding the inverse of arg, do\n%s <arg> <prime>\nOR call without arguments"%sys.argv[0])
        print "remember that prime must be a prime!!!"

    print "arg = %d, prime = %d\n"%(arg, prime)

    ## get inverse
    invarg = inverse(arg, prime)

    ## result
    print "the inverse of %d in Z[%d] is: %d"%(arg, prime, invarg)

    ## prove
    print "\nprove:\n%d * %d = %d mod %d"%(arg, invarg, prove(arg,invarg,prime),prime)


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"

