import socket
from utils import *

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.settimeout(TIMEOUT)

rtts = []
miss_count = 0

for query_index in range(1, PING_COUNT + 1):
    msg = f'Ping {query_index} {datetime.datetime.now()}'.encode()
    client_socket.sendto(msg, (IP, PORT))
    try:
        resp, _ = client_socket.recvfrom(BYTES)
        resp = resp.decode()
        print(resp)
        rtt = (datetime.datetime.now() - parse_time(resp)).total_seconds()
        rtts.append(rtt)
        print(generate_report(rtts))
    except:
        print('Request timed out')
        miss_count += 1
print(f'packet loss ratio {0 if miss_count == 0 else miss_count / PING_COUNT * 100 :.3f}')
