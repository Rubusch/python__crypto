#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Mar-07
#
# DES is a symmetric block cipher cipher, it takes 64-bit blocks and encrypts
# with 56-bit keylength; since 1990 the algorithm is considered as being too
# weak against exhaustive key search attacks with just 56-bit keylength;
# further the origin and specific design of the S-boxes is not fully published,
# thus there might still be a chance to contain backdoors by designers
#
# this implementation is working on strings, which makes it easier readable or
# better to experience the algorithm, a better implementation would be to code
# it with hex numbers and bit operations directly
#
# IMPORTANT: this implementation is meant as an educational demonstration only

## additional settings #########################################################

## print debug output
DBG_OUTPUT = False

## debug output in hex or bin (False)
DBG_PRINT_HEX = True
################################################################################

import sys   # sys.exit()

### utils ###
def die(msg):
    if 0 < len(msg): print(msg)
    sys.exit(1)

def DBG(msg):
    if DBG_OUTPUT:
        print(msg)

def tostring(val, nbits):
    ## binary representation
    mask = 0x1 << nbits
    val += mask

    if DBG_PRINT_HEX:
        ## hexadecimal representation
        res = ("%#.x"%val)[:2] + ("%#.x"%val)[3:]
    else:
        ## remove the 1 from the mask and return as string w/ leading 0s
        res = bin(val)[:2] + bin(val)[3:]
    return res

class InitialPermutation():
    def __init__(self):
        self._blocksize = 64
        ## starts with 1
        self.initial_permutation=[58,50,42,34,
                                   26,18,10, 2,
                                   60,52,44,36,
                                   28,20,12, 4,
                                   62,54,46,38,
                                   30,22,14, 6,
                                   64,56,48,40,
                                   32,24,16, 8,
                                   57,49,41,33,
                                   25,17, 9, 1,
                                   59,51,43,35,
                                   27,19,11, 3,
                                   61,53,45,37,
                                   29,21,13, 5,
                                   63,55,47,39,
                                   31,23,15, 7]

        ## starts with 1
        self.final_permutation  =[40, 8,48,16,
                                   56,24,64,32,
                                   39, 7,47,15,
                                   55,23,63,31,
                                   38, 6,46,14,
                                   54,22,62,30,
                                   37, 5,45,13,
                                   53,21,61,29,
                                   36, 4,44,12,
                                   52,20,60,28,
                                   35, 3,43,11,
                                   51,19,59,27,
                                   34, 2,42,10,
                                   50,18,58,26,
                                   33, 1,41, 9,
                                   49,17,57,25]

