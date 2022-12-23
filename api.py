import base64
import cv2
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from calibration import calibrate
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/calibrate/")
def read_users():
    return calibrate()


@app.get("/screenshot")
def get_screenshot():
    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Take a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to a JPEG image
    retval, buffer = cv2.imencode('.jpg', frame)

    # Encode the image as a base64 string
    image_b64 = base64.b64encode(buffer).decode()

    # Release the webcam
    cap.release()

    # Return the image as a response
    return image_b64


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        cap = cv2.VideoCapture(0)

        # Take a frame from the webcam
        ret, frame = cap.read()

        # Convert the frame to a JPEG image
        retval, buffer = cv2.imencode('.jpg', frame)

        # Encode the image as a base64 string
        image_b64 = base64.b64encode(buffer).decode()

        # Release the webcam
        cap.release()

        # Return the image as a response
        # return image_b64
        print(image_b64[0:10])
        await websocket.send_text(image_b64)
