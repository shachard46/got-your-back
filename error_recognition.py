from time import sleep
import json
import face_recognition
import cv2
import numpy as np
from notification import Notification


class FaceMovementRecognition:
    def __init__(self, calibration, xy_tolerance, z_tolerance=0.4) -> None:
        self.ztol = z_tolerance
        self.xytol = xy_tolerance
        self.cal = calibration

    def __take_samples(self, amount):
        self.video_capture = cv2.VideoCapture(0)
        frames = [self.video_capture.read()[1] for i in range(amount)]
        self.video_capture.release()
        return frames

    def __get_faces_locations(self, frames):
        return [face_recognition.face_locations(frame)[0] for frame in frames
                if face_recognition.face_locations(frame)]

    def __get_average_differance(self, locations, compute, get_diff, avg):
        locations = [compute(location) for location in locations]
        d_cal = compute(self.cal)
        return avg([get_diff(location, d_cal) for location in locations])

    def __get_average_distance(self, locations):
        return self.__get_average_differance(locations, FaceMovementRecognition.__get_face_center,
                                             FaceMovementRecognition.get_face_distance, lambda lists:
                                                 [sum(lists[i][j] for i in range(len(lists))) / len(lists) for j in range(len(lists[0]))])

    def __get_average_ratio(self, locations):
        return self.__get_average_differance(locations, FaceMovementRecognition.__get_rect_size,
                                             lambda a, b: a / b, np.average)

    def check_z_movement(self, locations):
        ratio = self.__get_average_ratio(locations)
        print(ratio)
        if ratio < (1 - self.ztol):
            return "Sit Closer"
        if ratio > (1 + self.ztol):
            return "Sit Further"
        return "Damn You Good"

    def check_xy_movement(self, locations):
        x, y = self.__get_average_distance(locations)
        print(x, y)
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

    def is_sitting_wrong(self):
        frames = self.__take_samples(10)
        locations = self.__get_faces_locations(frames)
        return {'z': self.check_z_movement(locations),
                'x': self.check_xy_movement(locations)[0],
                'y': self.check_xy_movement(locations)[1]}

    @staticmethod
    def __get_face_center(location):
        t, r, b, l = location
        return np.array([(r - l) / 2, (t - b) / 2])

    @staticmethod
    def __get_rect_size(location):
        t, r, b, l = location
        return abs(r - l) * abs(t - b)

    @staticmethod
    def get_face_distance(face1, face2):
        return [f1 - f2 for f1, f2 in zip(face1, face2)]


def read_calibration_data(path):
    data = {}
    with open(path, 'r') as f:
        data = np.array(json.load(f)['position'])
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
    rec = FaceMovementRecognition(cal, 20, 0.2)
    while True:
        status = rec.is_sitting_wrong()
        handle_status(status)
        sleep(10)


main()
