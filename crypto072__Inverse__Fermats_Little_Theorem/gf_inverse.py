#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-September-02

Galois Field Inverse

Returns the inverse of a provided number within a specified Galois Field

Inverse
 * only values a that are coprime to the modulus m, have an inverse

 * by Fermat's Little Theorem
   a^{-1} = a^{p-2} mod p

 * by Euler's Theorem, this takes first to compute Phi(p)
   a^{-1} = a^{Phi(p)-1} mod p


example

4^{-1} mod 13 = 4^{12 - 1} mod 13 = 10
"""

import sys

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)

def gcd(r0, r1):
    ## return the greatest common divisor
    ## identified by the Euclidean Algorithm
    if r0 > r1: (a,b) = (r0, r1)
    else: (a,b) = (r1, r0)
    while b != 0:
        print "\tgcd(%d, %d)"%(a,b)
        tmp = b
        b = a % b
        a = tmp
    return a


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


### main ###
def main(argv=sys.argv[1:]):
    print "inverse by Fermat's Little Theorem"

    arg=4
    modulus=13
    ## get arguments, or set default values
    if 2 == len(argv):
        if 0 < len(argv[0]) and 0 < len(argv[1]):
            try:
                arg=int(argv[0])
                modulus=int(argv[1])
            except:
                die("usage: %s <arg> <modulus>\nOR call without arguments"%sys.argv[0] )
    if 1 >= modulus: die("FATAL: modulus must be greater than 0")

    ## apply finite field, sonce argument was outside
    if modulus <= arg: arg = arg%modulus

    print "arg = %d"%(arg)
    print "modulus = %d\n"%(modulus)

    ## check divisibility
    if gcd(arg, modulus) != 1:
        die("FATAL: inverse only exists if arg and modulus are coprime, %d divides into %d"%(arg, modulus))

    ## compute inverse by Fermat's Little Theorem
    #inv = arg**(modulus-2) % modulus # won't work with bigger intermediate results
    inv = square_and_multiply(arg, modulus-2, modulus)
    print "inverse: %d"%inv



### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
