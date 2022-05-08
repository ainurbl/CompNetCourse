import socket

import cv2
import numpy as np

img = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
color = (0, 255, 0)
cv2.namedWindow(winname="Server")

HOST = "127.0.0.1"
PORT = 12346

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cv2.imshow("Server", img)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()

while True:
    cv2.imshow("Server", img)
    if cv2.waitKey(10) == 27:
        break
    data = conn.recv(1024)
    if data != b'':
        print(data.decode('ascii'))
        for dat in data.decode('ascii').split(';'):
            if dat == '':
                break
            print(dat)
            ix, iy, x, y = dat.split()
            # print(f'{ix}, {iy}, {x}, {y}')
            cv2.line(img, (int(ix), int(iy)), (int(x), int(y)), color, thickness=5)
conn.close()
cv2.destroyAllWindows()
