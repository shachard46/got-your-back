from time import sleep
import json
import face_recognition
import cv2
import numpy as np
from notification import Notification
import math


def get_center(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return np.array([(x1 - x2) / 2, (y1 - y2) / 2])


def get_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


class Face:
    def __init__(self, frame) -> None:
        self.frame = frame

    def get_face_location(self):
        locations = face_recognition.face_locations(self.frame)
        return locations[0] if locations else None

    def get_eyes_location(self):
        face_landmarks = face_recognition.face_landmarks(self.frame)
        left_eye = face_landmarks[0]["left_eye"]
        right_eye = face_landmarks[0]["right_eye"]
        left_eye_center = (sum(x[0] for x in left_eye) // len(left_eye),
                           sum(x[1] for x in left_eye) // len(left_eye))

        right_eye_center = (sum(x[0] for x in right_eye) // len(right_eye),
                            sum(x[1] for x in right_eye) // len(right_eye))
        return left_eye_center, right_eye_center

    def get_face_angle(self):
        l, r = self.get_eyes_location()
        x1, y1 = l
        x2, y2 = r
        return math.degrees(math.atan2(y2 - y1, x2 - x1))

    def get_eyes_distance(self):
        left, right = self.get_eyes_location()
        return get_distance(left, right)

    def get_face_center(self):
        t, r, b, l = self.get_face_location()
        return get_center((l, t), (r, b))

    def get_eyes_center(self):
        left_eye, right_eye = self.get_eyes_location()
        return get_center(left_eye, right_eye)


class FaceMovementRecognition:
    def __init__(self, calibration, xy_tolerance, z_tolerance, angle_tolerance) -> None:
        self.ztol = z_tolerance
        self.atol = angle_tolerance
        self.xytol = xy_tolerance
        self.cal = Face(calibration)
        self.faces: list[Face] = []

    def __take_samples(self, amount):
        self.video_capture = cv2.VideoCapture(0)
        try:
            self.faces = [Face(self.video_capture.read()[1])
                          for i in range(amount)]
            self.faces[0].get_eyes_location()
        except:
            self.faces = []
        self.video_capture.release()

    def __get_avg_eyes_center(self):
        faces = [face.get_eyes_center() for face in self.faces]
        return [sum(faces[i][j] for i in range(len(faces))) / len(faces)
                for j in range(len(faces[0]))]

    def __get_avg_eyes_distance(self):
        return np.average([face.get_eyes_distance() for face in self.faces])

    def __get_avg_face_angle(self):
        return np.average([face.get_face_angle() for face in self.faces])

    def __get_ratio(self):
        return self.__get_avg_eyes_distance() / self.cal.get_eyes_distance()

    def __get_xy_movement(self):
        eye_center = self.__get_avg_eyes_center()
        x, y = (eye_center[i] - self.cal.get_eyes_center()[i]
                for i in range(len(eye_center)))
        return x, y

    def __get_angle_change(self):
        return self.__get_avg_face_angle() - self.cal.get_face_angle()

    def check_z_movement(self):
        ratio = self.__get_ratio()
        if ratio < (1 - self.ztol):
            return "Sit Closer"
        if ratio > (1 + self.ztol):
            return "Sit Further"
        return "Damn You Good"

    def check_xy_movement(self):
        x, y = self.__get_xy_movement()
        x_msg = None
        y_msg = None
        if x > self.xytol:
            x_msg = f"Move Right"
        elif x < -self.xytol:
            x_msg = f"Move Left"
        if y > self.xytol:
            y_msg = f"Move Up"
        elif y < self.xytol:
            y_msg = f"Move Down"
        return (x_msg, y_msg) if x_msg and y_msg else ("Damn Bro", "Damn Bro")

    def check_angle_movement(self):
        angle = self.__get_angle_change()
        if abs(angle) > self.atol:
            return "Tilt Head Stright"
        else:
            return "Damn Bro"

    def is_sitting_wrong(self):
        self.__take_samples(10)
        if self.faces:
            return {'z': self.check_z_movement(),
                    'x': self.check_xy_movement()[0],
                    'y': self.check_xy_movement()[1],
                    'angle': self.check_angle_movement()}
        else:
            return {'bad': "Face Not Found"}


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
    rec = FaceMovementRecognition(cal, 20, 0.2, 10)
    while True:
        status = rec.is_sitting_wrong()
        handle_status(status)
        sleep(10)


main()
