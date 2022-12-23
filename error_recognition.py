from time import sleep
import json
import face_recognition
import cv2
import numpy as np
from notiffitction import nottfitcation


def get_smaller_frame(frame, ratio=0.33):
    small_frame = cv2.resize(frame, None, fx=ratio, fy=ratio)
    return small_frame[:, :, ::-1]


def take_samples(amount):
    frames = []
    video_capture = cv2.VideoCapture(0)
    frames = [video_capture.read()[1] for i in range(amount)]
    # small_frame = get_smaller_frame(frame)
    video_capture.release()
    return frames


def get_faces_locations(frames):
    return [face_recognition.face_locations(frame)[0] for frame in frames
            if face_recognition.face_locations(frame)]


def get_face_center(location):
    t, r, b, l = location
    return np.array([(r - l) / 2, (t - b) / 2])


def get_face_distance(face, cal):
    return np.linalg.norm(face - cal)


def get_average_distance(locations, cal):
    locations = [get_face_center(location) for location in locations]
    cal = get_face_center(cal)
    return np.average([get_face_distance(location, cal) for location in locations])


def is_sitting_wrong(tol, cal):
    frames = take_samples(10)
    locations = get_faces_locations(frames)
    cal = read_json(cal)
    dist = get_average_distance(locations, cal)
    return dist > tol


def read_json(path):
    data = {}
    with open(path, 'r') as f:
        data = np.array(json.load(f)['position'])
    return data


def main():
    while True:
        if is_sitting_wrong(4, "data.json"):
            nottfitcation("Alert", "Chaing position")
        else:
            nottfitcation("Good", "Cool cool cool")
        sleep(10)


main()
