from time import sleep
import json
import cv2
import numpy as np
from notification import Notification
import math
from face_movment_recognition import FaceMovementRecognition


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


def main():
    cal = read_calibration_data('data.json')
    rec = FaceMovementRecognition(cal, 5, 0.2, 10, camera)
    while True:
        status = rec.is_sitting_wrong()
        handle_status(status)
        sleep(5)


def run_one_time(camera):
    cal = read_calibration_data('data.json')
    rec = FaceMovementRecognition(cal, 5, 0.3, 10, camera)
    status = rec.is_sitting_wrong()
    return status
    # print(status)
    # handle_status(status)


# camera = cv2.VideoCapture(0)


# run_one_time(camera)
# main()
