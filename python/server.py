import asyncio
from struct import unpack

TYPE_SCREEN_SIZE = 37
TYPE_SUB = 38
TYPE_UNSUB = 39

class UdpServer:

    def __init__(self):
        self.addrs = []
        self.screen_size = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        type = data[0]
        if type == TYPE_SUB:
            print(f"{addr} just subscribed! :)")
            if self.screen_size is not None:
                self.transport.sendto(self.screen_size, addr)
            self.addrs.append(addr)
        elif type == TYPE_UNSUB:
            print(f"{addr} just unsubscribed! :(")
            self.addrs.remove(addr)
        elif type == TYPE_SCREEN_SIZE:
            print(f"{addr} is connnected!")
            self.screen_size = data
        else:
            for ad in self.addrs:
                self.transport.sendto(data, ad)

    def error_received(self, err):
        print(err)

async def run_server():
    print("Starting UDP server")
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(lambda: UdpServer(), local_addr=('192.168.1.67', 4269))

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()

if __name__ == '__main__':
    asyncio.run(run_server())