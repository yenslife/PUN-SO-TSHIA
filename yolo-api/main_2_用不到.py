import socket
import struct
import cv2
import numpy as np
from ultralytics import YOLO

HOST = '0.0.0.0'
PORT = 9999

print("載入 YOLO 模型中...")
model = YOLO("./best.pt")  # 你訓練好的模型
print("模型載入完成!")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print("等待 JetBot 連線中...")

conn, addr = s.accept()
print("已連線：", addr)

data = b""
payload_size = struct.calcsize(">I")

while True:
    # 1️⃣ 先接收影像的長度（4 bytes）
    while len(data) < payload_size:
        packet = conn.recv(4096)
        if not packet:
            break
        data += packet

    if len(data) < payload_size:
        break

    packed_size = data[:payload_size]
    data = data[payload_size:]
    frame_size = struct.unpack(">I", packed_size)[0]

    # 2️⃣ 接收完整影像資料
    while len(data) < frame_size:
        data += conn.recv(4096)

    frame_data = data[:frame_size]
    data = data[frame_size:]

    # 3️⃣ 解析成影像
    frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

    if frame is None:
        continue

    # 4️⃣ YOLO 推論
    results = model.predict(frame, conf=0.5, verbose=False)
    annotated_frame = results[0].plot()

    # 5️⃣ 顯示推論結果
    cv2.imshow("YOLO Stream", annotated_frame)
    if cv2.waitKey(1) == 27:  # 按 ESC 離開
        break

conn.close()
cv2.destroyAllWindows()
print("串流結束")

