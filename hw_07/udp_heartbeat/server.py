import socket

from utils import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))

client_to_last_ping = {}


def check_heartbeat(addr, ping_time):
    if addr in client_to_last_ping:
        diff = (ping_time - client_to_last_ping[addr]).total_seconds()
        return diff < TIME_BEFORE_PRESUMING_DEATH, diff
    return True, -1


while True:
    req, addr = server_socket.recvfrom(BYTES)
    ping_time = parse_time(req.decode())
    is_alive, diff = check_heartbeat(addr, ping_time)
    if not is_alive:
        print(f'client {addr} is probably dead, silence duration is {diff}')
    client_to_last_ping[addr] = ping_time
