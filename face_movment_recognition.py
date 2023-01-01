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
    def __init__(self, calibration, xy_tolerance, z_tolerance, angle_tolerance, video_capture, faces: list[Face] = []) -> None:
        self.ztol = z_tolerance
        self.atol = angle_tolerance
        self.xytol = xy_tolerance
        self.cal = Face(calibration)
        self.faces: list[Face] = faces
        if faces:
            faces = [face.get_eyes_location() for face in faces]
        self.video_capture = video_capture

    def __take_samples(self, amount):
        try:
            self.faces = [Face(self.video_capture.read()[1])
                          for i in range(amount)]
            self.faces[0].get_eyes_location()
        except:
            self.faces = []

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
        ratio = self.__get_ratio() ** 1.4
        status = {'msg': "Damn Bro", 'pos': ratio}
        if ratio < (1 - self.ztol):
            status["msg"] = "Sit Closer"
        elif ratio > (1 + self.ztol):
            status["msg"] = "Sit Further"
        return status

    def check_xy_movement(self):
        x, y = self.__get_xy_movement()
        x_msg = "Damn Bro"
        y_msg = "Damn Bro"
        if x > self.xytol:
            x_msg = f"Move Right"
        elif x < -self.xytol:
            x_msg = f"Move Left"
        if y > self.xytol:
            y_msg = f"Move Up"
        elif y < -self.xytol:
            y_msg = f"Move Down"
        return ({'msg': x_msg, 'pos': x}, {'msg': y_msg, 'pos': y})

    def check_angle_movement(self):
        angle = self.__get_angle_change()
        status = {'msg': "Damn Bro", 'pos': angle}
        if abs(angle) > self.atol:
            status["msg"] = "Tilt Head Stright"
        return status

    def get_sitting_status(self):
        if not self.faces:
            self.__take_samples(2)
        if self.faces:
            return {'z': self.check_z_movement(),
                    'x': self.check_xy_movement()[0],
                    'y': self.check_xy_movement()[1],
                    'angle': self.check_angle_movement()}
        else:
            return {'msg': "Face Not Found"}