class KeySchedule():
    def __init__(self, inputkey):

        ## starts with 1
        self._pc1 = [57,49,41,33,
                     25,17, 9, 1,
                     58,50,42,34,
                     26,18,10, 2,
                     59,51,43,35,
                     27,19,11, 3,
                     60,52,44,36,
                     63,55,47,39,
                     31,23,15, 7,
                     62,54,46,38,
                     30,22,14, 6,
                     61,53,45,37,
                     29,21,13, 5,
                     28,20,12, 4]

        ## starts with 1
        self._pc2 = [14,17,11,24,
                      1, 5, 3,28,
                     15, 6,21,10,
                     23,19,12, 4,
                     26, 8,16, 7,
                     27,20,13, 2,
                     41,52,31,37,
                     47,55,30,40,
                     51,45,33,48,
                     44,49,39,56,
                     34,53,46,42,
                     50,36,29,32]

        self._shiftrules = []
        shift_one = [1,2,9,16]
        for pos in range(1,17):
            if pos in shift_one:
                self._shiftrules.append(1)
            else:
                self._shiftrules.append(2)
        DBG("key schedule: init shiftrules: %s"%", ".join(map(str,self._shiftrules)))

        ## key expansion
        ##
        ## the key schedule derives 16 round keys k[i], each consisting of
        ## 48 bits, from original 56-bit key; another term for round key is
        ## subkey
        self.encryptkeys = self.encrypt_key_expansion(inputkey)

        ## decryption keys are the same as encyrption keys, but also can be gene-
        ## rated by using a right shift instead of a left shift, so here is pre-
        ## sented how to generate them freshly, instead of accessing the already
        ## generated keys with the corresponding reverted index which of course
        ## would be the efficient way how to do it
        self.decryptkeys = self.decrypt_key_expansion(inputkey)

    def encrypt_key_expansion(self, inputkey):
        return self._key_expansion(inputkey, True)

    def decrypt_key_expansion(self, inputkey):
        return self._key_expansion(inputkey, False)

    def _key_expansion(self, inputkey, isencrypt):
        DBG("\nkey schedule: encryption key expansion")
        DBG("key schedule: init key %s"%tostring(inputkey, 64))
        ## initial 1. PC-1 permutation, once at beginning (stripping last 8-bit)
        ##
        ## the 64-bit key is first reduced to 56 bits by ignoring every eighth
        ## bit, i.e. the parity bits are stripped in the initial PC-1
        ## permutation; again the parity bits certainly do not increase the key
        ## space! returns 56 bits
        stripped_initkey = DES._map_by_table(inputkey, self._pc1, 64)
        DBG("key schedule: 1. PC-1 permutation, stripping parity")
        DBG("key schedule: key      %s"%tostring(stripped_initkey, 56))

        ## generate a specific key for encryption
        ## the roundkey length is 56 bit
        ##
        ## iterate for each key until the roundidx is reached (easier to
        ## understand decryption afterwards)
        DBG( "key schedule" )
        keys = []
        key = stripped_initkey

        for idx in range(16):
            DBG("key schedule round %d" % idx)

            ## 2. split
            left, right = self._splitkey(key)
            DBG("key schedule: 2. split")
            DBG("key schedule: key       %s %s"%(tostring(left, 28), tostring(right, 28)))

            ## 3. shift left
            if isencrypt:
                DBG("key schedule: 3. shift left")
                left = self._shiftleft(left, idx)
                right = self._shiftleft(right, idx)
            else:
                DBG("key schedule: 3. shift right")
                left = self._shiftright(left, idx)
                right = self._shiftright(right, idx)

            DBG("key schedule: key       %s %s"%(tostring(left, 28), tostring(right, 28)))

            ## 4. merge keys
            key = DES._append(left, right, 28)
            DBG("key schedule: 4. merge keys")
            DBG("key schedule: key       %s"%(tostring(key, 56)))

            ## 5. PC-2 permutation
            roundkey = DES._map_by_table(key, self._pc2, 56)
            DBG("key schedule: 5. PC-2 permutation")
            DBG("key schedule: rnd key   %s"%(tostring(roundkey, 48)))

            keys.append(roundkey)
            DBG("")
        return keys

    def _splitkey(self, key):
        ## the resulting 56-bit key is split into two halves C[0] and D[0], and
        ## the actual key schedule starts
        leftkey = (key >> 28) & 0xfffffff
        rightkey = key & 0xfffffff
        return leftkey, rightkey

    def _shiftleft(self, key, roundidx):
        ## the two 28-bit halves are cyclically shifted left, i.e. rotated, by
        ## one or two bit positions depending on the round i according to the
        ## rules;
        ## note that the rotation takes only place within either the left or the
        ## right half; the total number of rotations sum up to 28 both halves
        ## are merged in this step
        ## key has size of 28 bit, result has 28 bit
        shifter = self._shiftrules[roundidx]
        ret = (key <<shifter) & 0xfffffff
        mask = 0x0
        for sh in range(shifter): mask = (mask<<1) | 0x1
        ret |= (key >>(28-shifter)) & mask
        return ret

    def _shiftright(self, key, roundidx):
        ## same as left shift, but used for decryption; in decryption round 1,
        ## subkey 16 is needed; in round 2 subkey 15
        ## in decryption round 1 the key is not rotated
        ## in decryption rounds 2,9 and 16 the two halves are rotated right by
        ## one bit
        ## in the other rounds, 3,4,5,6,7,8,10,11,12,13,14 and 15 the two halves
        ## are rotated right by two bits
        ## key has size of 28 bit, result has 28 bit

        ## special for decryption, and key generation
        if 0 == roundidx: return key
        shifter = self._shiftrules[roundidx]
        ret = 0x0
        for bit in range(shifter):
            pre = (key & 0b1) <<27
            ret = (ret >>1) | pre # prepend
            key >>= 1
        ret = ret | key
        return ret

