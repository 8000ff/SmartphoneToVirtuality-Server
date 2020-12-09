from asyncio import get_running_loop, sleep, run
from netifaces import ifaddresses, interfaces, AF_INET, gateways
from struct import pack, unpack

port = 4269

TYPE_SCREEN_SIZE = 37
TYPE_SUB = 38
TYPE_UNSUB = 39
TYPE_POSITION = 40

def get_available_addr():
    gateway_interface = gateways()['default'][AF_INET][1]
    for interface in interfaces():
        try:
            if interface == gateway_interface:
                return ifaddresses(interface)[AF_INET][0]['addr']
        except :
            continue
    return False

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

class ObjectDetection:
    
    def __init__(self, udpServer):
        self.udpServer = udpServer

    def sendData(self, x, y, z):
        for ad in self.udpServer.addrs:
            self.udpServer.transport.sendto(self.getDataFrom(x, y, z), ad)

    def getDataFrom(self, x, y, z, type_="f"):
        res = bytes([TYPE_POSITION])
        res += bytes(pack(type_, x))
        res += bytes(pack(type_, y))
        res += bytes(pack(type_, z))
        return res

async def run_server():
    ip = input("Enter an address (press enter to let the server choose): ")
    ip = get_available_addr() if ip == "" else ip
    if not ip:
        raise Exception("No available network interface.")

    print(f"Starting UDP server on {ip}:{port}")
    loop = get_running_loop()
    udpServer = UdpServer()
    objDetect = ObjectDetection(udpServer)
    transport, _ = await loop.create_datagram_endpoint(lambda: udpServer, local_addr=(ip, port))
    
    try:
        await sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()

if __name__ == '__main__':
    run(run_server())