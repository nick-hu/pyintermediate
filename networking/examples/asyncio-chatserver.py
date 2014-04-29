#!/usr/bin/env python

from sys import argv

import asyncio

clients = []


class SimpleChatClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        #print("connection_made: {}".format(self.peername))
        clients.append(self)

    def data_received(self, data):
        #print("data_received: {}".format(data.decode()))
        for client in clients:
            if client is not self:
                client.transport.write("{}: {}".format(self.peername, data.decode()).encode())

    def connection_lost(self, ex):
        #print("connection_lost: {}".format(self.peername))
        clients.remove(self)

if __name__ == '__main__':
    print("Starting server...")

    loop = asyncio.get_event_loop()

    """
    loop is a BaseEventLoop object. coro is a coroutine wrapped in a Task.
    coro becomes a Future. run_until_complete runs until the Future is done.
    """

    coro = loop.create_server(SimpleChatClientProtocol, port=int(argv[1]))
    server = loop.run_until_complete(coro)

    for socket in server.sockets:
        print("Serving on {}:{}".format(*socket.getsockname()))

    loop.run_forever()
