import json
import socket
import cv2
import struct
import numpy as np
import time
from jetbot import Camera

HOST = "192.168.0.183"  # Mac 的 IP
PORT = 9999

# camera = Camera()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("已連上 Mac!")

try:
    while True:
        frame = camera.value  # numpy array，格式是 HxWx3 (RGB)

        # OpenCV 使用 BGR，因此先轉換格式
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # 壓縮 JPEG，節省網路壓力
        _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        data = buffer.tobytes()

        # 發送資料大小 + 影像資料
        s.sendall(struct.pack(">I", len(data)) + data)
        
        # 接收推論結果 這邊也就是我們撰寫前後左右邏輯的地方
        try:
            result = s.recv(4096).decode().strip()
            result_obj = json.loads(result)
            detections = result_obj.get("detections")
            if result and len(detections) != 0:
                print("YOLO:", result)
                move_robot(detections)

        except Exception as e:
            print(f"error: {e}")
            pass

        time.sleep(0.01)

except Exception as e:
    print(f"停止串流: {e}")

finally:
    camera.stop()
    s.close()

