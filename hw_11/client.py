import socket

import cv2
import numpy as np

HOST = "127.0.0.1"
PORT = 12346

img = np.zeros(shape=[512, 512, 3], dtype=np.uint8)

# variables
ix = -1
iy = -1
drawing = False
color = (0, 255, 0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def draw_line(x, y):
    global ix, iy, img
    cv2.line(img, (ix, iy), (x, y), color, thickness=5)
    s.send(f'{ix} {iy} {x} {y};'.encode('ascii'))


def draw_rectangle_with_drag(event, x, y, flags, param):
    global ix, iy, drawing, img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix = x
        iy = y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            draw_line(x, y)
            ix = x
            iy = y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        draw_line(x, y)
        ix = x
        iy = y


cv2.namedWindow(winname="Client")
cv2.setMouseCallback("Client",
                     draw_rectangle_with_drag)

while True:
    cv2.imshow("Client", img)

    if cv2.waitKey(10) == 27:
        break

cv2.destroyAllWindows()
