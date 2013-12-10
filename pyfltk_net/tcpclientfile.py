#!/usr/bin/env python

import socket
import sys

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((socket.gethostbyname(socket.gethostname()), int(sys.argv[1])))

cfile = conn.makefile("w")
try:
    cfile.write(sys.stdin.read())
finally:
    cfile.close()
    conn.close()
