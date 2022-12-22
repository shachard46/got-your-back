from time import sleep
import json
import face_recognition
import cv2
import numpy as np


def get_smaller_frame(frame, ratio=0.33):
    small_frame = cv2.resize(frame, None, fx=ratio, fy=ratio)
    return small_frame[:, :, ::-1]


def take_samples(amount, video):
    frames = []
    for i in range(amount):
        ret, frame = video.read()
        # small_frame = get_smaller_frame(frame)
        frames.append(frame)
    return frames


def get_faces_encodings(frames):
    return [face_recognition.face_encodings(frame)[0] for frame in frames]


def get_average_distance(encodings, cal):
    return np.average(face_recognition.face_distance(encodings, cal))


def is_sitting_wrong(tol, dist):
    return dist > tol


video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
img = face_recognition.face_encodings(
    face_recognition.load_image_file('face.jpg'))[0]


def main():
    for i in range(5):
        frames = take_samples(10, video_capture=cv2.VideoCapture(0))
        encodings = get_faces_encodings(frames)
        cal = json.load('')
        wrong = is_sitting_wrong(0.1, get_average_distance(encodings, cal))
        print(wrong)
        sleep(60)
    video_capture.release()


main()
