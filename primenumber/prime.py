#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

for n in range(2,20):
    for x in range(2,n):
        if n % x == 0:
            print n, 'equals', x, '*', n/x
            # usage of break - also continue and pass are possible!
            break
        else:
            # loop fell through, without finding a factor
            print n, 'is a prime number'

print "READY.\n"
