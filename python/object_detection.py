from sys import argv
from struct import pack
import socket as sct
from time import sleep

PORT = 4269
TYPE_POSITION = 40

counter = 0
inc = 0.001
incr = True

class UdpClient:

    def __init__(self, ip, port):
        self.sock = sct.socket(sct.AF_INET, sct.SOCK_DGRAM)
        self.ip = ip
        self.port = port

    def sendto(self, data):
        self.sock.sendto(data, (self.ip, self.port))

    def get_byte_from(self, x, y, z, type_='f'):
        return bytes([TYPE_POSITION]) + bytes(pack(type_, x)) + bytes(pack(type_, y)) + bytes(pack(type_, z))

def getI(i):
    global counter, incr
    if counter == 0:
        incr = True
    elif counter == 10:
        incr = False
    
    if incr:
        counter += 1
        return i + inc
    else:
        counter -= 1
        return i - inc

def object_detection(ip):
    uc = UdpClient(ip, PORT)
    i = 0
    while True:
        i = getI(i)
        uc.sendto(uc.get_byte_from(i, 0, 0))
        sleep(1)

if __name__ == "__main__":
    if len(argv) > 1:
        ip = argv[1]
    else:
        ip = input("Enter IP: ")
    
    object_detection(ip)