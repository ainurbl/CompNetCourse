import socket

MY_IP = None
NETWORK_IP = None
MY_MAC = None
MY_HOST_NAME = None
MASK = None

DST_MAC = 'ff:ff:ff:ff:ff:ff'


def init():
    global MY_IP, NETWORK_IP, MY_MAC, MASK, MY_HOST_NAME
    with open('config.txt') as file_handler:
        lines = [str(i).strip() for i in file_handler]
        MY_IP = lines[0]
        NETWORK_IP = lines[1]
        MY_MAC = lines[2]
        MASK = [int(i) for i in lines[3].split(', ')]
    MY_HOST_NAME = socket.gethostname()


def get_host_name(ip):
    host_name = '-'
    try:
        host_name = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        print(f'Whoops, could not get host by address')
    return host_name
