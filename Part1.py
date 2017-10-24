#!~/usr/bin/env python


"""
Part 1
"""

if __name__ == '__main__':
    with open('part1.ciphertext.bin', 'rb') as cipher:
        with open('part1.otp.bin', 'rb') as otp:
            m = [a ^ b for (a, b) in zip(cipher.read(), otp.read())]
            print(bytearray(m).decode("utf-8"))
