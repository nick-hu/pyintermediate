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
    print("starting up..")

    loop = asyncio.get_event_loop()
    coro = loop.create_server(SimpleChatClientProtocol, port=1234)
    server = loop.run_until_complete(coro)

    for socket in server.sockets:
        print("serving on {}".format(socket.getsockname()))

    loop.run_forever()
