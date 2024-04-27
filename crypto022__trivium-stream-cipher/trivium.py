#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Feb-28

# trivium is a stream cipher which combines three LFSR to obtain a safer PRNG
# trivium comprehends several phases:
# init
# warm up
# encryption
#
# here just the warum up fase, is depicted
#
# IV is 80 times '0'
# key is 80 times '0'
#
#
# IMPORTANT: this implementation is meant as an educational demonstration only


# TODO decryption          
# TODO work with real bit operations           
# TODO, adjust seed e.g. by clock          

import sys

IV = ['0' for i in range(80)] # TODO, adjust e.g. by clock
key = ['0' for i in range(80)] # TODO, adjust e.g. by clock as seed
A = []
B = []
C = []
shifterA=0
shifterB=0
shifterC=0


def die(msg):
    if 0 < len(msg): print(msg)
    sys.exit(1)

def printrivium():
    global A
    print("~~~ Clock Tick ~~~")
    print("A: ","".join(A))
    print("B: ","".join(B))
    print("C: ","".join(C))
    print("~~~ * ~~~\n")

def getpos(reg,idx,shifter):
    ## curiously, the indexes for trivium registers in literature start with '1'
    ## and not with '0'
    return reg[(idx-1+shifter)%len(reg)]

def setpos(reg,idx,val,shifter):
    reg[(idx-1+shifter)%len(reg)] = val

def incshifter(reg, shifter):
    return (shifter + 1)%len(reg)

def XOR(a, b):
    if a == b: return '0'
    else: return '1'

def AND(a, b):
    if a == '1' and b == '1': return '1'
    return '0'

def init():
    ## init A
    global A
    A += [i for i in IV]
    A += ['0' for i in range(93 - len(IV))]

    ## init B
    global B
    B += [k for k in key]
    B += ['0' for i in range(84 - len(key))]

    ## init C
    global C
    C += ['0' for i in range(108)]
    C += '1' # bit #109 - #111
    C += '1'
    C += '1'

def trivium():
    global shifterA
    global shifterB
    global shifterC

    ## 1. intermediate AND
    tmpA = AND(getpos(A, 91, shifterA), getpos(A, 92, shifterA))

    ## 2. combine for A
    outA = XOR(tmpA, getpos(A, 66, shifterA))
    outA = XOR(outA, getpos(A, 93, shifterA))
    shifterA = incshifter(A, shifterA)

    ## 3. prepare for B
    setpos(B, 1, XOR(getpos(B, 78, shifterB), outA), shifterB)

    ## 4. intermediate AND
    tmpB = AND(getpos(B, 82, shifterB), getpos(B, 83, shifterB))

    ## 5. combine for B
    outB = XOR(tmpB, getpos(B, 69, shifterB))
    outB = XOR(outB, getpos(B, 84, shifterB))
    shifterB = incshifter(B, shifterB)

    ## 6. prepare for C
    setpos(C, 1, XOR(getpos(C, 87, shifterC), outB), shifterC)

    ## 7. intermediate AND
    tmpC = AND(getpos(C, 109, shifterC), getpos(C, 110, shifterC))

    ## 8. combine for C
    outC = XOR(tmpC, getpos(C, 66, shifterC))
    outC = XOR(outC, getpos(C, 111, shifterC))
    shifterC = incshifter(C, shifterC)

    ## 9. result
    result = XOR(outA, outB)
    result = XOR(result, outC)

    ## 10. prepare A for next round
    setpos(A, 1, XOR(outC, getpos(A, 69, shifterA)), shifterA)

    ## DEBUG snapshot
#    printrivium()

    ## return iteration result bit - PRNG generated bit
    return result


def warmup():
    print("~~~ Warm-up Phase ~~~")
    clocktime = 4 * (len(A) + len(B) + len(C))
    for tick in range(clocktime):
        trivium()

def encrypt(binplaintext):
    print("~~~ Encryption Phase ~~~")
    print(f"plaintext:\t{binplaintext}")
    pseudorandom = []
    ciphertext = []
    for bit in binplaintext:
        s=trivium()

        ## encrypt by XORing the trivium pseudo-random bit s, with the idx bit of the plaintext
        c = XOR(s, bit)

        ## stream cipher
#        sys.stdout.softspace=0
#        print(c,)

        ## or batch...
        ciphertext += c

        ## DEBUG, print also the generated pseudo random bits
        pseudorandom += s
#    print "" # for streaming..
    print(f"PRNG:\t\t{pseudorandom}")
    print(f"ciphertext:\t{ciphertext}")

def decrypt():
# TODO
    pass



## args - the filenmae
def main(argv=sys.argv[1:]):
    ## check args
    # TODO

    ## init phase
    init()

    ## warm up phase
    warmup()

    ## encryption phase
    binplaintext = ['0','1','0','1','0','1','0','1','0','0','0','1','0','1','0','0']
    encrypt(binplaintext)

    printrivium()


### start ###
if __name__ == '__main__':
    main()

print("READY.")
