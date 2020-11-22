import asyncio
from threading import Thread
from time import sleep

TYPE_SCREEN_SIZE = -12
TYPE_SUB = -13
TYPE_UNSUB = -14

class UdpServer:

    def __init__(self):
        self.addrs = []
        self.screen_size = None

    def process(self, data, addr):
        type, _ = data.decode().split('_')
        type = int(type)
        if type == TYPE_SUB:
            print(f"{addr} just subscribed! :)")
            if self.screen_size is not None:
                self.transport.sendto(self.screen_size, addr)
            self.addrs.append(addr)
        elif type == TYPE_UNSUB:
            print(f"{addr} just unsubscribed! :(")
            self.addrs.remove(addr)
        else:
            if self.screen_size is None and type == TYPE_SCREEN_SIZE:
                print(f"{addr} is connnected!")
                self.screen_size = data
            for ad in self.addrs:
                self.transport.sendto(data, ad)
        
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        self.process(data, addr)

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