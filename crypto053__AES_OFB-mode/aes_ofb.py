#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-May-04

AES (american encryption standard)
128-bit block size
key lengths of 128 bit, 192 bit or 256 bit


OFB - Output Feedback Mode

       IV--->O   O<------+             +------>O   O<---IV
                /        |             |          /
               |         |             |         |
               V         |             |         V
            +-----+  +--------+   +--------+  +-----+
      k --->| e() |  | s[i-1] |   | s[i-1] |  | e() |
            +-----+  +--------+   +--------+  +-----+
               |         A             A         |
               |         |             |         |
               +---------+             +---------+
               |                                 |
               V                                 V
    x[i] ---> XOR -----------> y[i] ----------> XOR ---> x[i]

 * the OFB mode forms a synchronous stream cipher, as the key stream does not
   depend on the plain or ciphertext.
   [p. 130; Understanding Cryptography; Paar / Pelzl; Springer 2010]
 * turns a block cipher into a stream cipher
 * OFB does not know any explicit decryption process, it XORs the plaintext with
   the generated encrypted key a first time, which corresponds an encrpytion, and
   XORs it a second time to the encrypted text, which corresponds then a
   decryption
 * OFB has been critizized being limited to the number of key encryptions, after
   which it will cycle again and start with the first encrypted key
   [TODO source, Wikipedia? Nist? Paper?]
 * OFB is nondeterminant, hence, encryptig the same plaintext twice results in different ciphertexts
   [p. 130; Understanding Cryptography; Paar / Pelzel; Springer 2010]


theory

let e() be a block cipher of block size b; let x[i], y[i] and s[i] be bit strings
of length b; and IV be a nonce of length b

encryption (first block): s[1] = e[k](IV) and y[1] = s[1] XOR x[1]
encryption (general block): s[i] = e[k](s[i-1]) and y[i] = s[i] XOR x[i]   ; i>=2
decryption (first block): s[1] = e[k](IV) and x[1] = s[1] XOR y[1]
decryption (general block): s[i] = e[k](s[i-1]) and x[i] = s[i] XOR y[i]   ; i>=2


AES-OFB example

Key:        000102030405060708090a0b0c0d0e0f
IV:         0123456789abcdef0123456789abcdef
Plaintext:  00112233445566778899aabbccddeeff
Ciphertext: TODO                            


