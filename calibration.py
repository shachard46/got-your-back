import json
import face_recognition
import cv2
import base64
import numpy as np


def get_webcam_screenshot():
    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Take a single frame from the webcam
    ret, frame = cap.read()

    # Release the webcam
    cap.release()

    # Return the frame as a NumPy array
    return has_face(frame)


def has_face(frame):
    # Convert the frame to a format that the face_recognition library can process
    small_frame = frame[:, :, ::-1]

    # Use the face_locations function to detect faces in the frame
    face_locations = face_recognition.face_locations(small_frame)

    # If the face_locations function returns at least one face, return True
    if len(face_locations) > 0:
        # Convert the frame to a format that the face_recognition library can process
        face_data = {}
        face_data.update({
            "image": small_frame.tolist()
        })
        with open('data.json', 'w') as outfile:
            # Write the dictionary to the file as pretty-printed JSON
            json.dump(face_data, outfile, indent=4)
            return face_data
    else:
        return False


def calibrate():
    status = False
    while not status:
        status = get_webcam_screenshot()

    cap = cv2.VideoCapture(0)

    # Take a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to a JPEG image
    retval, buffer = cv2.imencode('.jpg', frame)

    # Encode the image as a base64 string
    image_b64 = base64.b64encode(buffer).decode()

    # Release the webcam
    cap.release()

    return image_b64


calibrate()
