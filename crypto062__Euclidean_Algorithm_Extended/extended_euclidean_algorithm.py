#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-May-19

Extended Euclidean Algorithm (EEA)

an extension to the Euclidean Algorithm, that computes besides the greatest
common divisor of integers a and b, the coefficients of Bézout's identity

    ax + by = gcd(a,b)

the algorihtm helps, when finding solutions for the diophantine equation

when
    ax + by mod x

is given; a is a dummy and ax becomes 0 when applying mod(x)
finally, when a and b are coprime, the gcd(a,b) = 1; which together forms
    1 mod a = gcd(a, b)

if this is the case, a, and be are coprime; now with
    ax + by mod x =
    by mod x = gcd(a, b)

we have a way to compute the inverse to b, which must be y



input: positive integers r0 and r1, with r0 > r1
output: gcd(r0, r1), as well as s and t (the Bézout coefficients), such that
    gcd(r0, r1) = s*r0 + t*r1

initialization:
    old_s = 1;   old_t = 0;   old_r = r0
    s     = 0;   t     = 1;   r     = r1

 - a and b are taken as coprime, since x is the modular multiplicative inverse of
   a modulo b, and y is the modular multiplicative inverse of b modulo a

 - Similarly, the polynomial extended Euclidean algorithm allows one to compute
   the multiplicative inverse in algebraic field extensions and, in particular in
   finite fields of non prime order.


algorithm:
    while r != 0:
        quot = old_r / r
        (old_r, r) = (r, old_r - quot * r)
        (old_s, s) = (s, old_s - quot * s)
        (old_t, t) = (t, old_t - quot * t)


source

http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
http://en.wikipedia.org/wiki/Polynomial_greatest_common_divisor#B.C3.A9zout.27s_identity_and_extended_GCD_algorithm
"""

import sys

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)

def extended_gcd(r0, r1):
    if r0 >= r1: (a,b) = (r0,r1)
    else: (a,b) = (r1,r0)

    print "\tinit"
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a

    print "\told_r = %d,\tr = %d"%(old_r, r)
    print "\told_s = %d,\ts = %d"%(old_s, s)
    print "\told_t = %d,\tt = %d"%(old_t, t)
    print ""

    while r != 0:
        quot = old_r / r
        (old_r, r) = (r, old_r - quot * r)
        (old_s, s) = (s, old_s - quot * s)
        (old_t, t) = (t, old_t - quot * t)

        print "\t\tanother round..."
        print "\t\tquot = %d"%quot
        print "\t\told_r = %d,\tr = %d"%(old_r, r)
        print "\t\told_s = %d,\ts = %d"%(old_s, s)
        print "\t\told_t = %d,\tt = %d"%(old_t, t)
        print ""

    print "Bézout coefficients: %d and %d"%(old_s, old_t)
    print "greatest common divisor: %d"%old_r
    print "quotients by the gcd: %d and %d"%(t, s)


### main ###
def main(argv=sys.argv[1:]):
    r0=27
    r1=21
    if 2 == len(argv):
        if 0 < len(argv[0]) and 0 < len(argv[1]):
            try:
                r0=int(argv[0])
                r1=int(argv[1])
            except:
                die("usage: %s <r0> <r1>\nOR call without arguments"%sys.argv[0])

    print "Given: r0 = %d; r1 = %d\n"%(r0,r1)
    print "What is x and y in\n\t%d*x + %d*y = gcd(%d, %d)"%(r0, r1, r0, r1)


    ## get the greatest common divisor
    extended_gcd(r0, r1)


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"

