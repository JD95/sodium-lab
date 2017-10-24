#~/usr/bin/env python

from nacl import pwhash, secret

if __name__ == '__main__':
    with open('part4.ciphertext.bin', 'rb') as c:
        cipher = c.read()
        salt = cipher[:32]
        outer = cipher[32:(32 + 72)]
        inner = cipher[(32 + 72):]
        pwd = b'swordfish'
        outerkey = pwhash.kdf_scryptsalsa208sha256(
            secret.SecretBox.KEY_SIZE,
            pwd,
            salt,
            opslimit=pwhash.SCRYPT_OPSLIMIT_INTERACTIVE,
            memlimit=pwhash.SCRYPT_MEMLIMIT_INTERACTIVE
        )
        outer_box = secret.SecretBox(outerkey)
        inner_key = outer_box.decrypt(outer)
        inner_box = secret.SecretBox(inner_key)
        payload = inner_box.decrypt(inner)
        with open('part4.payload', 'wb') as f:
            f.write(payload)
