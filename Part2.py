#~/usr/bin/env python

import nacl.secret
import nacl.utils

"""
Part 2
"""

if __name__ == '__main__':
    with open('part2.ciphertext.bin', 'rb') as ct:
        with open('part2.key.bin', 'rb') as key:
            box = nacl.secret.SecretBox(key.read())
            print(str(box.decrypt(ct.read())))
