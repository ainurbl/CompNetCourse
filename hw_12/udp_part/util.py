import socket

from random import choice
from string import ascii_uppercase

DEFAULT_GUI_TEXT_SIZE = (45, 1)

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 12333

BATCH_SIZE = 1024

def random_string(n):
    return ''.join(choice(ascii_uppercase) for _ in range(n))


def udp_socket_init():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.settimeout(1)
    return udp_socket


def tcp_socket_init(host, port):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((host, port))
    return tcp_socket
