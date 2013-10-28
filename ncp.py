#!/usr/bin/env python

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
curraddr = socket.gethostbyname(socket.gethostname())
sock.bind((curraddr, int(sys.argv[1])))

print "Awaiting for file transfer..."

text, addr = sock.recvfrom(int(sys.argv[3]))

print "Received file from client at", addr[0] + ":" + str(addr[1])

sock.close()

with open(sys.argv[2], "w") as f:
    f.write(text)
