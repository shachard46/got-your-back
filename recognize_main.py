import glob
from time import sleep
import json
import cv2
import numpy as np
from notification import Notification
from face_movment_recognition import FaceMovementRecognition
from display_to_imgs import get_img_diff


def read_calibration_data(path):
    data = {}
    with open(path, 'r') as f:
        data = np.array(json.load(f)['image']).astype('uint8')
    return data


def get_smaller_frame(frame, ratio=0.33):
    small_frame = cv2.resize(frame, None, fx=ratio, fy=ratio)
    return small_frame[:, :, ::-1]


def handle_status(status: dict):
    notification = Notification('alert', '')
    for ax in status.keys():
        if status[ax]:
            # notification.set_message(status[ax])
            # notification.notify()
            print(status[ax])


def check_sitting_status_continusly(camera):
    cal = read_calibration_data('data.json')
    rec = FaceMovementRecognition(cal, 5, 0.2, 10, camera)
    while True:
        status = rec.get_sitting_status()
        handle_status(status)
        sleep(5)


def get_sitting_status(cal, imgs):
    rec = FaceMovementRecognition(cal, 5, 0.3, 10, faces=imgs)
    return rec.get_sitting_status(), get_img_diff(cal, imgs[len(imgs) // 2])


def check_sitting_status(camera):
    cal = read_calibration_data('data.json')
    rec = FaceMovementRecognition(cal, 5, 0.3, 10, camera)
    status = rec.get_sitting_status()
    return status


image_files = list(map(cv2.imread, glob.glob('./Test_image/*.jpg')))
calibration_img = cv2.imread('calibration_img.jpg')
print(get_sitting_status(calibration_img, image_files))
