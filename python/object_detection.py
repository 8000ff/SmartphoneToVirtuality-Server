from sys import argv
from struct import pack
import socket as sct
from time import sleep

PORT = 4269
TYPE_POSITION = 40

counter = 0
inc = 0.001
incr = True

class ODUdp:

    def __init__(self, ip, port):
        self.sock = sct.socket(sct.AF_INET, sct.SOCK_DGRAM)
        self.ip = ip
        self.port = port

    def sendto(self, data):
        self.sock.sendto(data, (self.ip, self.port))

    def get_byte_from(self, x, y, z, type_='f'):
        return bytes([TYPE_POSITION]) + bytes(pack(type_, x)) + bytes(pack(type_, y)) + bytes(pack(type_, z))
        
if __name__ == "__main__":
    if len(argv) > 1:
        ip = argv[1]
    else:
        ip = input("Enter IP: ")
    
    object_detection(ip)