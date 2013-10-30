#!/usr/bin/env python

import socket
import sys

with open(sys.argv[1], "rb") as f:
    text = f.read()

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print "Connecting to server at", sys.argv[2] + ":" + sys.argv[3]

conn.connect((sys.argv[2], int(sys.argv[3])))

print "Transferring file..."

conn.sendall(text)
print "Sent file", sys.argv[1]

conn.close()
