#!/usr/bin/env python

import socket
import asyncore
from asynchat import async_chat
from sys import argv


class ChatSession(async_chat):
    def __init__(self, server, sock):
        async_chat.__init__(self, sock)
        self.socket = sock
        self.server = server
        self.set_terminator("\n")
        self.data = []

    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        line = "".join(self.data)
        self.data = []
        self.server.broadcast(line, self)

    def handle_close(self):
        async_chat.handle_close(self)
        self.server.disconnect(self)


class ChatServer(asyncore.dispatcher):
    def __init__(self, port, name):
        print "Starting server..."
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(("", port))

        self.addr = self.socket.getsockname()
        print self.addr
        print "Serving on {0}:{1}".format(*self.addr)
        self.listen(5)
        self.name = name
        self.sessions = []

    def handle_accept(self):
        conn, addr = self.accept()
        self.sessions.append((ChatSession(self, conn), addr))
        print ">>> Made connection to {0}:{1} >>>".format(*addr)
        conn.send("Connected to server at {0}:{1}\n".format(*self.addr))

    def broadcast(self, line, sender):
        for session, addr in self.sessions:
            if session != sender:
                msg = "[{0}:{1}] {2}\n".format(addr[0], addr[1], line)
                session.push(msg)

    def disconnect(self, session):
        addr = self.sessions.pop(zip(*self.sessions)[0].index(session))[1]
        print "<<< Lost connection to {0}:{1} <<<".format(*addr)

if __name__ == "__main__":
    s = ChatServer(int(argv[1]), "asyncore chat server")

    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass
