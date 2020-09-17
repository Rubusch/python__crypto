#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-May-19

Euler's Phi Function

Phi(m) returns the number of integers in Z[m] relatively prime to modulus m.

The theorem answers the question of how many numbers in a set are relatively
prime to m.

Let m have the following canonical factorization
    m = p[1]^{e1} * p[2]^{e2} * p[3]^{e3} * ... p[n]^{en}

where the p[i] are distinct prime numbers and e[i] are positive integers, then
    Phi(m) = Product[i=1; n]( p[i]^{ei} - pi^{ei-1} )

Euler's Phi function gives a fast and easy way of calculating the number of
coprimes, if the factorization of m is given, i.e. without Euler's Phi functin
running through all elements and computing the gcd is extremely slow if the
numbers are large, on the other side without having the factorization, Euler's
Phi can't be computed


example

let m = 240; the factorization of 240 in the canonical factorization form is
    m = 240 = 16 * 15 = 2^4 * 3 * 5 = p1^{e1} * p2^{e2} * p3^{e3}

there are 3 distinct prime factors, i.e. n = 3. The value for Euler's phi
function follows then as:
    Phi(m) = (2^4 - 2^3)(3^1 - 3^0)(5^1 - 5^0) = 8 * 2 * 4 = 64

that means, 64 integers in the range {0,1,...,239} are coprime to m = 240

it is obvious that this method is straightforward in comparison to compute all
240 gcds.


source

[p. 166; Understanding Cryptography; Paar / Pelzel; Springer 2010]
"""


import sys

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)


def factorize(m):
    ## for phi(m) generally omit factor '1', since (1^1 - 1^0) == 0
    print "generally we avoid factor '1'"
    factors = []
    exponents = []

    ## get factors of m (inclusively of m if it is a prime)
    val = m
    for num in range(2, m+1):
        if 0 == (val % num):
            factors.append(num)
            cnt = 0
            while 0 == val % num:
                cnt+=1
                val = val / num
            exponents.append(cnt)
            if num > val: break
    return (factors, exponents)


def phi(m, factors, exponents):
    ## compute Phi(m), the number of all integers in Z[m], relatively prime to m
    res = 1
    for idx in range(len(factors)):
        print "(%d^%d - %d^%d)"%(factors[idx], exponents[idx], factors[idx], (exponents[idx]-1)),
        res *= (factors[idx]**exponents[idx] - factors[idx]**(exponents[idx]-1) )
    print "="
    return res


### main ###
def main(argv=sys.argv[1:]):
    arg=14
    if 1 == len(argv):
        if 0 < len(argv[0]):
            try:
                arg=int(argv[0])
            except:
                die("usage: %s <arg>\nOR call without arguments"%sys.argv[0])

    ## input values
    print "arg = %d"%(arg)
    print "How many (co)primes exist in the galois field %d?\n" % arg

    ## find prim factors
    print "factorize(arg)"
    (factors, exponents) = factorize(arg)

    print "\tfactors:\t[%s]"%', '.join(map(str,factors))
    print "\texponents:\t[%s]"%', '.join(map(str,exponents))

    ## Phi(m)
    print "\nphi(%d) = "%(arg),
    ephi = phi(arg, factors, exponents)
    print ephi

    ## result
    print "\nZ[%d] contains %d integers that are relatively prime to m=%d"%(arg, ephi, arg)


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
