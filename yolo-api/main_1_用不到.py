import socket
import struct
import cv2
import numpy as np

HOST = '0.0.0.0'
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print("等待 JetBot 連線中...")

conn, addr = s.accept()
print("已連線：", addr)

data = b""
payload_size = struct.calcsize(">I")

while True:
    # 先收 4 bytes 的影像長度資訊
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_size = data[:payload_size]
    data = data[payload_size:]
    frame_size = struct.unpack(">I", packed_size)[0]

    # 再收完整影像資料
    while len(data) < frame_size:
        data += conn.recv(4096)
    frame_data = data[:frame_size]
    data = data[frame_size:]

    frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
    cv2.imshow("JetBot Stream", frame)

    if cv2.waitKey(1) == 27:
        break

conn.close()
cv2.destroyAllWindows()

