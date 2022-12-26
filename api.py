import io
from PIL import Image
from fastapi import FastAPI
import base64
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
import cv2
from calibration import calibrate
import numpy as np
from recognize_main import run_one_time
import json
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
    return buffer


@app.websocket("/ws")
async def get_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            sending_data = {"live": get_video()}
            if data == "Check My seating":
                d = run_one_time(camera)
                # Convert the dictionary to a JSON string
                json_data = json.dumps(d)
                # Convert the JSON string to a bytes object
                bytes_data = bytes(json_data, "utf-8")
                await websocket.send_bytes(bytes_data)
            elif data == "Calibrate":
                success, frame = camera.read()
                calibrate(frame)
            elif data == "ImageComponent":
                print("ImageComponent")

            sending_data["live"] = sending_data["live"].tolist()
            json_data = json.dumps(sending_data)
            # Convert the JSON string to a bytes object
            bytes_data = bytes(json_data, "utf-8")
            await websocket.send_bytes(bytes_data)

    except WebSocketDisconnect:
        camera.release()
        print("Client disconnected")
        await websocket.close()
