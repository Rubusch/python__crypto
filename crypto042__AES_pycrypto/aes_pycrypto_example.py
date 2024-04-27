#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Mar-19
#
# based on http://www.commx.ws/2013/10/aes-encryption-with-python/
# framework example

import base64
from Cryptodome import Random
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES

def encrypt(plaintext, key=None, key_size=256):
    if key is None:
        key = Random.new().read(key_size // 8)

    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padding = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
    padded_plaintext = base64.b64encode(padding(plaintext).encode('utf-8'))
    return (iv + cipher.encrypt(padded_plaintext), key)

def decrypt(ciphertext, key):
    unpad = lambda s: s[:-ord(s[-1])]
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(base64.b64decode(cipher.decrypt(ciphertext[AES.block_size:])).decode('utf-8'))
    return plaintext

if __name__ == '__main__':
    ## a random key will be taken and returned together with the ciphered text
    ## the pair "randomkey + ciphered text" then will be passed to the decrypt
    ## function (that's why the ciphered printout looks always different);
    ## in addition an IV will be applied at encryption (CBC ?)

    import os
    plaintext = "E vós, Tágides minhas, pois criado" + os.linesep + \
        "Tendes em mim um novo engenho ardente," + os.linesep + \
        "Se sempre em verso humilde celebrado" + os.linesep + \
        "Foi de mim vosso rio alegremente," + os.linesep + \
        "Dai-me agora um som alto e sublimado," + os.linesep + \
        "Um estilo grandíloquo e corrente," + os.linesep + \
        "Porque de vossas águas, Febo ordene" + os.linesep + \
        "Que não tenham inveja às de Hipocrene." + os.linesep

    print(f"plaintext:\n{plaintext}")

    ciphertext_and_key = encrypt(plaintext)
    ciphertext = bytearray(ciphertext_and_key[0]).hex()
    #ciphertext = "".join(f"{i:02x}" for i in ciphertext_and_key[0]) ## alternative to the above
    print(f"encrypted:\n{ciphertext}" + os.linesep)

    decryptedtext = decrypt(*ciphertext_and_key) ## pass ciphertext and key
    print(f"decrypted:\n{decryptedtext}")
    assert decryptedtext == plaintext

    print("READY.")
