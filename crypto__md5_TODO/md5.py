#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-September-08


md5 algorithm (not collision save, can be broken in seconds, 2014) is a classic
hash function; can be used for performance tests e.g. by breaking it


md5 example

pseudocode implementation (source: http://en.wikipedia.org/wiki/MD5)

//Note: All variables are unsigned 32 bit and wrap modulo 2^32 when calculating
var int[64] s, K

//s specifies the per-round shift amounts
s[ 0..15] := { 7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22 }
s[16..31] := { 5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20 }
s[32..47] := { 4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23 }
s[48..63] := { 6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21 }

//Use binary integer part of the sines of integers (Radians) as constants:
for i from 0 to 63
    K[i] := floor(abs(sin(i + 1)) × (2 pow 32))
end for
//(Or just use the following table):
K[ 0.. 3] := { 0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee }
K[ 4.. 7] := { 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501 }
K[ 8..11] := { 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be }
K[12..15] := { 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821 }
K[16..19] := { 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa }
K[20..23] := { 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8 }
K[24..27] := { 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed }
K[28..31] := { 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a }
K[32..35] := { 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c }
K[36..39] := { 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70 }
K[40..43] := { 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05 }
K[44..47] := { 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665 }
K[48..51] := { 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039 }
K[52..55] := { 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1 }
K[56..59] := { 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1 }
K[60..63] := { 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391 }

//Initialize variables:
var int a0 := 0x67452301   //A
var int b0 := 0xefcdab89   //B
var int c0 := 0x98badcfe   //C
var int d0 := 0x10325476   //D

//Pre-processing: adding a single 1 bit
append "1" bit to message
/* Notice: the input bytes are considered as bits strings,
  where the first bit is the most significant bit of the byte.[46]

//Pre-processing: padding with zeros
append "0" bit until message length in bits ≡ 448 (mod 512)
append original length in bits mod (2 pow 64) to message


//Process the message in successive 512-bit chunks:
for each 512-bit chunk of message
    break chunk into sixteen 32-bit words M[j], 0 ≤ j ≤ 15
//Initialize hash value for this chunk:
    var int A := a0
    var int B := b0
    var int C := c0
    var int D := d0
//Main loop:
    for i from 0 to 63
        if 0 ≤ i ≤ 15 then
            F := (B and C) or ((not B) and D)
            g := i
        else if 16 ≤ i ≤ 31
            F := (D and B) or ((not D) and C)
            g := (5×i + 1) mod 16
        else if 32 ≤ i ≤ 47
            F := B xor C xor D
            g := (3×i + 5) mod 16
        else if 48 ≤ i ≤ 63
            F := C xor (B or (not D))
            g := (7×i) mod 16
        dTemp := D
        D := C
        C := B
        B := B + leftrotate((A + F + K[i] + M[g]), s[i])
        A := dTemp
    end for
//Add this chunk's hash to result so far:
    a0 := a0 + A
    b0 := b0 + B
    c0 := c0 + C
    d0 := d0 + D
end for

var char digest[16] := a0 append b0 append c0 append d0 //(Output is in little-endian)

//leftrotate function definition
leftrotate (x, c)
    return (x << c) binary or (x >> (32-c));
"""

import sys # sys.exit()
import math

### tools ###
def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)

def string2hex(text):
    return int(text.encode('hex'),16)

def hex2string(hexadecimal):
    text = "%x"%hexadecimal
    return ''.join(chr(int(text[i:i+2], 16)) for i in range(0, len(text), 2))


### algorithm ###

sbox = [7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
        5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
        4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
        6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21]
print "sbox:"
for s in range(len(sbox)/16):
    for s_offset in range(16):
        print '%.2d' % sbox[s*16+s_offset],
    print ""
print ""

## kbox can be replaced by a table of fixed numbers as well
kbox = [int(math.floor(abs(math.sin(k+1)) * (2**32))) for k in range(64)]
print "kbox:"
for k in range(len(kbox)/4):
    print '%s'%'\t'.join(map(lambda x: "%#x"%x, kbox[k*4:k*4+4]))
print ""


def bit_append(bitlst, bits, nbits=1):
    ## returns the bit list (a number) with the appended bits
    ##
    ## params:
    ## bitlst = a value, which serves as a list of bits
    ## bits = the bits to be appended
    ## nbits = number of bits being appended, defaults to 1
    return ((bitlst << nbits) | bits)


def bit_len(bitlst):
# TODO problematic: binary length is not passed - it is known!    
# possibility leading '1'?    

    ## returns the number of bits for the provided argument
    ##
    ## params:
    ## bitlst = a value which serves as a list of bits
    die("TODO bit_len")    
    return len(bin(bitlst))-2


def bit_list(arg, argsize, chunksize):
    ## returns chunks of bits as list by the specified size
    ## the size of the arg has to be divisible by chunksize
    ##
    ## params:
    ## arg = a value which serves as a list of bits
    ## argsize = the size of the arg
    ## chunksize = the size of each chunk
    lst = []
    if chunksize >= argsize: return [arg]

    ## generate a pattern, chunksize bits
    pattern = 0b0
    for idx in range(chunksize):
        pattern = bit_append(pattern, 0b1)

    ## start from last chunk, since leading chuncks then can be empty
    for idx_chunks in range(argsize//chunksize):
        lst.insert(0, arg & pattern)
        arg = arg >>chunksize

    return lst


def bit_or(a, b):
    ## bitwise OR
    ##
    ## params: numbers a, b
    return bit_append(a, b, 0)


def bit_xor(a, b):
    ## bitwise XOR
    ##
    ## params: numbers a, b
    return (a ^ b)


def bit_and(a, b):
    ## bitwise AND
    ##
    ## params: numbers a, b
    return (a & b)


def bit_not(a, asize):
    ## bitwise NOT
    ##
    ## params: number a
#    return (~+-a)    
#    return ~a # TODO check    
    
#    print "vvv:\t'%s'"%bin(a)    
#    print "vvv:\t'%s'"%bin((~+-(0b1 <<asize)) ^ a)    
    
    return ((~+-(0b1 <<asize)) ^ a)


def leftrotate(arg, argsize, shiftsize):
    ## rotate by shiftsize bits
    ##
    ## params:
    ## arg = the argument to be shifted
    ## argsize = the size of arg
    ## shiftsize = the number of bits to be rotated
    argframed = arg|(0b1 <<argsize)
    for idx in range(shiftsize):
        shifter = argframed >>(argsize-idx-1) & 0b1
        arg = bit_append(arg, shifter)

    pattern = 0b1
    for idx in range(argsize-1):
        pattern = bit_append(pattern, 0b1)

    return arg & pattern



messagelength = 448
def padding(arg, arglen):
# TODO    
#    die("XXX") 
    ## append a single '1' bit
    ## input bytes are considered as bit strings, where the first bit is the most significant bit of the byte
    arg = bit_append(arg, 0b1) 
    origlen = arglen

#    print "XXX:arg\t'%#s'"%bin(arg)    

    ## append "0" bit until message length in bits ≡ 448 (mod 512)
    while(arglen % 512) < 448:      
        arg = bit_append(arg, 0b0) 
        arglen += 1
#    print "XXX:arg\t'%#s'"%bin(arg)    

    ## append original length in bits mod (2 pow 64) to message
    arglen = origlen %(2**64)
#    print "XXX:arglen\t'%#d'"%arglen

#    print "XXX:arg\t'%#s'"%bin(bit_append( arg, arglen, len(hex2string(arglen))*8 ))   
#    die("XXX")
#    return bit_append( arg, arglen, len(hex2string(arglen))*8 )   
    return bit_append( arg, arglen, 64 )   


def run_md5(szplaintext):
    ## runs the algorithm
    ##
    ## params:
    ## szplaintext = the entire plaintext as string
    plaintext = string2hex(szplaintext)
    plaintext_len = len(szplaintext*8) ## len returns length in byte,
    ## i.e. for 'a' it is 1 byte, while 'ö' is 2 bytes long

    ## padding
    plaintext = padding(plaintext, plaintext_len)
# TODO check: padded plaintext has less than 458 bits?
    print "XXX:arg\t'%#s'"%bin(plaintext)   

    digest = 0x0

    ## fixed variables
    a0 = 0x67452301
    print "XXX: a0\t'%#s' - init"%bin(a0)    
    b0 = 0xefcdab89
    print "XXX: b0\t'%#s' - init"%bin(b0)    
    c0 = 0x98badcfe
    print "XXX: c0\t'%#s' - init"%bin(c0)    
    d0 = 0x10325476
    print "XXX: d0\t'%#s' - init"%bin(d0)    

    ## split into chunks of size 512 bits
    plaintext_chunks = bit_list(plaintext, plaintext_len, 512)
    print "XXX:plaintext_chunks\t'%#s'"%' '.join(map(bin, plaintext_chunks)) # hex notation    

    ## for each 512-bit chunk of message
    for idx_chunk in range(len(plaintext_chunks)):
        (a0,b0,c0,d0) = md5_operation(plaintext_chunks[idx_chunk], a0, b0, c0, d0)

    print "XXX: a0\t'%#s'"%bin(a0)    

    ## output is assumed in little-endian
    digest = bit_append(digest, a0, 32) # TODO figure out fixed length of a0    
    digest = bit_append(digest, b0, 32) # TODO figure out fixed length of b0    
    digest = bit_append(digest, c0, 32) # TODO figure out fixed length of c0    
    digest = bit_append(digest, d0, 32) # TODO figure out fixed length of d0    

    print "XXX: digest\t'%#s'"%bin(digest)    

    return digest


def md5_operation(plaintext_chunk, a0, b0, c0, d0):
    ## break 512 bit chunk into sixteen 32-bit words M[j], 0 ≤ j ≤ 15
    matrix = bit_list(plaintext_chunk, 512, 32)
#    print "YYY: matrix\t'%#s'"%' '.join(map(bin, matrix))    

    ## initialize hash value for this chunk
    A = a0
    B = b0
    C = c0
    D = d0

    
    print "***: A\t'%s' - 32bit (raw)"%bin(A)    
    _tmp = A|0b100000000000000000000000000000000
    print "***: A\t'0b%s' - 32bit (leading '1' at pos 33.)"%bin(_tmp&0b111111111111111111111111111111111)[3:]    
    _tmp = 0x0
    

    g = 0
    for idx in range(64): # 64 rounds
        print "idx:%d"%idx   
        if idx <= 15:
            print "\t\tidx<=15"    
#            F = bit_or(bit_and(B, C), bit_and(bit_not(B), D))
            
            F = bit_or(bit_and(B, C), bit_and(bit_not(B, 32), D))
            
#            b_and_c = bit_and(B, C)
#            print "...:\t'%s' - b_and_c"%bin(b_and_c)    
#
#            not_b = bit_not(B, 32)
#            print "...:\t'%s' - not_b"%bin(not_b)    
#            not_b_and_d = bit_and(not_b, D)
#            print "...:\t'%s' - not_b_and_d"%bin(not_b_and_d)    
#
#            F = bit_or(b_and_c, not_b_and_d)
#            print "...:\t'%s' - F"%bin(F)    
            
            g = idx

        elif 16 <= idx and idx <= 31:
            print "\t\tidx<=31"    
            F = bit_or(bit_and(D, B), bit_and(bit_not(D, 32), C))
            g = (5 * idx + 1) % 16

        elif 32 <= idx and idx <= 47:
            print "\t\tidx<=47"    
            F = bit_xor(B, bit_xor(C, D))
            g = (3 * idx + 5) % 16

        elif 48 <= idx and idx <= 63:
            print "\t\tidx<=63"    
            F = bit_xor(C, bit_or(B, bit_not(D, 32)))
            g = (7 * idx) % 16

        ## trocadilha
        tmp = D
        D = C
        C = B
# TODO: check A is 32 bit of size    

        
#        B = B + leftrotate(A + F + kbox[idx] + matrix[g], 32, sbox[idx])
        
#        print "...:\t'%s' - B, before"%bin(B)    
        _tmp = B|0b100000000000000000000000000000000
        print "...: B\t'0b%s' - 32bit before (leading '1' at pos 33.)"%bin(_tmp&0b111111111111111111111111111111111)[3:]    
        _tmp = 0x0


        _in = A + F + kbox[idx] + matrix[g]
#        print "...:\t'%s' - _in, before"%bin(_in)    

        _lr = leftrotate(_in, 32, sbox[idx])
        print "...:\t'%s' - _lr, before"%bin(_lr)    

        # TODO check cut 32 bit??
        B = (B + _lr) & 0b11111111111111111111111111111111   

#        print "...:\t'%s' - B, after"%bin(B)            
        _tmp = B|0b100000000000000000000000000000000
        print "...: B\t'0b%s' - 32bit after (leading '1' at pos 33.)"%bin(_tmp&0b111111111111111111111111111111111)[3:]    
        _tmp = 0x0

#        die("XXX")    
        



        A = tmp
        
        print "***: A\t'%s' - 32bit (raw)"%bin(A)    
        _tmp = A|0b100000000000000000000000000000000
        print "***: A\t'0b%s' - 32bit (leading '1' at pos 33.)"%bin(_tmp&0b111111111111111111111111111111111)[3:]    
        _tmp = 0x0   
        print ""    
#        die("XXX")    
        

    
    print "***: A\t'%s' - 32bit (raw)"%bin(A)    
    _tmp = A|0b100000000000000000000000000000000
    print "***: A\t'0b%s' - 32bit (leading '1' at pos 33.)"%bin(_tmp&0b111111111111111111111111111111111)[3:]    
    _tmp = 0x0   
    
    ## end for 32-bit matrizes

#    die("XXX")    

    ## add this chunk's hash to result so far
    a0 += A
    print "YYY: a0\t'%#s'"%bin(a0)    
    b0 += B
    print "YYY: b0\t'%#s'"%bin(b0)    
    c0 += C
    print "YYY: c0\t'%#s'"%bin(c0)    
    d0 += D
    print "YYY: d0\t'%#s'"%bin(d0)    

    return (a0, b0, c0, d0)


### main ###
def main(argv=sys.argv[1:]):
    print "md5"
    plaintext="ABC" ## TODO input    

    ## get arguments, or set default values
    if 1 == len(argv):
        if 0 < len(argv[0]):
            try:
                plaintext = argv[0]
            except:
                die("usage: %s <plaintext>\nOR call without arguments"%sys.argv[0] )
    ## checks
    
#    a = 0b1 # init
    a = "ö"

#    print "A:a\t'%#s'"%bin(a) # hex notation
    print "A: %s\t'%#s', len: %d"%(a, bin(string2hex(a)), len(a)*8 ) # hex notation
#    die("XXX")    

    
    print "---"
    ## algorithm
    digest = run_md5(a)
    print "---"
    


#    print "B:res\t'%#s'"%bin(res) # hex notation    
#    print "B:res\t'%#s'"%' '.join(map(bin, res)) # hex notation
    

# TODO    
#    if 4 >= arg: die("FATAL: arg must be greater than 4")
#    die("STOP")    



# TODO remove trailing 'L'    
# TODO check result!!!    
    print "digest:  \t'%#x'"%digest    
    print "expected:\t'%#x' - ö"%0xa172480f4e21d0a124bac19c89569c59    



### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
