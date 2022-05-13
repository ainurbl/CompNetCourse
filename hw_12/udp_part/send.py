import datetime

import PySimpleGUI as gui

from util import *

window = gui.Window('UDP send', [
    [gui.Text('Введите IP для получения', size=DEFAULT_GUI_TEXT_SIZE), gui.InputText(DEFAULT_HOST, key='host')],
    [gui.Text('Введите порт для получения', size=DEFAULT_GUI_TEXT_SIZE), gui.InputText(DEFAULT_PORT, key='port')],
    [gui.Text('Введите число пакетов для отправки', size=DEFAULT_GUI_TEXT_SIZE), gui.InputText('500', key='count')],
    [gui.Button('Отправить')],
])

udp_socket = udp_socket_init()

while True:
    event, values = window.read()

    if event in (None, 'Exit'):
        break

    if event == 'Отправить':
        host, port, messages_count = None, None, 0
        try:
            host, port = values['host'], int(values['port'])
            messages_count = int(values['count'])
        except Exception as e:
            print(e)

        if messages_count == 0:
            window['count'].Update('Please, enter positive integer')
            continue

        tcp_socket = None
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.connect((host, port))
            tcp_socket.sendall(bytes(str(messages_count), encoding='utf-8'))
        except Exception as e:
            print(e)
        finally:
            if tcp_socket is not None:
                tcp_socket.close()

        try:
            for i in range(messages_count):
                message = f'{int(datetime.datetime.now().timestamp() * 1000)} '
                message += random_string(BATCH_SIZE - len(message))
                udp_socket.sendto(message.encode(), (host, port))
        except Exception as e:
            print(e)

udp_socket.close()
