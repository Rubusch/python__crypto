#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Mar-07
#
# initial phase of the DES algorithm, as also final phase

import sys   # sys.argv[]

class InitialPermutation():
    def __init__(self):
        self._blocksize = 64
        self._initial_permutation=[58,50,42,34,26,18,10, 2,
                                   60,52,44,36,28,20,12, 4,
                                   62,54,46,38,30,22,14, 6,
                                   64,56,48,40,32,24,16, 8,
                                   57,49,41,33,25,17, 9, 1,
                                   59,51,43,35,27,19,11, 3,
                                   61,53,45,37,29,21,13, 5,
                                   63,55,47,39,31,23,15, 7]
        self._final_permutation  =[40, 8,48,16,56,24,64,32,
                                   39, 7,47,15,55,23,63,31,
                                   38, 6,46,14,54,22,62,30,
                                   37, 5,45,13,53,21,61,29,
                                   36, 4,44,12,52,20,60,28,
                                   35, 3,43,11,51,19,59,27,
                                   34, 2,42,10,50,18,58,26,
                                   33, 1,41, 9,49,17,57,25]

    def _checklength(self, text):
        if self._blocksize != len(text):
            die("wrong blocksize passed, %d needed, %d passed"%(self._blocksize, len(text)))

    def _pick(self, text, position):
        return text[position-1]

    def initial_permute(self, text):
        ## Note that both permutations do not increase the security of DES at all
        self._checklength(text)
        return [self._pick(text,pos) for pos in self._initial_permutation]

    def final_permute(self, text):
        ## Note that both permutations do not increase the security of DES at all
        self._checklength(text)
        return [self._pick(text,pos) for pos in self._final_permutation]


### utils ###
def die(msg):
    if 0 < len(msg): print(msg)
    sys.exit(1)

def printo(text):
    for idx in range(len(text)):
        if 0 == idx%8:
            if idx != 0:
                print("")
        if int(text[idx]) < 10:
            print(f"{text[idx]} ", end="")
        else:
            print(f"{text[idx]} ", end="")
    print("\n")

### main ###
def main():
    ## init
    text = range(1,65)
    ip = InitialPermutation()
    print("initial:")
    printo(text)

    ## permute
    text = ip.initial_permute(text)
    print("ip:")
    printo(text)

    ## reverse
    text = ip.final_permute(text)
    print("ip-rev:")
    printo(text)

### start ###
if __name__ == '__main__':
    main()
print("READY.")
