import cv2
import numpy as np
import socket

cap = cv2.VideoCapture(0)

stoper = 3

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.connect(('192.168.7.1', 12090))

so.sendall(b'M0SL6404<;>L6404')  # just change the L6404 to the number of your engine

bot = False

while True:
    _, frame = cap.read()

    # cv2.rectangle(frame, (640, 580), (480, 400), (0, 0, 255), 15)
    crop_img = frame[400:400 + 80, 260:260 + 210]  # 480 | y, 640 _ x
    crop2 = crop_img

    hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv)
    v += 999999999999999  # brightness
    crop_img = cv2.merge((h, s, v))

    crop_img = cv2.cvtColor(crop_img, cv2.COLOR_HSV2BGR)
    crop = crop_img

    crop_img = cv2.Canny(crop_img, 150, 150)  # edge
    indices = np.where(crop_img != [0])
    coordinates = list(zip(indices[0], indices[1]))

    line = []
    coll = 0
    fline = []
    for i in coordinates:
        if i[0] == coll:
            num = str(np.average(line))
            num = num.strip('[')
            num = num.strip(']')
            num = num.split()
            try:
                fline.append((int(num[0]), coll))
            except:
                pass
            line = []
            coll += 1
            line.append(i)
        else: line.append(i[1])

    for i in fline:
        cv2.rectangle(crop2, i, i, (0, 0, 255), 7)

    new_crop = []
    new_crop2 = []
    for i in fline:
        new_crop.append(i[1])

    coll = 0
    for i in coordinates:
        if i[0] == coll:
            new_crop2.append(i[0])
        else:
            coll += 1

    new_crop = np.average(new_crop)

    new_crop3 = 0
    for i in new_crop2:
        if 50 >= i:
            new_crop3 += 1

    if len(coordinates) < 130:
        stoper = 3
        print('stop 1')
        if bot == True: so.sendall(b'M0A*<;>X')
    elif new_crop == 'nan':
        stoper = 3
        print('stop 2')
        if bot == True: so.sendall(b'M0A*<;>X')
    elif new_crop > 45:
        stoper = 3
        print('stop 3')
        if bot == True: so.sendall(b'M0A*<;>X')
    elif new_crop3 < 35:
        stoper = 3
        print('stop 4')
        if bot == True: so.sendall(b'M0A*<;>X')
    else:
        if stoper != 0:
            stoper -= 1
        else:
            print('go')
            if bot == True: so.sendall(b'M0A*<;>V15')

    cv2.imshow('crop', crop_img)
    cv2.imshow('Original', crop)
    cv2.imshow('orig', crop2)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()