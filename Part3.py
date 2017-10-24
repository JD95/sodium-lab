#~/usr/bin/env python

import socket
import nacl.utils
from nacl.public import PrivateKey, Box
from nacl.encoding import Base64Encoder

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("cyberlab.pacific.edu", 12001))
    totalsent = 0
    private = PrivateKey.generate()
    public = private.public_key
    box = Box(private, public)
    msg = bytearray('CRYPTO 1.0 REQUEST\r\n'
                    + 'Name: Jeff Dwyer\r\n'
                    + 'PublicKey: ' +
                    str(public.encode(Base64Encoder)) + '\r\n'
                    + '\r\n', 'utf-8')
    while totalsent < len(msg):
        sent = s.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError('socket connection broken')
        totalsent += sent
    chunks = []
    bytes_recd = 0
    while bytes_recd < len(msg):
        chunk = s.recv(min(len(msg) - bytes_recd, 2048))
        if chunk == b'':
            raise  RuntimeError('socket connection broken')
        chunks.append(chunk)
        bytes_recd += len(chunk)
    print(box.decrypt(b''.join(chunks)))
