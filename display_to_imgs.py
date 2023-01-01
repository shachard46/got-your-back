import face_recognition
import cv2
import numpy as np
import json
from face_movment_recognition import Face


# Get the width and height of the images


def get_img_diff(cal: Face, face: Face):
    t1, l1, b1, r1 = cal.get_face_location()
    t2, l2, b2, r2 = face.get_face_location()
    cv2.rectangle(face.frame, (l1, t1), (r1, b1), (0, 0, 255), 2)
    cv2.rectangle(face.frame, (l2, t2), (r2, b2), (0, 0, 255), 2)
    # Display the resulting image
    ret, buffer = cv2.imencode(".jpg", face.frame)
    return json.dumps(buffer.tolist())
