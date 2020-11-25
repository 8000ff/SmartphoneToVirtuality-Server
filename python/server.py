from asyncio import get_running_loop, sleep, run
from socket import gethostbyname_ex, getfqdn

port = 4269

TYPE_SCREEN_SIZE = 37
TYPE_SUB = 38
TYPE_UNSUB = 39

def get_available_addr():
    return gethostbyname_ex(getfqdn())[-1][-1]

class UdpServer:

    def __init__(self):
        self.addrs = []
        self.screen_size = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if data[0] == TYPE_SUB:
            print(f"{addr} just subscribed! :)")
            if self.screen_size is not None:
                self.transport.sendto(self.screen_size, addr)
            self.addrs.append(addr)
        elif data[0] == TYPE_UNSUB:
            print(f"{addr} just unsubscribed! :(")
            self.addrs.remove(addr)
        elif data[0] == TYPE_SCREEN_SIZE:
            print(f"{addr} is connnected!")
            self.screen_size = data
        else:
            for ad in self.addrs:
                self.transport.sendto(data, ad)

    def error_received(self, err):
        print(err)

async def run_server():
    ip = get_available_addr()
    print(f"Starting UDP server on {ip}:{port}")
    loop = get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(lambda: UdpServer(), local_addr=(ip, port))

    try:
        await sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()

if __name__ == '__main__':
    run(run_server())