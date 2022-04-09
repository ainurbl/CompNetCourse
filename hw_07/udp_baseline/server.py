import time
import socket
import random
from utils import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))

while True:
    req, addr = server_socket.recvfrom(BYTES)
    if random.random() < MISS_RATE:
        continue
    time.sleep(random.random())
    resp = req.decode().upper().encode()
    server_socket.sendto(resp, addr)
