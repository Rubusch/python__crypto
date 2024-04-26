#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Mar-07
#
# the key schedule generates the 56bit keys for DES
# DES uses 64bit key inputs, where the last bit is parity (so cut off), thus the
# de facto key length is 56 bit, which is not secure nowadays

import sys   # sys.argv[]

class KeySchedule():
    def __init__(self, inputkey):
        ## the key schedule derives 16 round keys k[i], each consisting of
        ## 48 bits, from original 56-bit key; another term for round key is
        ## subkey
        self._checklength(inputkey, 64)
        self._rawinputkey = inputkey

        self._pc1 = [57,49,41,33,25,17, 9, 1,
                     58,50,42,34,26,18,10, 2,
                     59,51,43,35,27,19,11, 3,
                     60,52,44,36,63,55,47,39,
                     31,23,15, 7,62,54,46,38,
                     30,22,14, 6,61,53,45,37,
                     29,21,13, 5,28,20,12, 4]

        self._pc2 = [14,17,11,24, 1, 5, 3,28,
                     15, 6,21,10,23,19,12, 4,
                     26, 8,16, 7,27,20,13, 2,
                     41,52,31,37,47,55,30,40,
                     51,45,33,48,44,49,39,56,
                     34,53,46,42,50,36,29,32]

        self._shiftrules = []
        shift_one = [1,2,9,16]
        for pos in range(1,17):
            if pos in shift_one:
                self._shiftrules.append(1)
            else:
                self._shiftrules.append(2)
        print("init shiftrules: %s"%", ".join(map(str,self._shiftrules)))

        ## initial 1. PC-1 permutation, once at beginning (stripping last 8-bit)
        self._inputkey = self.pc1_permutation(self._rawinputkey)
#        printx(self._inputkey)  

    def _checklength(self, text, length):
        if length != len(text):
            die("wrong blocksize passed, %d needed, %d passed"%(length,len(text)))

    def _pick(self, text, position):
        return text[position-1]

    def pc1_permutation(self, key):
        ## initial key permutation PC-1
        ## the 64-bit key is first reduced to 56 bits by ignoring every eighth
        ## bit, i.e. the parity bits are stripped in the initial PC-1
        ## permutation; again the parity bits certainly do not increase the key
        ## space! returns 56 bits
        self._checklength(key,64)
        return [self._pick(key,pos) for pos in self._pc1]

    def split(self, key):
        ## the resulting 56-bit key is split into two halves C[0] and D[0], and
        ## the actual key schedule starts
        return key[:28], key[28:]

    def shift_left(self, key, roundidx):
        ## the two 28-bit halves are cyclically shifted, i.e. rotated, left by
        ## one or two bit positions depending on the round i according to the
        ## rules; note that the rotation takes only place within either the left
        ## or the right half; the total number of rotations sum up to 28
        ## both halves are merged in this step
        self._checklength(key,28)
        shifter = self._shiftrules[roundidx]
        return key[shifter:] + key[:shifter]

    def shift_right(self, key, roundidx):
        ## same as left shift, but used for decryption; in decryption round 1,
        ## subkey 16 is needed; in round 2 subkey 15
        ## in decryption round 1 the key is not rotated
        ## in decryption rounds 2,9 and 16 the two halves are rotated right by
        ## one bit
        ## in the other rounds, 3,4,5,6,7,8,10,11,12,13,14 and 15 the two halves
        ## are rotated right by two bits
        self._checklength(key,28)
        if 0 == roundidx: return key
        shifter = self._shiftrules[roundidx]
        keylen = len(key)
        return key[(keylen-shifter):] + key[:(keylen-shifter)]

    def pc2_permutation(self, key):
        ## to derive the 48-bit round keys k[i], the two halves are permuted
        ## bitwise again with PC-2, which stands for "permutation choice 2"
        ## PC-2 permutes the 56 input bits coming from C[i] and D[i] and ignores
        ## 8 of them; each bit is used in approximately 14 of the 16 round keys
        self._checklength(key,56)
        ## permute
        return [self._pick(key,pos) for pos in self._pc2]

    def get_encrypt_key(self, roundidx):