class FFunction():
    def __init__(self, inputkey):
        ## the e-box as other boxes as well, historically starts by one as first
        ## index; for a better understanding, this is kept throughtout the im-
        ## plemenetation

        ## starts with 1
        self._ebox = [32, 1, 2, 3,
                       4, 5, 4, 5,
                       6, 7, 8, 9,
                       8, 9,10,11,
                      12,13,12,13,
                      14,15,16,17,
                      16,17,18,19,
                      20,21,20,21,
                      22,23,24,25,
                      24,25,26,27,
                      28,29,28,29,
                      30,31,32, 1]

        ## S-boxes design criteria:
        ##
        ## 1. each S-box has six input bits and four output bits
        ## 2. no single output bit should be too close to a linear combination
        ##    of the input bits
        ## 3. if the lowest and the highest bits of the input are fixed and the
        ##    four middle bits are varied, each of the possible 4-bit output
        ##    values must occur exactly once
        ## 4. if two inputs to an S-box differ in exactly one bit, their outputs
        ##    must differ in at least two bits
        ## 5. if two inputs to an S-box differ in the two middle bits, their
        ##    outputs must differ in at least two bits
        ## 6. if two inputs to an S-box differ in their first two bits and are
        ##    identical in their last two bits, the two outputs must be
        ##    different
        ## 7. for any nonzero 6-bit difference between inputs, no more than 8 of
        ##    the 32 pairs of inputs exhibiting that difference may result in
        ##    the same output difference
        ## 8. a collision (zero output difference) at the 32-bit output of the
        ##    eight S-boxes is only possible for three adjacent S-boxes
        self._s1 = [[0xe,0x4,0xd,0x1,0x2,0xf,0xb,0x8,0x3,0xa,0x6,0xc,0x5,0x9,0x0,0x7],
                    [0x0,0xf,0x7,0x4,0xe,0x2,0xd,0x1,0xa,0x6,0xc,0xb,0x9,0x5,0x3,0x8],
                    [0x4,0x1,0xe,0x8,0xd,0x6,0x2,0xb,0xf,0xc,0x9,0x7,0x3,0xa,0x5,0x0],
                    [0xf,0xc,0x8,0x2,0x4,0x9,0x1,0x7,0x5,0xb,0x3,0xe,0xa,0x0,0x6,0xd]]

        self._s2 = [[0xf,0x1,0x8,0xe,0x6,0xb,0x3,0x4,0x9,0x7,0x2,0xd,0xc,0x0,0x5,0xa],
                    [0x3,0xd,0x4,0x7,0xf,0x2,0x8,0xe,0xc,0x0,0x1,0xa,0x6,0x9,0xb,0x5],
                    [0x0,0xe,0x7,0xb,0xa,0x4,0xd,0x1,0x5,0x8,0xc,0x6,0x9,0x3,0x2,0xf],
                    [0xd,0x8,0xa,0x1,0x3,0xf,0x4,0x2,0xb,0x6,0x7,0xc,0x0,0x5,0xe,0x9]]

        self._s3 = [[0xa,0x0,0x9,0xe,0x6,0x3,0xf,0x5,0x1,0xd,0xc,0x7,0xb,0x4,0x2,0x8],
                    [0xd,0x7,0x0,0x9,0x3,0x4,0x6,0xa,0x2,0x8,0x5,0xe,0xc,0xb,0xf,0x1],
                    [0xd,0x6,0x4,0x9,0x8,0xf,0x3,0x0,0xb,0x1,0x2,0xc,0x5,0xa,0xe,0x7],
                    [0x1,0xa,0xd,0x0,0x6,0x9,0x8,0x7,0x4,0xf,0xe,0x3,0xb,0x5,0x2,0xc]]

        self._s4 = [[0x7,0xd,0xe,0x3,0x0,0x6,0x9,0xa,0x1,0x2,0x8,0x5,0xb,0xc,0x4,0xf],
                    [0xd,0x8,0xb,0x5,0x6,0xf,0x0,0x3,0x4,0x7,0x2,0xc,0x1,0xa,0xe,0x9],
                    [0xa,0x6,0x9,0x0,0xc,0xb,0x7,0xd,0xf,0x1,0x3,0xe,0x5,0x2,0x8,0x4],
                    [0x3,0xf,0x0,0x6,0xa,0x1,0xd,0x8,0x9,0x4,0x5,0xb,0xc,0x7,0x2,0xe]]

        self._s5 = [[0x2,0xc,0x4,0x1,0x7,0xa,0xb,0x6,0x8,0x5,0x3,0xf,0xd,0x0,0xe,0x9],
                    [0xe,0xb,0x2,0xc,0x4,0x7,0xd,0x1,0x5,0x0,0xf,0xa,0x3,0x9,0x8,0x6],
                    [0x4,0x2,0x1,0xb,0xa,0xd,0x7,0x8,0xf,0x9,0xc,0x5,0x6,0x3,0x0,0xe],
                    [0xb,0x8,0xc,0x7,0x1,0xe,0x2,0xd,0x6,0xf,0x0,0x9,0xa,0x4,0x5,0x3]]

        self._s6 = [[0xc,0x1,0xa,0xf,0x9,0x2,0x6,0x8,0x0,0xd,0x3,0x4,0xe,0x7,0x5,0xb],
                    [0xa,0xf,0x4,0x2,0x7,0xc,0x9,0x5,0x6,0x1,0xd,0xe,0x0,0xb,0x3,0x8],
                    [0x9,0xe,0xf,0x5,0x2,0x8,0xc,0x3,0x7,0x0,0x4,0xa,0x1,0xd,0xb,0x6],
                    [0x4,0x3,0x2,0xc,0x9,0x5,0xf,0xa,0xb,0xe,0x1,0x7,0x6,0x0,0x8,0xd]]

        self._s7 = [[0x4,0xb,0x2,0xe,0xf,0x0,0x8,0xd,0x3,0xc,0x9,0x7,0x5,0xa,0x6,0x1],
                    [0xd,0x0,0xb,0x7,0x4,0x9,0x1,0xa,0xe,0x3,0x5,0xc,0x2,0xf,0x8,0x6],
                    [0x1,0x4,0xb,0xd,0xc,0x3,0x7,0xe,0xa,0xf,0x6,0x8,0x0,0x5,0x9,0x2],
                    [0x6,0xb,0xd,0x8,0x1,0x4,0xa,0x7,0x9,0x5,0x0,0xf,0xe,0x2,0x3,0xc]]

        self._s8 = [[0xd,0x2,0x8,0x4,0x6,0xf,0xb,0x1,0xa,0x9,0x3,0xe,0x5,0x0,0xc,0x7],
                    [0x1,0xf,0xd,0x8,0xa,0x3,0x7,0x4,0xc,0x5,0x6,0xb,0x0,0xe,0x9,0x2],
                    [0x7,0xb,0x4,0x1,0x9,0xc,0xe,0x2,0x0,0x6,0xa,0xd,0xf,0x3,0x5,0x8],
                    [0x2,0x1,0xe,0x7,0x4,0xa,0x8,0xd,0xf,0xc,0x9,0x0,0x3,0x5,0x6,0xb]]

        ## starts with 1
        self.pbox = [16, 7,20,21,
                      29,12,28,17,
                       1,15,23,26,
                       5,18,31,10,
                       2, 8,24,14,
                      32,27, 3, 9,
                      19,13,30, 6,
                      22,11, 4,25]

        self.keyschedule = KeySchedule(inputkey)

    def _sbox(self, text, sbox):
        ## text has 6 bit, result is a 4-bit s-box entry
        val_first = (text >> 5) & 0x1
        val_last = text & 0x1
        row = DES._append(val_first, val_last)
        col = (text >> 1) & 0xf
        return sbox[row][col]

    def split(self, text):
        ## in round i it takes the right half R[i-1] of the output of the
        ## previous round and the current round key k[i] as input; the output of
        ## the f-function is used as an XOR-mask for encrypting the left half
        ## input bits L[i-1]
        ## takes 64-bit text, and splits into two 32-bit pieces
        left = (text>>32) & 0xffffffff
        right = text & 0xffffffff
        return (left, right)

    def expansion(self, text):
        ## first, the 32-bit input is expanded to 48 bits by partitioning the
        ## input into eight 4-bit blocks and by expanding each block to 6 bits
        ## expand 32bit to 48bit
        binlst = 0x0
        for pos in self._ebox:
            ## text has 32 bit
            binlst = DES._append(binlst, DES._getnth(text, (pos-1), 32))
        return binlst

    def encryptkey(self, text, roundidx):
        ## next, the 48-bit result of the expansion is XORed with the round key
        ## k[i], and the eight 6-bit blocks are fed into eight different substi-
        ## tution boxes, which are often referred to as S-boxes takes a 48-bit
        ## input and a 48-bit key, the result then is 48-bit
        text ^= self.keyschedule.encryptkeys[roundidx]
        return text

    def decryptkey(self, text, roundidx):
        ## in fact this method is not necessary - for decryption the encryption
        ## keys are used in the reversed order (give it a try)
