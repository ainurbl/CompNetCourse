import datetime

import PySimpleGUI as gui

from util import *

host, port = DEFAULT_HOST, DEFAULT_PORT
tcp_socket = tcp_socket_init(host, port)
tcp_socket.listen(1)

window = gui.Window('TCP get', [
    [gui.Text('Введите IP для получения', size=DEFAULT_GUI_TEXT_SIZE), gui.InputText(host)],
    [gui.Text('Введите порт для получения', size=DEFAULT_GUI_TEXT_SIZE), gui.InputText(str(port))],
    [gui.Text('Число полученных пакетов', size=DEFAULT_GUI_TEXT_SIZE), gui.Text(key='count')],
    [gui.Text('Скорость соединения', size=DEFAULT_GUI_TEXT_SIZE), gui.Text(key='speed')],
    [gui.Button('Получить')],
])

total = 0
current = 0
left_ms = 0
right_ms = 0

while True:
    event, values = window.read(100)

    if event in (None, 'Exit'):
        break

    try:
        new_host, new_port = values[0], int(values[1])
    except Exception as e:
        print(e)
        continue

    if new_host != host or new_port != port:
        host, port = new_host, new_port
        tcp_socket.close()
        tcp_socket = tcp_socket_init(host, port)
        tcp_socket.listen(1)

    if event == 'Получить':
        current = 0
        left_ms = 0

        recv_tcp_socket = None
        try:
            recv_tcp_socket, _ = tcp_socket.accept()
            total = int(recv_tcp_socket.recv(BATCH_SIZE).decode())
            for i in range(total):
                try:
                    message_time_ms, _ = recv_tcp_socket.recv(BATCH_SIZE).decode().split()
                    current += 1
                    if left_ms == 0:
                        left_ms = int(message_time_ms)
                except socket.timeout:
                    pass
            right_ms = round(datetime.datetime.now().timestamp() * 1000)
        except Exception as e:
            print(e)
        finally:
            if recv_tcp_socket is not None:
                recv_tcp_socket.close()

    total_time_ms = right_ms - left_ms
    speed = 0
    if total_time_ms > 0:
        speed = round(BATCH_SIZE * current / total_time_ms)
    window['speed'].Update(f'{speed} KB/S')
    window['count'].Update(f'{current} of {total}')

tcp_socket.close()
