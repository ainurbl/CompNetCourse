import datetime

IP = '127.0.0.1'
PORT = 35666
BYTES = 1024
MISS_RATE = 0.2
TIMEOUT = 1
PING_COUNT = 10


def parse_time(msg):
    msg = msg.split()
    return datetime.datetime.strptime(f'{msg[2]} {msg[3]}', '%Y-%m-%d %H:%M:%S.%f')


def generate_report(rtts):
    return f'rtt {rtts[-1]:.3f}, min {min(rtts):.3f}, max {max(rtts):.3f}, avg {sum(rtts) / len(rtts):.3f}'