#        text ^= self.keyschedule.encryptkeys[len(self.keyschedule.encryptkeys) - roundidx -1]
        ## finally, a separate key generation for decryption keys (using right
        ## shift instead of left shift, basically) is not needed, but just
        ## demonstrated here
        text ^= self.keyschedule.decryptkeys[roundidx]
        return text

    def sbox(self, text):
        ## the s-boxes are the core of DES in terms of cryptographic strength;
        ## they are the only nonlinear element in the algorithm and provide
        ## confusion
        ## takes a 48-bit input, result is 32-bit
        ##
        ## this is because the 6-bit sequences taken for obtaining the s-box
        ## entries are converted 8 times into 4-bit s-box table entries each
        binlst = 0x0
        sub = (text >> (48 - 6)) & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s1), 4)

        sub = (text >> (48 - 12)) & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s2), 4)

        sub = (text >> (48 - 18)) & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s3), 4)

        sub = (text >> (48 - 24)) & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s4), 4)

        sub = (text >> (48 - 30)) & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s5), 4)

        sub = (text >> (48 - 36)) & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s6), 4)

        sub = (text >> (48 - 42)) & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s7), 4)

        sub = text & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s8), 4)

        return binlst

class DES():
    def __init__(self, inputkey):
        self.ip = InitialPermutation()
        self.ffunc = FFunction(inputkey)

    @staticmethod
    def _tablelookup(table, index, offset=0):
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

    @staticmethod
    def _getnth(binlst, nth, size):
        ## return the nth bit, contained in the bit list (a number)
        ## where nth is an index, starting with 0
        ##
        ## params:
        ## binlst = a number, which serves as list of bit values
        ## nth = index of a specific bit in binlst
        ## size = the full size of the binlst in bits
        return ((binlst >> (size - (nth+1))) & 0x1)

    @staticmethod
    def _append(binlst, val, nbits=1):
        ## appends a bit to a bit list (a number) of such values and returns it
        ##
        ## params:
        ## binlst = a bit number, which serves as list of bit values
        ## val = a binary number to be appended
        ## nbits = the size of val
        ##         DES is a bit based algorithm, so the atomic unit is in bits
        return ((binlst <<nbits)|val)

    @staticmethod
    def _map_by_table(text, table, textsize):
        ## fetches a refered bit from text and maps it according to the table
        ##
        ## params:
        ## text = the input text, a bit number
        ## table = the mapping table
        ## textsize = the number of bits for text
        binlst = 0b0
        for pos in table:
            ## fetch bit specified by table
            binlst = DES._append(binlst, DES._getnth(text, (pos-1), textsize))
        return binlst

    @staticmethod
    def _string2hex(text):
        ## python3 string to hex :int formatting by means of binascii package
        import binascii
        return int(binascii.hexlify(bytes(text,"iso_8859_1")), 16)

    @staticmethod
    def _hex2string(hexadecimal):
        text = "%x"%hexadecimal
        return ''.join(chr(int(text[i:i+2], 16)) for i in range(0, len(text), 2))

    def encrypt(self, plaintext, ishex=False):
        ## input can be hex or string, output will be hex
        if ishex: state = plaintext
        else: state = DES._string2hex(plaintext) & 0xffffffffffffffff
        DBG( "\n\nENCRYPTION\n\nplaintext:         %#s"%tostring(state, 64) )
        return self.crypto(state, True)

    def decrypt(self, ciphertext):
        ## input is in hex, output will be string
        DBG( "\n\nDECRYPTION\n\nplaintext:         %#s"%tostring(ciphertext, 64) )
        state = self.crypto(ciphertext, False)

        ## IMPORTANT: for ciphertext blocks shorter than blocksize - if hex
        ## output is needed, '0's have to be appended, otherwise (as string)
        ## missing '0's to fill size are cut off at decoding automatically
        return DES._hex2string(state)

    def crypto(self, state, isencrypt):
        ## params
        ## plaintext = the plaintext as string or as hex number
        ## ishex = if the plaintext was a hex number (True)

        ## 1. initial permutation
        ## Note that both permutations do not increase the security of DES at all
        ## takes 64-bit input, result is
        state = DES._map_by_table(state, self.ip.initial_permutation, 64)
        DBG("1. initial permutation")
        DBG("    %s"%(tostring(state, 64)))

        ## F-function
        for idx in range(16):
            ## DES loops the following steps
            ## 2. split
            left_half, right_half = self.ffunc.split(state)
            DBG("2. split")
            DBG("    %s %s"%(tostring(left_half, 32), tostring(right_half, 32)))

            ## 3. expansion permutation
            right_exp = self.ffunc.expansion(right_half)
            DBG("3. expansion permutation")
            DBG("    %s %s"%(tostring(left_half, 32), tostring(right_half, 32)))
            DBG("             | %s - expanded right half"%(tostring(right_exp, 48)))
            if isencrypt: DBG("             | %s - roundkey[%d]"%(tostring(self.ffunc.keyschedule.encryptkeys[idx], 48), idx))
            else: DBG("             | %s - roundkey[%d]"%(tostring(self.ffunc.keyschedule.decryptkeys[idx], 48), idx))

            ## 4. apply key
            if isencrypt: right_exp = self.ffunc.encryptkey(right_exp,idx)
            else: right_exp = self.ffunc.decryptkey(right_exp,idx)
            DBG("4. key")
            DBG("    %s %s"%(tostring(left_half, 32), tostring(right_half, 32)))
            DBG("             | %s"%(tostring(right_exp, 48)))

            ## 5. s-boxes
            right_exp = self.ffunc.sbox(right_exp)
            DBG("5. s-box")
            DBG("    %s %s"%(tostring(left_half, 32), tostring(right_half, 32)))
            DBG("             | %s"%(tostring(right_exp, 32)))

            ## 6. permutation
            ## finally, the 32-bit output is permuted bitwise according to the
            ## P permutation; unlike the initial IP and its inverse IP-1, the
            ## permutation P introduces diffusion because the four output bits of
            ## each S-box are permuted in such a way that they affect several
            ## different S-boxes in the following round
            ## takes a 32-bit input, result is 32-bit
            right_exp = self._map_by_table(right_exp, self.ffunc.pbox, 32)
            DBG("6. permutation")
            DBG("    %s %s"%(tostring(left_half, 32), tostring(right_half, 32)))
            DBG("             | %s"%(tostring(right_exp, 32)))

            ## 7. xor left and right half
            left_half ^= right_exp
            DBG("7. xor left half")
            DBG("    %s %s"%(tostring(left_half, 32), tostring(right_half, 32)))

            ## 8. merge and switch halves
            state = DES._append(right_half, left_half, 32)
            DBG("8. merge and switch halves")
            DBG("    %s"%(tostring(state, 64)))
            DBG("")

        ## DES loops the following steps
        ## final split
        left_half, right_half = self.ffunc.split(state)
        DBG("final split")
        DBG("    %s %s"%(tostring(left_half, 32), tostring(right_half, 32)))

        ## final merge and switch halves
        state = DES._append(right_half, left_half, 32)
        DBG("final switch halves")
        DBG("    %s"%(tostring(state, 64)))

        ## revert permutation
        ## Note that both permutations do not increase the security of DES at all
        state = DES._map_by_table(state, self.ip.final_permutation, 64)
        DBG("9. final permutation")
        DBG("    %s"%(tostring(state, 64)))

        return state

