#!/usr/bin/env python

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
curraddr = socket.gethostbyname_ex(socket.gethostname())[2][0]
sock.bind((curraddr, int(sys.argv[1])))

print "Awaiting for client connection..."

sock.listen(1)
conn, addr = sock.accept()
print "Client connected from", addr[0] + ":" + str(addr[1])

print "Receiving file; writing to", sys.argv[2]

with open(sys.argv[2], "wb") as f:
    while True:
        text = conn.recv(1024)
        if not text:
            break
        f.write(text)

conn.close()
