#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Feb-18

import sys   # sys.argv[]
from os import path   # path.isfile()


def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)


def replacer(code):
#    ## all lowercase, exercise 1.1
#    code.update({'a':'X'})
#    code.update({'b':'T'})
#    code.update({'c':'W'})
#    code.update({'d':'D'})
#    code.update({'e':'V'})
#    code.update({'f':'Q'})
#    code.update({'g':'Z'})
#    code.update({'h':'L'})
#    code.update({'i':'S'})
#    code.update({'j':'O'})
#    code.update({'k':'N'})
#    code.update({'l':'B'})
#    code.update({'m':'A'})
#    code.update({'n':'U'})
#    code.update({'o':'G'})
#    code.update({'p':'H'})
#    code.update({'q':'K'})
#    code.update({'r':'E'})
#    code.update({'s':'P'})
#    code.update({'t':'Y'})
#    code.update({'u':'R'})
#    code.update({'v':'C'})
#    code.update({'w':'I'})
#    code.update({'x':'F'})
#    code.update({'y':'M'})
##    code.update({'z':''}) # not used
    
    ## all lowercase, exercise 1.1
    code.update({'a':'I'})
#    code.update({'b':''})
#    code.update({'c':''})
#    code.update({'d':''})
    code.update({'e':'Q'})
    code.update({'f':'F'})
    code.update({'g':'U'})
#    code.update({'h':''})
#    code.update({'i':''})
    code.update({'j':'N'})
    code.update({'k':'C'})
    code.update({'l':'R'})
#    code.update({'m':''})
    code.update({'n':'V'})
#    code.update({'o':''})
#    code.update({'p':''})
#    code.update({'q':''})
    code.update({'r':'D'})
    code.update({'s':'S'})
    code.update({'t':'H'}) #?
#    code.update({'u':''})
#    code.update({'v':''})
    code.update({'w':'A'})
    code.update({'x':'P'})
    code.update({'y':'E'})
    code.update({'z':'T'})



def shifter(code, shift):
    ## exercise 1.2
    abc = "abcdefghijklmnopqrstuvwxyz"
    ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if shift > len(ABC):
        print shift,">",len(ABC)   
        die("shift size too big")

    ## cut of shift amount letters
    ABC = ABC[shift:] + ABC[:shift]

    ## set up dict
    for cnt in range(len(abc)):
        code.update({abc[cnt]:ABC[cnt]})


## args - the filename
def main(argv=sys.argv[1:]):
    if 0 == len(argv) or not path.isfile(argv[0]):
        die("usage: %s <path to .txt>" % sys.argv[0])
    filename = argv[0]

    shift=0
    if 1 < len(argv):
        shift = int(argv[1])

    ## set up dictionary
    code = {}

    ## 1. figure out main frequencies, then
    ## 2. figure out missing letters more and more
    ## 3. in case there are typos ;)

    ## exercise 1.1
#    replacer(code)

    ## exercise 1.2
#    shifter(code, shift)

    ## exercise 1.11
    replacer(code)

    ## read text
    f=open(filename)
    cnt=0
    for line in f:

    ## substitute
        result = "".join([code[i] if i in code else i  for i in line])

    ## display result
        print "%d:\t%s"%(cnt,result),
        cnt+=1
    f.close()


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
