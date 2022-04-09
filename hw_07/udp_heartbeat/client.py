import random
import socket
import time

from utils import *

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

start_time = datetime.datetime.now()

for query_index in range(1, CLIENT_PINGS_COUNT + 1):
    msg = f'Ping {query_index} {datetime.datetime.now()}'.encode()
    client_socket.sendto(msg, (IP, PORT))
    time.sleep(random.random() + 0.2)
