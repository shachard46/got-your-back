import io
from PIL import Image
from fastapi import FastAPI
import base64
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
import cv2
from calibration import calibrate
import numpy as np
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
try:
    camera = cv2.VideoCapture(0)
    while not camera:
        camera = cv2.VideoCapture(0)
    print(camera)
except:
    print("problem with conection")


def get_video():
    success, frame = camera.read()
    if not success:
        while not success:
            success, frame = camera.read()
        # break
    ret, buffer = cv2.imencode('.jpg', frame)
    return buffer.tobytes()


@app.websocket("/ws")
async def get_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data == "Live":
                await websocket.send_bytes(get_video())
            elif data == "Calibrate":
                success, frame = camera.read()
                calibrate(frame)
            elif data == "ImageComponent":
                print("ImageComponent")
            else:
                await websocket.send_bytes(get_video())

    except WebSocketDisconnect:
        camera.release()
        print("Client disconnected")
