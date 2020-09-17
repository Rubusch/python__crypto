#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-September-11

The greatest common divisor, gcd() of two numbers
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
        print "gcd(%d, %d) = "%(a,b)
        tmp = b
        b = a % b
        a = tmp
    return a


### main ###
def main(argv=sys.argv[1:]):
    a=123
    b=321
    if 2 == len(argv):
        if 0 < len(argv[0]) and 0 < len(argv[1]):
            try:
                a=int(argv[0])
                b=int(argv[1])
            except:
                die("usage: %s <a> <b>\nOR call without arguments"%sys.argv[0])

    if 0 >= a: die("FATAL: a has to be greater than 0")
    if 0 >= b: die("FATAL: b has to be greater than 0")

    print "a = %d, b = %d"%(a,b)
    print "What is the greatest common divisor of %d and %d?\n" % (a,b)
    print gcd(a,b)
    print ""


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"