sources
TODO: paper???
http://en.wikipedia.org/wiki/Block_cipher_modes_of_operation
http://csrc.nist.gov/groups/ST/toolkit/BCM/index.html
"""

import sys

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)


### DEBUGGING ###

DEBUGGING = False
def DBG(msg):
    if DEBUGGING: print msg

DBG_PRINT_HEX = True
def tostring(val, nbits):
    ## push a leading dummy, to obtain leading '0's
    mask = 0x1 << nbits
    val += mask

    if DBG_PRINT_HEX:
        ## hexadecimal representation
        res = ("%#.x"%val)[:2] + ("%#.x"%val)[3:]
    else:
        ## remove the 1 from the mask and return as string w/ leading 0s
        res = bin(val)[:2] + bin(val)[3:]
    return res

### /DEBUGGING ###


class AES:
    def __init__(self, inputkey, keylength):
        ## blocksize
        self._blocksize = 128

        ## S-box
        self._sbox = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
                      [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
                      [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
                      [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
                      [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
                      [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
                      [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
                      [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
                      [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
                      [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
                      [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
                      [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
                      [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
                      [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
                      [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
                      [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]]

        self._inv_sbox = [[0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB],
                          [0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB],
                          [0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E],
                          [0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25],
                          [0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92],
                          [0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84],
                          [0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06],
                          [0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B],
                          [0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73],
                          [0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E],
                          [0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B],
                          [0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4],
                          [0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F],
                          [0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF],
                          [0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61],
                          [0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D]]

        ## diffusion layer - shift rows
        self._shift_rows = [0,5,10,15,4,9,14,3,8,13,2,7,12,1,6,11]
        self._inv_shift_rows = [self._shift_rows.index(idx) for idx in range(len(self._shift_rows))]

        ## diffusion layer - mix columns
        self._mix_columns__const_matrix = [[0x02,0x03,0x01,0x01],
                                           [0x01,0x02,0x03,0x01],
                                           [0x01,0x01,0x02,0x03],
                                           [0x03,0x01,0x01,0x02]]

        self._mix_columns__inv_const_matrix = [[0x0e,0x0b,0x0d,0x09],
                                               [0x09,0x0e,0x0b,0x0d],
                                               [0x0d,0x09,0x0e,0x0b],
                                               [0x0b,0x0d,0x09,0x0e]]

        ## diffusion layer - galois multiplication
        self._exp_box = [[0x01,0x03,0x05,0x0f,0x11,0x33,0x55,0xff,0x1a,0x2e,0x72,0x96,0xa1,0xf8,0x13,0x35],
                         [0x5f,0xe1,0x38,0x48,0xd8,0x73,0x95,0xa4,0xf7,0x02,0x06,0x0a,0x1e,0x22,0x66,0xaa],
                         [0xe5,0x34,0x5c,0xe4,0x37,0x59,0xeb,0x26,0x6a,0xbe,0xd9,0x70,0x90,0xab,0xe6,0x31],
                         [0x53,0xf5,0x04,0x0c,0x14,0x3c,0x44,0xcc,0x4f,0xd1,0x68,0xb8,0xd3,0x6e,0xb2,0xcd],
                         [0x4c,0xd4,0x67,0xa9,0xe0,0x3b,0x4d,0xd7,0x62,0xa6,0xf1,0x08,0x18,0x28,0x78,0x88],
                         [0x83,0x9e,0xb9,0xd0,0x6b,0xbd,0xdc,0x7f,0x81,0x98,0xb3,0xce,0x49,0xdb,0x76,0x9a],
                         [0xb5,0xc4,0x57,0xf9,0x10,0x30,0x50,0xf0,0x0b,0x1d,0x27,0x69,0xbb,0xd6,0x61,0xa3],
                         [0xfe,0x19,0x2b,0x7d,0x87,0x92,0xad,0xec,0x2f,0x71,0x93,0xae,0xe9,0x20,0x60,0xa0],
                         [0xfb,0x16,0x3a,0x4e,0xd2,0x6d,0xb7,0xc2,0x5d,0xe7,0x32,0x56,0xfa,0x15,0x3f,0x41],
                         [0xc3,0x5e,0xe2,0x3d,0x47,0xc9,0x40,0xc0,0x5b,0xed,0x2c,0x74,0x9c,0xbf,0xda,0x75],
                         [0x9f,0xba,0xd5,0x64,0xac,0xef,0x2a,0x7e,0x82,0x9d,0xbc,0xdf,0x7a,0x8e,0x89,0x80],
                         [0x9b,0xb6,0xc1,0x58,0xe8,0x23,0x65,0xaf,0xea,0x25,0x6f,0xb1,0xc8,0x43,0xc5,0x54],
                         [0xfc,0x1f,0x21,0x63,0xa5,0xf4,0x07,0x09,0x1b,0x2d,0x77,0x99,0xb0,0xcb,0x46,0xca],
                         [0x45,0xcf,0x4a,0xde,0x79,0x8b,0x86,0x91,0xa8,0xe3,0x3e,0x42,0xc6,0x51,0xf3,0x0e],
                         [0x12,0x36,0x5a,0xee,0x29,0x7b,0x8d,0x8c,0x8f,0x8a,0x85,0x94,0xa7,0xf2,0x0d,0x17],
                         [0x39,0x4b,0xdd,0x7c,0x84,0x97,0xa2,0xfd,0x1c,0x24,0x6c,0xb4,0xc7,0x52,0xf6,0x01]]

        self._ln_box  = [[0x00,0x00,0x19,0x01,0x32,0x02,0x1a,0xc6,0x4b,0xc7,0x1b,0x68,0x33,0xee,0xdf,0x03],
                         [0x64,0x04,0xe0,0x0e,0x34,0x8d,0x81,0xef,0x4c,0x71,0x08,0xc8,0xf8,0x69,0x1c,0xc1],
                         [0x7d,0xc2,0x1d,0xb5,0xf9,0xb9,0x27,0x6a,0x4d,0xe4,0xa6,0x72,0x9a,0xc9,0x09,0x78],
                         [0x65,0x2f,0x8a,0x05,0x21,0x0f,0xe1,0x24,0x12,0xf0,0x82,0x45,0x35,0x93,0xda,0x8e],
                         [0x96,0x8f,0xdb,0xbd,0x36,0xd0,0xce,0x94,0x13,0x5c,0xd2,0xf1,0x40,0x46,0x83,0x38],
                         [0x66,0xdd,0xfd,0x30,0xbf,0x06,0x8b,0x62,0xb3,0x25,0xe2,0x98,0x22,0x88,0x91,0x10],
                         [0x7e,0x6e,0x48,0xc3,0xa3,0xb6,0x1e,0x42,0x3a,0x6b,0x28,0x54,0xfa,0x85,0x3d,0xba],
                         [0x2b,0x79,0x0a,0x15,0x9b,0x9f,0x5e,0xca,0x4e,0xd4,0xac,0xe5,0xf3,0x73,0xa7,0x57],
                         [0xaf,0x58,0xa8,0x50,0xf4,0xea,0xd6,0x74,0x4f,0xae,0xe9,0xd5,0xe7,0xe6,0xad,0xe8],
                         [0x2c,0xd7,0x75,0x7a,0xeb,0x16,0x0b,0xf5,0x59,0xcb,0x5f,0xb0,0x9c,0xa9,0x51,0xa0],
                         [0x7f,0x0c,0xf6,0x6f,0x17,0xc4,0x49,0xec,0xd8,0x43,0x1f,0x2d,0xa4,0x76,0x7b,0xb7],
                         [0xcc,0xbb,0x3e,0x5a,0xfb,0x60,0xb1,0x86,0x3b,0x52,0xa1,0x6c,0xaa,0x55,0x29,0x9d],
                         [0x97,0xb2,0x87,0x90,0x61,0xbe,0xdc,0xfc,0xbc,0x95,0xcf,0xcd,0x37,0x3f,0x5b,0xd1],
                         [0x53,0x39,0x84,0x3c,0x41,0xa2,0x6d,0x47,0x14,0x2a,0x9e,0x5d,0x56,0xf2,0xd3,0xab],
                         [0x44,0x11,0x92,0xd9,0x23,0x20,0x2e,0x89,0xb4,0x7c,0xb8,0x26,0x77,0x99,0xe3,0xa5],
                         [0x67,0x4a,0xed,0xde,0xc5,0x31,0xfe,0x18,0x0d,0x63,0x8c,0x80,0xc0,0xf7,0x70,0x07]]

        ## round coefficients
        ## source: http://en.wikipedia.org/wiki/Rijndael_key_schedule
        ##
        ## basically just generated by doubling (left shifting) and applying
        ## mod P(x), where P(x) = x^8 + x^4 + x^3 + x + 1
        ## only the first some are actually used!!!
        self._rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

        ## key schedule
        self._keylength = keylength
        self._rounds = 10
        if 192 == self._keylength: self._rounds = 12
        elif 256 == self._keylength: self._rounds = 14
        self._keys = self._key_schedule(inputkey, self._keylength)


    ## utilities

    def _gfmult(self,vala, valb):
        ## Galois Field Multiplication
        ##
        ## implementation of a single multiplication under mod P(x)
        ## this implementation uses the ln and exp table
        if vala != 0 and valb != 0:
            vala = self._tablelookup(self._ln_box,vala)
            valb = self._tablelookup(self._ln_box,valb)
            res = vala+valb
            res = res % 0xff
            res = self._tablelookup(self._exp_box,res)
            return res
        else:
            return 0x0

    def _tablelookup(self,table,index,offset=0):
        ## params:
        ## table = table to look up content
        ## index = a 0xff value, where 0xf0 describes 16 row indexes and 0x0f
        ## 16 column indexes
        ##
        ## returns table value by the provided row and column indexes
        row = 0xf & (index >>(offset+4))
        if offset > 0:
            col = 0xf & (index >> offset)
        else:
            col = 0xf & index
        return table[row][col]

    def _getnth(self, hexlst, nth, size):
        ## params:
        ## hexlst = a hex value, which serves as list of byte values
        ## nth = index of a specific byte in hexlst
        ## size = the full size of the hexlst
        ##
        ## return the nth 8-bit number, contained in the hex list (a number)
        ## where nth is an index, starting with 0
        return ((hexlst >> (size - (nth+1)*8)) & 0xff)

    def _append(self, hexlst, val, nbytes=1):
        ## appends an 8-bit hex val to a hex list (a number) of such values
        ## and returns it
        ##
        ## params:
        ## hexlst = a hex value, which serves as list of byte values
        ## val = a value e.g. as hex number to be appended
        ## nbytes = the number of bytes to be appended, the size of val
        return ((hexlst << (8*nbytes))|val)

    def _cutlastbits(self, hexlst, nbits):
        ## cuts and returns the last nbits out of a provided value hexlst
        ##
        ## params:
        ## hexlist = the value
        ## nbits = number of last bits to cut out and return
        mask = 0x0
        for i in range(nbits):
            mask = mask <<1 | 0x1
        return hexlst & mask

    ## methods
    def _key_schedule(self, password, keylength):
        ## key expansion for AES
        ##
        ## at instatiation of the cipher class this generates all subkeys and
        ## initializes a list of subkeys which then is accessible by the round
        ## index
        ##
        ## params:
        ## password = the initial key
        ## keylength = the specific applied key length, for AES this may be
        ## 128 bit, 192 bit or 256 bit
        ##
        ## init, e.g. keylength 128 and password:
        ## 0x000102030405060708090a0b0c0d0e0f
        Nb = 4
        Nk = keylength / 32
        Nr = Nk + 6 # rounds keys
        words = []
        words = [0] * Nb * (Nr+1)
        temp = 0x0

        ## split initial key into four pieces
        ## 0x00010203 0x04050607 0x08090a0b 0x0c0d0e0f
        for idx in range(Nk):
            words[idx] = (password >>(keylength - (idx+1) * 32)) & 0xffffffff

        for idx in range(Nk, Nb*(Nr+1)): # round 4. -> 44. (128-bit)
            words[idx] = 0x0

            ## init temp to the last quadruple
            temp = words[idx-1]

            nextword = 0x0
            if idx % Nk == 0:
                ## first word block, rotate and substitute

                ## rotate word
                swap = (temp >>24) & 0xff
                temp = ((temp <<8) & 0xffffffff)|swap
                ## temp: 0x0d0e0f0c

                ## s-boxing and r-coefficient
                for sub in range(4):
                    ## s-boxing
                    ch = self._tablelookup(self._sbox, temp, (32-8*(sub+1)))
                    ## ch: d7

                    ## the 0. char, XOR against round coefficient
                    if sub == 0: ch ^= self._rcon[idx/Nk -1]
                    ## ch: d7

                    ## append new character
                    nextword = self._append(nextword, ch)
                    ## swap: d6

                temp = nextword
                ## temp: 0xd6ab76fe

            elif Nk > 6 and idx % Nk == 4:
                ## keylength above 128-bit, additional substitutions
                for sub in range(4):
                    ## s-boxing
                    ch = self._tablelookup(self._sbox, temp, (32-8*(sub+1)))

                    ## append new character
                    nextword = self._append(nextword, ch)

                temp = nextword
                ## temp: 0xd6ab76fe

            ## assign the preceeding word, XORed against the current temp
            words[idx] = words[idx-Nk] ^ temp
        return words

    def _add_round_key(self, state, rnd):
        ## add a round key
        ##
        ## params:
        ## state = current state, the text to be encrypted or decrypted as hex
        ##         value
        ## rnd = current round index
        key = self._keys[rnd*4]
        key = self._append(key, self._keys[rnd*4+1], 4)
        key = self._append(key, self._keys[rnd*4+2], 4)
        key = self._append(key, self._keys[rnd*4+3], 4)
        ret = key ^ state
        print "R%d (key = %s)\t= %#x" % (rnd,tostring(key, self._keylength),ret)
        return ret

    def _substitution_layer__sub_bytes(self, state, table):
        ## substitution per 8-bit values
        ##
        ## params:
        ## state = current state, the text to be encrypted or decrypted as hex
        ##         value
        ## table = the substitution matrix either for encryption (self._sbox) or
        ##         decryption (self._inv_sbox)
        hexlst = 0x0
        for idx in range(self._blocksize/8):
            ch = self._getnth(state, idx, self._blocksize)
            val = self._tablelookup(table, ch)
            hexlst = self._append(hexlst, val)
        return hexlst

    def _diffusion_layer__shift_rows(self, state, table):
        ## first operation in the diffusion layer on 8-bit values
        ##
        ## params:
        ## state = current state, the text to be encrypted or decrypted as hex
        ##         value
        ## table = the specific shift rows mapping table, for encryption
        ##         (self._shift_rows) or decryption (self._inv_shift_rows)
        hexlst = 0x0
        for idx in range(self._blocksize/8):
            hexlst = self._append(hexlst, self._getnth(state, table[idx], self._blocksize))
        return hexlst

## not used here, just code snippet
    def _diffusion_layer__mix_column_TRICK(self, state):
        ## major diffusion element on 8-bit values
        ##
        ## matrix-matrix-multiplication in GF(2^8)
        ## with P(x) = x^8 + x^4 + x^3 + x + 1
        ##
        ## operation as depicted
        ##
        ##  / c0 \      / 2 3 1 1 \     / b0 \
        ## |  c1  |    |  1 2 3 1  |   |  b1  |
        ## |  c2  | == |  1 1 2 3  | * |  b2  |
        ##  \ c3 /      \ 3 1 1 2 /     \ b3 /
        ##
        ## where B = state/input, and C = states/output
        ##
        ## the here implemented mix-columns avoids dealing with exp and ln
        ## tables for calculation a generic GF-multiplication, but takes
        ## advantage of the fact, that multiplying by 1 results in the identity,
        ## and by 2 is actually a left shift mod P(x) operation; multiplying by
        ## 3 then is a combination of both; any further operation as used for
        ## the inverse matrix at decryption, then, is not as easy and will need
        ## a generic GF-multiplication implementation, as also implemented here
        ##
        ## Galois Field restrictions:
        ## * Addition: XOR operation
        ## * Multiplication: leftshift, with modular reduction to P(x)
        ##
        ## in specific:
        ## * the factor 1 will multiply by identity, means just take the b-value
        ## * the factor 2 is a doubling (leftshift by 1) and modular reduction
        ##   here named b vector
        ## * the factor 3 is a XOR combination of 1 and 2, since 3x = x + 2x,
        ##   here named bb and b vector
        ## * this does NOT WORK FOR DECRIPTION
        ##
        ## params:
        ## state = current state, the text to be encrypted as hex value
        hexlst = 0x0
        for col in range(len(self._mix_columns__const_matrix[0])):
            b_vec = [0]*4
            bb_vec = [0]*4
            for row in range(len(self._mix_columns__const_matrix)):
                ## 1. left shift by factor for each vector value
                ## 2. XOR the shifted vector results
                b_vec[row] = self._getnth(state, row+(4*col), self._blocksize)

                ## write doubled b-values into bb-vec,
                ## GF(2^8), perform modular reduction by mod P(x), which is
                ## P(x) = x^8 + x^4 + x^3 + x + 1
                ##
                ## if b_vec[row] & 0x80:
                ##     bb_vec[row] = b_vec[row] <<1 ^ 0x11b
                ## else:
                ##     bb_vec[row] = b_vec[row] <<1
                ##
                ## brief implementation of the above
                bb_vec[row] = b_vec[row] <<1 ^ 0x11b if b_vec[row] & 0x80 else b_vec[row] <<1
                ##
            hexlst = self._append(hexlst, (bb_vec[0] ^  b_vec[1] ^ bb_vec[1] ^  b_vec[2] ^  b_vec[3]))
            hexlst = self._append(hexlst, ( b_vec[0] ^ bb_vec[1] ^  b_vec[2] ^ bb_vec[2] ^  b_vec[3]))
            hexlst = self._append(hexlst, ( b_vec[0] ^  b_vec[1] ^ bb_vec[2] ^  b_vec[3] ^ bb_vec[3]))
            hexlst = self._append(hexlst, ( b_vec[0] ^ bb_vec[0] ^  b_vec[1] ^  b_vec[2] ^ bb_vec[3]))
        return hexlst

    def _diffusion_layer__mix_column(self, state, table):
        ## a generic mix-columns, taking advantage of a generic
        ## GF-multiplication implementation; depending on the passed table,
        ## either encryption or decryption is performed
        ##
        ## properties/operations in the Galois Field:
        ## '+' corresponds to XOR, thus no difference between '+' and '-'
        ## '*' correspondes to a multiplication, then mod P(x)
        ##
        ## the polynomial expression can be written equally in binary form, e.g.
        ## P(x) = x^8 + x^4 + x^3 + x + 1, then corresponds to
        ##      = 100011011 or 0x11b
        ##
        ## params:
        ## state = current state (hex value) of the cipher text or plaintext
        ## table = either the constant encryption table
        ##         (self._mix_columns__const_matrix) or its inverse for
        ##         decryption (self._mix_columns__inv_const_matrix)
        res = 0x0
        for col in range(4):
            for row in range(4):
                arr = []
                for ccol in range(len(table[0])):
                    vala = state >>(120 - ((col*4 + ccol)*8)) & 0xff
                    arr.append(self._gfmult(vala, table[row][ccol]))
                val = reduce(lambda x,y: x^y, arr)
                res = self._append(res, val)
        return res


    ## public interface

    def encrypt_ofb(self, plaintext, blocksize, IV):
        ## params:
        ## plaintext = the plaintext as string
        ## blocksize = the blocksize of the algorithm
        ## IV = the initiation vector, size 128 bit

        ## asking for blocksize is bogus here, though, it is left on purpose
        ## to stress the point that AES has always 128bit block size!
        if 128 != blocksize: die("AES is defined for only 128bit blocksize")
        ## blocking
        size = len(plaintext) * 8
        nblocks = size / blocksize
        blockbytes = blocksize / 8
        cipherblocks = []
        curr_block = 0x0
        for b in range(nblocks+1):
            ## convert textblock into hex
            textblock = plaintext[(b*blockbytes):(b*blockbytes+blockbytes)]
            if 0 == len(textblock): break
            hexblock = self._cutlastbits(int(textblock.encode('hex'),16), blocksize)
            ## get last block or IV for the first
            if 0 == b: last_block = IV
            else: last_block = curr_block
            ## XOR next plaintext block against last ciphered text block
            curr_block = self.encrypt(last_block, ishex=True)
            ## encrypt - it can be sent, and then decrypted directly (stream)
            cipherblocks.append(hexblock ^ curr_block)
        return cipherblocks


    def encrypt(self, plaintext, ishex=False, npaddingbits=0):
        ## params
        ## plaintext = the plaintext as string or as hex number
        ## ishex = if the plaintext was a hex number (True)

        ## init
        if ishex: state = plaintext
        else: state = int(plaintext.encode('hex'),16) & 0xffffffffffffffffffffffffffffffff
        DBG( "\nENCRYPTION\n\nplaintext: \t%s"%tostring(state, 128) )

        ## padding for broken blocks
        if 0 < npaddingbits:
            DBG( "padding (before): \t%s"%tostring(state, 128))
            padding = 1 <<(npaddingbits-1)
            state = (state <<(npaddingbits)) | padding
            DBG( "padding (after): \t%s"%tostring(state, 128))

        ## round 0
        state = self._add_round_key(state, 0)
        DBG( "add key: \t%s\n"%tostring(state, 128) )

        for rnd in range(self._rounds-1):
            state = self._substitution_layer__sub_bytes(state, self._sbox)
            DBG( "substitute: \t\t%s"%tostring(state, 128))

            state = self._diffusion_layer__shift_rows(state, self._shift_rows)
            DBG( "shift rows: \t\t%s"%tostring(state, 128))

            ## alternative implementation
#            state = self._diffusion_layer__mix_column_TRICK(state) ## KEEP!
            ## more generic implementation
            state = self._diffusion_layer__mix_column(state, self._mix_columns__const_matrix)
            ## /alternative implementation
            DBG( "mix column: \t\t%s"%tostring(state, 128) )

            state = self._add_round_key(state, rnd+1)
            DBG( "add key: \t\t%s\n"%tostring(state, 128) )

        ## round n
        state = self._substitution_layer__sub_bytes(state, self._sbox)
        DBG( "substitute: \t%s"%tostring(state, 128) )

        state = self._diffusion_layer__shift_rows(state, self._shift_rows)
        DBG( "shift rows: \t%s"%tostring(state, 128) )

        state = self._add_round_key(state, self._rounds)
        DBG( "add key: \t%s\n"%tostring(state, 128) )

        print ""
        return state


    def decrypt_ofb(self, cipherblocks, blocksize, IV):
        ## params:
        ## plaintext = the plaintext as string
        ## blocksize = the blocksize of the algorithm
        ## IV = the initiation vector, size 128 bit
        decryptedtext = ""
        last_block = 0x0
        curr_block = 0x0
        ## AES-OFB turns the block cipher AES into a stream cipher
        ## it also actually only needs the encrypt function
        for b in range(len(cipherblocks)):
            if b == 0: last_block = IV
            else: last_block = curr_block
            ## decrypt last block
            curr_block = self.encrypt(last_block, ishex=True)
            ## XOR decrypted text block against forelast encrypted block
            decryptedblock = cipherblocks[b] ^ curr_block
            ## convert to string
            data = "%x"%decryptedblock
            decryptedtext += ''.join(chr(int(data[i:i+2], 16)) for i in range(0, len(data), 2))
        return decryptedtext


    def decrypt(self, ciphertext, ashex=False, ispadded=False, asnum=False):
        ## params:
        ## ciphertext = the ciphertext as hex number
        ## ashex = shall the output be a hex number, or a string?
        ## ispadded = is ciphertext, or does it contain a padding block?

        state = ciphertext
        DBG("\n\nDECRYPTION\n\ninput: %s"%tostring(state, 128))

        ## round n
        state = self._add_round_key(state, self._rounds)
        DBG( "add key: \t%s"%tostring(state, 128) )

        state = self._diffusion_layer__shift_rows(state, self._inv_shift_rows)
        DBG( "shift rows: \t%s"%tostring(state, 128) )

        state = self._substitution_layer__sub_bytes(state, self._inv_sbox)
        DBG( "substitute: \t%s\n"%tostring(state, 128) )

        for rnd in range(self._rounds-2,-1,-1):
            state = self._add_round_key(state, rnd+1)
            DBG( "add key: \t\t%s"%tostring(state, 128) )

            state = self._diffusion_layer__mix_column(state, self._mix_columns__inv_const_matrix)
            DBG( "mix column: \t\t%s"%tostring(state, 128) )

            state = self._diffusion_layer__shift_rows(state, self._inv_shift_rows)
            DBG( "shift rows: \t\t%s"%tostring(state, 128) )

            state = self._substitution_layer__sub_bytes(state, self._inv_sbox)
            DBG( "substitute: \t\t%s"%tostring(state, 128) )
            DBG("")

        state = self._add_round_key(state, 0)
        DBG( "add key: \t%#.32x"%state )

        DBG( "\nfinal result: %s\n"%tostring(state, 128) )
        print ""

        if ispadded:
            ## cut off padding '0's
            while 0 == state & 0b1:
                state = state >>1
            ## cut off padding '1'
            state = state>>1

        ## as number
        if asnum: return state

        ## convert to string
        data = "%x"%state
        if ashex:
            ## append trailing zeros, for string encoding, the string is reduced
            ## to the significant digits implicitely
            while len(data) < 32: data += "0"
            return data
        return ''.join(chr(int(data[i:i+2], 16)) for i in range(0, len(data), 2))



### main ###
def main(argv=sys.argv[1:]):
## to just use it with hex numbers and a single block, the class can be
## instrumented the following way
#    inputkey = 0x2b7e151628aed2a6abf7158809cf4f3c
#    keylength = 128
#    aes = AES(inputkey, keylength)
#    blocktext = 0x01000000000000000000000000000000
#    ciphertext = aes.encrypt(blocktext, ishex=True)
#    print "ciphered: %s"%tostring( ciphertext, 128)
#    die("STOP")

    ## AES has fixed block size of 128 bit
    blocksize = 128
    inputkey = 0x0
    plaintext = ""
    keylength = 128

    if len(argv) > 0:
        ## offer encryption by command line argument
        try:
            keylength = int(argv[0])
            inputkey = int(argv[1],16)
            plaintext = argv[2]
        except:
            die('usage: either w/o arguments, or as follows\n$ %s <keylength> '\
                    '<inputkey> "<plaintext>"\ne.g.\n$ %s %d %s "%s"' \
                    %(sys.argv[0],sys.argv[0],128, \
                          "0x000102030405060708090a0b0c0d0e0f", \
                          "As Lusíadas"))
    else:
        ## init some raw input key example
        inputkey = 0x000102030405060708090a0b0c0d0e0f
        ## init some input text example
        plaintext = "Vós, tenro e novo ramo florescente\n" \
            "De uma árvore de Cristo mais amada\n" \
            "Que nenhuma nascida no Ocidente,\n" \
            "Cesárea ou Cristianíssima chamada;\n" \
            "(Vede-o no vosso escudo, que presente\n" \
            "Vos amostra a vitória já passada,\n" \
            "Na qual vos deu por armas, e deixou\n" \
            "As que Ele para si na Cruz tomou)"

    print "initial key:\n%#.32x, key length %d, block size %d\n" % (inputkey, keylength, blocksize)

    print "plaintext:"
    print "%s\n" % plaintext

    ## init the algorithm
    aes_encrypter = AES(inputkey, keylength)

    ## blocks
    IV = 0x0123456789abcdef0123456789abcdef
    ciphertext = aes_encrypter.encrypt_ofb(plaintext, blocksize, IV)

    ## print result
    print "encrypted:"
    for item in ciphertext:
        print "%s"%tostring(item, 128)
    print "\n"

    ## init the algorithm
    aes_decrypter = AES(inputkey, keylength)

    ## decrypt
    decryptedtext = aes_decrypter.decrypt_ofb(ciphertext, blocksize, IV)

    ## print result
    print "decrypted:"
    print "%s\n" % decryptedtext

### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
