import chardet
import base64
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
import cv2
import numpy as np
from recognize_main import get_sitting_status
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def decode_photo(str):
    _, encoded_image = str.split(',')
    image_bytes = base64.b64decode(encoded_image)
    image = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


@app.post("/check_my_seating")
async def create_user(request: Request):
    data = await request.json()
    print(data["calibrationPhoto"] != None, data["screenshotList"] != None)

    if data["calibrationPhoto"] != None and data["screenshotList"] != None:
        calibrationPhoto = decode_photo(data["calibrationPhoto"])
        screenshotList = map(decode_photo, data["screenshotList"])
        res = get_sitting_status(calibrationPhoto, screenshotList)[0]
        print(res)
        return res
