import numpy as np
import socket

def packet(sock, n):

    data = bytearray()
    while len(data) < n:

        pack = sock.recv(n - len(data))
        data.extend(pack)

    return data

def area(b, y, x):

    return b[y-1:y+2, x-1:x+2].flatten()

def maxLen(data):

    onePos, secondPos = None, None

    for y in range(1, data.shape[0] - 1):
        for x in range(1, data.shape[1] - 1):

            v = data[y, x]
            if v < 3: continue

            if any([n > v for n in area(data, y, x)]): continue

            if onePos is None: onePos = (x, y)

            elif secondPos is None: secondPos = (x, y)

            else: break

    return onePos, secondPos

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("84.237.21.36", 5152))

    for i in range(10):

        sock.send(b"get")
        rc = packet(sock, 40002)
        img = np.frombuffer(rc[2:40002], dtype="uint8").reshape(200, 200)
        onePos, secondPos = maxLen(img)
        res = np.sqrt((onePos[0] - secondPos[0]) ** 2 + (onePos[1] - secondPos[1]) ** 2)
        sock.send(f"{res:.1f}".encode())

    sock.send(b"beat")
    print(sock.recv(20).decode())

