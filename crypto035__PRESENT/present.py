#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Mar-17
#
# a lightweight block cipher, designed specifically for applications such as
# RFID tags or other pervasive computing applications that are extremely power
# or cost constrained
# [p. 78, Understanding Cryptography, Christof Paar, Jan Pelzl, 2010, Springer]
#
# PRESENT exists as PRESENT-80 or -128 with corresponding key length
# PRESENT is based on a substitution-permutation-network
#
# PRESENT algorithm authors
# Copyright (c) 2008 Christophe Oosterlynck (christophe.oosterlynck@gmail.com)
#         Philippe Teuwen (philippe.teuwen@nxp.com)
#
# IMPORTANT: this implementation is meant as an educational demonstration only

import sys   # sys.argv[]

### utils ###
def die(msg):
    if 0 < len(msg): print(msg)
    sys.exit(1)

class Present:
    def __init__(self, inputkey):
        self._sbox = [0xc,0x5,0x6,0xb,0x9,0x0,0xa,0xd,0x3,0xe,0xf,0x8,0x4,0x7,0x1,0x2]
        self._sbox_inv = [self._sbox.index(i) for i in range(len(self._sbox))]  ## python3

        self._permutation = [ 0,16,32,48, 1,17,33,49, 2,18,34,50, 3,19,35,51,
                              4,20,36,52, 5,21,37,53, 6,22,38,54, 7,23,39,55,
                              8,24,40,56, 9,25,41,57,10,26,42,58,11,27,43,59,
                             12,28,44,60,13,29,45,61,14,30,46,62,15,31,47,63]
        self._permutation_inv = [self._permutation.index(i) for i in range(len(self._permutation))]

        ## init all 31 keys once, then just go by index
        self._roundkeys = []

        self._generateRoundkeys80(inputkey)

    ## utilities
    def _checklength(self, text, length):
        if length != len(text):
            die("wrong blocksize passed, %d needed, %d passed"%(length,len(text)))

    def _xor(self, binlst1, binlst2):
        self._checklength( binlst1, len(binlst2))
        return [int(binlst1[idx])^int(binlst2[idx]) for idx in range(len(binlst1))]

    ## algorithm steps
    def _generateRoundkeys80(self, inputkey):
        key = inputkey
        for idx in range(1,32):
            ## cut out first 64 bit as round key
            self._roundkeys.append(key >> 16)

            ## left shift by 61 bit
            key = ((key & (2**19-1))<<61) + (key>>19)

            ## S(key[0])
            key = (self._sbox[key >> 76]  << 76) + (key & (2**76-1))

            ## key[60:65] XOR roundCounter
            key ^= idx << 15

    def _generateRoundkeys128(self, inputkeys):
        self._checklength(inputkey, 128)
        key = inputkey
        for idx in range(1,32):
            ## cut out first 64 bit as round key
            self._roundkeys.append(key >> 64)

            ## left shift by 61 bit
            key = ((key & (2**67-1))<<61) + (key>>67)

            ## S(key[0])
            key = (self._sbox[key >> 124]  << 124) + (self._sbox[(key>>120) & 0xf] << 120) + (key & (2**120-1))
            ## key[60:65] XOR roundCounter
            key ^= idx << 62

    def _addRoundKey(self, state, key):
        return state ^ key

    def _sBoxLayer(self, state):
        ret = 0
        for idx in range(16):
            ret += self._sbox[(state >> (idx*4)) & 0xf] << (idx*4)
        return ret

    def _sBoxLayer_dec(self, state):
        ret = 0
        for idx in range(16):
            ret += self._sbox_inv[(state >> (idx*4)) & 0xf] << (idx*4)
        return ret

    def _pLayer(self, state):
        ret = 0
        for idx in range(64):
            ret += ((state >> (idx)) & 0x1) << self._permutation[idx]
        return ret

    def _pLayer_dec(self, state):
        ret = 0
        for idx in range(64):
            ret += ((state >> (idx)) & 0x1) << self._permutation_inv[idx]
        return ret

    ## S-box tools
    def _sBox(self, fourbit):
        self._checklength(fourbit,4)
        return self._sbox[bin2dec("".join(map(str,fourbit)))]

    ## public interface
    def encrypt(self, plaintext):
        ## takes plaintext as string - just demonstrated with one block, to
        ## avoid padding issues
        ##
        ## string to number
        ## python3 string to hex :int formatting by means of binascii package
        import binascii
        state = int(binascii.hexlify(bytes(plaintext,"iso_8859_1")), 16) &0xffffffffffffffff  ## python3

        for idx in range(31-1):
            state = self._addRoundKey(state, self._roundkeys[idx])
            state = self._sBoxLayer(state)
            state = self._pLayer(state)
        ## last key
        state = self._addRoundKey(state, self._roundkeys[-1])
        return state

    def decrypt(self, ciphertext):
        state = ciphertext
        for idx in range(31-1):
            state = self._addRoundKey(state, self._roundkeys[-idx-1])
            state = self._pLayer_dec(state)
            state = self._sBoxLayer_dec(state)
        state = self._addRoundKey(state, self._roundkeys[0])

        ## conversion to string, simply prepends '0' in case of smaller blocks
        data = "%.16x" % (state)
        import binascii
        ret = bytes.fromhex(data).decode("iso_8859_1") ## python3

        return ret

### main ###
def main():
    blocksize = 64

    ## init some raw input key
    inputkey = 0xbbbb55555555eeeeffff
    print("initial key:")
    import os
    print(f"{inputkey:x}" + os.linesep) ## python3

    ## init the algorithm
    present = Present(inputkey)

    ## init some input text
    plaintext = "E também as memórias gloriosas" + os.linesep + \
        "Daqueles Reis, que foram dilatando" + os.linesep + \
        "A Fé, o Império, e as terras viciosas" + os.linesep +  \
        "De África e de Ásia andaram devastando;" + os.linesep + \
        "E aqueles, que por obras valerosas" + os.linesep + \
        "Se vão da lei da morte libertando;" + os.linesep + \
        "Cantando espalharei por toda parte," + os.linesep + \
        "Se a tanto me ajudar o engenho e arte." + os.linesep
    print("plaintext:")
    print(f"{plaintext}")

    ciphertext = []
    blocktext = ""
    for idx in range(len(plaintext)-1):
        blocktext += plaintext[idx]
        if (idx+1) % (blocksize/8) == 0:
            ciphertext.append(present.encrypt(blocktext))
            blocktext = ""
    blocktext += plaintext[idx+1]
    ciphertext.append(present.encrypt(blocktext))

    ## print result
    print("encrypted:")
    for item in ciphertext:
        print(f"{item:x}")
    print("")

    ## decrypt
    decryptedtext = ""
    for block in ciphertext:
        decryptedtext += present.decrypt(block)

    ## print result
    print("decrypted:")
    print(f"{decryptedtext}")

### start ###
if __name__ == '__main__':
    main()
print("READY.")