### main ###
def main(argv=sys.argv[1:]):
    blocksize = 64 # fixed, so variable is not used
    keysize_with_parity = 64
    inputkey = 0xffffffffffffffff
    plaintext = ""
    keylength = 64 # fixed, so variable is not used

    if len(argv) > 0:
        ## offer encryption by command line argument
        try:
            inputkey = int(argv[0],16)
            plaintext = argv[1]
        except:
            die('usage: either w/o arguments, or as follows\n$ %s <inputkey> ' \
                    '"<plaintext>"\ne.g.\n$ %s %s "%s"' \
                    %(sys.argv[0],sys.argv[0], \
                          "0x000102030405060708090a0b0c0d0e0f", \
                          "As Lusíadas"))
    else:
        ## init some raw input key example
        inputkey = 0x0001020304050607
        ## init some input text example

        ## NB: in python3 using '\n' may cause hickups at parsing for encryption,
        ## thus prefer 'os.linesep' instead
        import os
        plaintext = "As armas e os barões assinalados, " + os.linesep + \
            "Que da ocidental praia Lusitana, " + os.linesep + \
            "Por mares nunca de antes navegados, " + os.linesep + \
            "Passaram ainda além da Taprobana, " + os.linesep + \
            "Em perigos e guerras esforçados, " + os.linesep + \
            "Mais do que prometia a força humana, " + os.linesep + \
            "E entre gente remota edificaram " + os.linesep + \
            "Novo Reino, que tanto sublimaram;"

    print(f"initial key:\n{tostring(inputkey, 16)}, key length {keylength}, block size {blocksize}\n")

    print("plaintext:")
    if len(plaintext) <= 0: die("plaintext was empty")
    print("{plaintext}\n")

    ## init the algorithm
    des = DES(inputkey)

    idx = -1
    ciphertext = []
    blocktext = ""
    for idx in range(len(plaintext)-1):
        blocktext += plaintext[idx]
        if (idx+1) % (blocksize/8) == 0:
            ciphertext.append(des.encrypt(blocktext))
            blocktext = ""
    blocktext += plaintext[idx+1]
    ciphertext.append(des.encrypt(blocktext))

    ## print result
    print("encrypted:")
    for item in ciphertext:
        print("{tostring(item, 64)}")
    print("\n")

    ## decrypt
    decryptedtext = ""
    for block in ciphertext:
        decryptedtext += des.decrypt(block)

    ## print result
    print("decrypted:")
    print(f"{decryptedtext}")

### start ###
if __name__ == '__main__':
    main()
print("READY.")
