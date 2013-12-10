#!/usr/bin/python

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse
sock.bind((socket.gethostbyname(socket.gethostname()), int(sys.argv[1])))

sock.listen(1)
conn, addr = sock.accept()

cfile = conn.makefile()
try:
    sys.stdout.write(cfile.read())
finally:
    cfile.close()
    conn.close()
