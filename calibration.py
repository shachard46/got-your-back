import numpy as np
import base64
import json
import face_recognition
import cv2


def get_webcam_screenshot(frame):
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


def calibrate(frame):
    status = False
    while not status:
        status = has_face(frame)
    print("Done Calibrate")
