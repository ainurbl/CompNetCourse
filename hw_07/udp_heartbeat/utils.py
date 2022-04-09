import datetime

IP = '127.0.0.1'
PORT = 35666
BYTES = 1024
CLIENT_PINGS_COUNT = 30
TIME_BEFORE_PRESUMING_DEATH = 1


def parse_time(msg):
    msg = msg.split()
    return datetime.datetime.strptime(f'{msg[2]} {msg[3]}', '%Y-%m-%d %H:%M:%S.%f')
