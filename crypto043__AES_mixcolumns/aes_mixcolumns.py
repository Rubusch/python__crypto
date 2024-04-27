#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-Mar-19

the following demonstrates a trick that can be used for encryption and galois
field multiplication over mod P(x), where P(x) = x^8 + x^4 + x^3 + x + 1; with
factors of 1 (identity), 2, and 3 - seen as factor 2 and a galois addition of
identity (1)

since the inverse matrix, as used in AES decryption uses values greater than 3,
the above procedure is not helpful anymore and a full galois multiplication is
necessary

sources:
Book: Understanding Cryptography, Christof Paar, Jan Pelzl (c) Springer 2010

http://en.wikipedia.org/wiki/Advanced_Encryption_Standard
http://en.wikipedia.org/wiki/Rijndael_mix_columns
http://en.wikipedia.org/wiki/Rijndael_key_schedule

Chris Veness' AES implementation: http://www.movable-type.co.uk/scripts/aes.html
(c) 2005-2008 Chris Veness. Right of free use is granted for all
commercial or non-commercial use. No warranty of any form is offered.

functions from AES python port
(c) 2009 by Markus Birth <markus@birth-online.de>
"""

import sys

def die(msg):
    print(msg)
    sys.exit(1)

## Galois Multiplication
## addition = XOR operation
## multiplication = left shift, then modular reduction by P(x)
##
## here a is a 4-vector of the specific column,
## while b is a 4-vector of the same values x2, in case they are having a
## carry and would exceed the GF(2^8) limit, this is removed
## then, XORing the elements, either a signle a is taken,
## or a b, means 2a are taken, or
## a corresponding a and it's b, means 3a are taken, corresponding to the matrix
##
## Mix Columns operation, per column (here a is one column)
##
##         / 2 3 1 1 \     / a0 \
##        |  1 2 3 1  |   |  a1  |
##  C ==  |  1 1 2 3  | * |  a2  |
##         \ 3 1 1 2 /     \ a3 /
##
def mix_columns(s, Nb=4):
    for c in range(4):
        a = [0] * 4
        xaa = [0] * 4

        for idx in range(4):
            a[idx] = s[idx][c]
            xaa[idx] = s[idx][c]<<1 ^ 0x011b if s[idx][c]&0x80 else s[idx][c]<<1
            ## explicitly written
            # if s[i][c] & 0x80:
            #     xaa[i] = s[i][c]<<1 ^ 0x011b
            # else:
            #     xaa[i] = s[i][c]<<1

        print("a: [%s]"%", ".join("%.2x"%i for i in a))
        print("xaa: [%s]"%", ".join("%.2x"%i for i in xaa))

        s[0][c] = xaa[0] ^ a[1] ^ xaa[1] ^ a[2] ^ a[3]
        print(f"s[0][{c}]\t= xaa[0] ^ a[1] ^ xaa[1] ^ a[2] ^ a[3]\t= {xaa[0]:02x} ^ {a[1]:02x} ^ {xaa[1]:02x} ^ {a[2]:02x} ^ {a[3]:02x}\t= {s[0][c]:02x}")

        s[1][c] = a[0] ^ xaa[1] ^ a[2] ^ xaa[2] ^ a[3]
        print(f"s[1][{c}]\t= a[0] ^ xaa[1] ^ a[2] ^ xaa[2] ^ a[3]\t= {a[0]:02x} ^ {xaa[1]:02x} ^ {a[2]:02x} ^ {xaa[2]:02x} ^ {a[3]:02x}\t= {s[1][c]:02x}")

        s[2][c] = a[0] ^ a[1] ^ xaa[2] ^ a[3] ^ xaa[3]
        print(f"s[2][{c}]\t= a[0] ^ a[1] ^ xaa[2] ^ a[3] ^ xaa[3]\t= {a[0]:02x} ^ {a[1]:02x} ^ {xaa[2]:02x} ^ {a[3]:02x} ^ {xaa[3]:02x}\t= {s[2][c]:02x}")

        s[3][c] = a[0] ^ xaa[0] ^ a[1] ^ a[2] ^ xaa[3]
        print(f"s[3][{c}]\t= a[0] ^ xaa[0] ^ a[1] ^ a[2] ^ xaa[3]\t= {a[0]:02x} ^ {xaa[0]:02x} ^ {a[1]:02x} ^ {a[2]:02x} ^ {xaa[3]:02x}\t= {s[1][c]:02x}")

        print("")

    return s

def printstate(s):
    for row in range(4):
        for col in range(4):
            ## dec
            val = s[row][col]
#            if val <= 9: print(f" 0{val}",end="")
#            else: print(f" {val}",end="")
            ## hex
            print(f" {val:02x}",end="")
        print("")
    print("")

    print("text [state]:")
    for idx in range(16):
        print(f"{s[idx%4][idx//4]:02x}",end="")
    print("\n")

if __name__ == "__main__":
    Nb = 4
    ## incrementing number state
#    state = [ [0]*Nb, [0]*Nb, [0]*Nb, [0]*Nb ]
#    for i in range(4*Nb): state[i%4][i/4] = i

    ## example state
    state = [[0x63,0x09,0xcd,0xba],
             [0x53,0x60,0x70,0xca],
             [0xe0,0xe1,0xb7,0xd0],
             [0x8c,0x04,0x51,0xe7]]

    printstate(state)

    state = mix_columns(state)

    printstate(state)

    print("READY.")
