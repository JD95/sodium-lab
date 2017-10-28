#!~/usr/bin/env python

import socket
import binascii
from nacl.public import PrivateKey, Box
from nacl.encoding import Base16Encoder, HexEncoder
import base64

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('cyberlab.pacific.edu', 12001))
    private = PrivateKey.generate()
    public = private.public_key

    k = public.encode(encoder=Base16Encoder)
    msg = (b'CRYPTO 1.0 REQUEST\r\n'
           + b'Name: Jeff Dwyer\r\n'
           + b'PublicKey: ' + k + b'\r\n'
           + b'\r\n')

    # Sending Request
    print(msg.decode('utf-8'))
    totalsent = 0
    while totalsent < len(msg):
        sent = s.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError('socket connection broken')
        totalsent += sent

    chunks = []
    listen = True
    while listen:
        chunk = s.recv(2048)
        chunks.extend(chunk)
        listen = chunk != b''

    c = bytearray(chunks).decode('utf-8')
    server_public = c.split('\r\n')[2].split(': ')[1]
    c = c.split('\r\n')[3].split(': ')[1]
    dumb = PrivateKey.generate()
    dumb.public_key._public_key = base64.b16decode(server_public)
    b = Box(private, dumb.public_key)
    c = c.encode('utf-8')
    c = binascii.unhexlify(c)
    print(b.decrypt(c))
