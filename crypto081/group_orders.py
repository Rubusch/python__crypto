#!/usr/bin/env python
# -*- coding: utf-8
"""
@author: Lothar Rubusch
@email: l.rubusch@gmail.com
@license: GPLv3
@2024-March-05

Orders of Finit Group

Q: We consider the Group Z*[53]. What are the possible element orders?
How many elements exist for each oder?

TODO    
"""
import sys

def ord(elem, modulo):
    initial = elem
    exponent = 0
    group_elements = []
    while True:
        exponent += 1
        print(f"\t{elem} ** {exponent} mod({modulo}) = ", end = "")
        elem = elem ** exponent % modulo
        group_elements.append(elem)
        print(f"{elem} mod({modulo})")
        if 1 == elem:
            break
    print(f"group elements of finite group {initial-1}: {group_elements}")
    return exponent

def unique(raw_list):
    results = []
    for elem in raw_list:
        if elem not in results:
            results.append(elem)
    return results

def main(argv=sys.argv[1:]):
    group_mod = int(argv[0])
    print(f"Finite Group Order of Z*[{group_mod}]")

    results = []
    for elem in range(2, (group_mod-1)):
        res=ord(elem, group_mod)
        print(f"order of {elem} = {res}")    
        results.append(res)
    print(f"finite group orders: {results}")
    print(f"cardinality of group: {max(results)}")
    print(f"possible element orders: {unique(results)}")

if __name__ == '__main__':
    main()
print("READY.")
