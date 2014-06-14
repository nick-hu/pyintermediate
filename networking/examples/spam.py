#!/usr/bin/env python

import socket
from sys import argv
from time import sleep

text = "\t "
for x in xrange(50, 256):
    text += chr(x) * 10000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((argv[1], int(argv[2])))
print "Connected"
sock.setblocking(False)

while True:
    try:
        sock.send(text)
    except socket.error:
        pass