#        print("\tencrypt")
        ## generate keys for encryption
        ##
        ## iterate for each key until the roundidx is reached (easier to
        ## understand decryption afterwards)
        key = self._inputkey
        for idx in range(roundidx+1):
            ## 2. split
            left, right = self.split(key)
#            printx(left,7)
#            printx(right,7)

            ## 3. shift left
            left = self.shift_left(left,idx)
#            printx(left,7)
            right = self.shift_left(right,idx)
#            printx(right,7)

            ## 4. merge keys
            key = left+right
#            printx(key)

            ## 5. PC-2 permutation
            roundkey = self.pc2_permutation(key)
#            printx(roundkey)

        return roundkey

    def get_decrypt_key(self, roundidx):
#        print("\tdecrypt")
        ## generate keys for decryption, by the property
        ## C[0] == C[16] and D[0] == D[16]
        ## the first key for decryption is the last key for encryption
        key = self._inputkey
        for idx in range(roundidx+1):
            ## 2. split
            left, right = self.split(key)
#            printx(left,7)
#            printx(right,7)

            ## 3. shift right
            left = self.shift_right(left,idx)
#            printx(left,7)
            right = self.shift_right(right,idx)
#            printx(right,7)

            ## 4. merge keys
            key = left+right
#            printx(key)

            ## 5. PC-2 permutation
            roundkey = self.pc2_permutation(key)
#            printx(roundkey)

        return roundkey

### utils ###
def die(msg):
    if 0 < len(msg): print(msg)
    sys.exit(1)

def bin2dec(binstr):
    ## generate decimal value from binary string
    val = 0
    for idx in reversed(range(len(binstr))):
        potence = 0
        if '1' == binstr[idx]:
            potence = 1
            for i in range(len(binstr)-1-idx):
                potence *= 2
        val += potence
    return val

def printx(text, cols=8):
    ## print in columns
    for idx in range(len(text)):
        if 0 == idx%cols:
            if idx != 0:
                print("")
        if int(text[idx]) < 10:
            print(f" {text[idx]} ",end="")
        else:
            print(f"{text[idx]} ",end="")
    print("\n")

def printhexlist(binlist):
    ## print binary value list, as hex values
    elem = ""
    vals = []
    for idx in range(len(binlist)):
        if 0 == idx%4 and idx != 0:
            vals.append( bin2dec(elem) )
            elem = ""
        elem += str(binlist[idx])
    vals.append(bin2dec(elem))
    res = [str(hex(v)).upper()[2:] for v in vals]
    print("%s"%" ".join(map(str,res)))

### main ###
def main():
    ## init
#    inputkey = [1 for i in range(64)] # all ones -> not useful
    inputkey = [0 for i in range(64)] # all zeros -> not useful
    for idx in range(32): inputkey[idx] = 1 # some ones
#    inputkey[0] = 1 # a single 1 at position 0

    keyschedule = KeySchedule(inputkey)

    print("initial:")
    printx(inputkey)

    ## generate encryption keys
    print("encryption:")
    for idx in range(16):
        print(f"round {(1+idx)}:")

        ## encryption
        keyidx = idx
        print("encrypt [keyidx %.2d]:"%(keyidx))
        key = keyschedule.get_encrypt_key(idx)
#       printx(key,6) # print binary

        print("    0x", end="")
        printhexlist(key) # print hex

        ## decryption
        keyidx = 15 - idx
        print("decrypt [keyidx %.2d]: 0x"%(keyidx))
        key = keyschedule.get_decrypt_key(15 - idx)
#        printx(key,6) # print binary

        print("    0x",end="")
        printhexlist(key) # print hex

        print("")

### start ###
if __name__ == '__main__':
    main()
print("READY.")
