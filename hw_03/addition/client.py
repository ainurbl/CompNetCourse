import argparse
import socket

BATCH_SIZE = 1024

parser = argparse.ArgumentParser()
parser.add_argument("host", type=str)
parser.add_argument("port", type=int)
parser.add_argument("path", type=str)
args = parser.parse_args()

host, port, path = args.host, args.port, args.path

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
sock.sendall(bytes(f'GET /{path} HTTP/1.1\r\n\r\n', 'utf-8'))
sock.settimeout(1)
sock.setblocking(True)

content_bytes = []

while True:
    try:
        recv = sock.recv(BATCH_SIZE)
        content_bytes.extend(recv)
        if len(recv) < BATCH_SIZE:
            break
    except socket.timeout:
        break

print(bytes(content_bytes).decode('utf-8'))
sock.close()
