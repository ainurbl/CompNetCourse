import argparse
import socket
from pathlib import Path

from threadpool import TThreadpool

PORT = 35666
BATCH_SIZE = 1024

error_resp = b'HTTP/1.1 404 Not Found\r\n\r\n'


def check_path_correctess(path: Path):
    return not path.is_dir() and path.exists()


def create_resp(path: Path):
    if not check_path_correctess(path):
        return error_resp
    with open(path, 'r') as file_handler:
        content = file_handler.read()
    resp = f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}'
    return bytes(resp, 'utf-8')


def extract_path(req: str):
    return req.split('\n')[0].strip().split(' ')[1][1:]


def job_to_do(sock: socket.socket):
    path = Path(extract_path(sock.recv(BATCH_SIZE).decode('utf-8')))
    sock.sendall(create_resp(path))
    sock.close()


parser = argparse.ArgumentParser()
parser.add_argument("--thread_upper_bound", type=int, default=2)
thread_upper_bound = parser.parse_args().thread_upper_bound

pool = TThreadpool(thread_upper_bound, job_to_do)
pool.start()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', PORT))
server_socket.listen()

while True:
    try:
        sock, _ = server_socket.accept()
        pool.add_client(sock)
    except Exception:
        break

pool.stop()
