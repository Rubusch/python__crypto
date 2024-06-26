#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-September-11

The least common multiple, lcm[] of two numbers
"""


import sys

### tools ###

def die(msg):
    if 0 < len(msg): print(msg)
    sys.exit(1)


def gcd(r0, r1):
    ## return the greatest common divisor
    ## identified by the Euclidean Algorithm
    if r0 > r1: (a,b) = (r0, r1)
    else: (a,b) = (r1, r0)
    while b != 0:
        tmp = b
        b = a % b
        a = tmp
    return a

def lcm(r0, r1):
    ## return the least common multiple
    print(f"lcm[{r0}; {r1}] = ({r0} * {r1}) / gcd({r0}; {r1}) = ", end="")
    return r0*r1/gcd(r0,r1)

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
                die(f"usage: {sys.argv[0]} <a> <b>\nOR call without arguments")

    if 0 >= a: die("FATAL: a has to be greater than 0")
    if 0 >= b: die("FATAL: b has to be greater than 0")

    print(f"a = {a}, b = {b}")
    print(f"What is the least common multiple of {a} and {b}?\n")
    print(lcm(a,b))


### start ###
if __name__ == '__main__':
    main()
print("READY.")
