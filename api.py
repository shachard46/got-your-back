from fastapi import FastAPI
import base64
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket
import cv2
from calibration import calibrate
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
cap = cv2.VideoCapture(0)
# set the width and height of the frame
cap.set(3, 640)
cap.set(4, 480)


@app.get("/calibrate/")
def read_users():
    return calibrate()


@app.get("/image")
def get_image():
    with open("face.jpg", "rb") as f:
        image_data = f.read()
    image_data_base64 = base64.b64encode(image_data).decode('utf-8')
    return {"image": image_data_base64}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    while True:
        # capture a frame from the webcam
        _, frame = cap.read()

        # encode the frame as a Base64 string
        frame_base64 = base64.b64encode(frame).decode('utf-8')

        # send the encoded frame to the client
        await websocket.send_text(frame_base64)
