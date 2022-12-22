import json
import face_recognition
import cv2


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
        face_data = {}
        for (top, right, bottom, left) in face_locations:
            face_encodings = face_recognition.face_encodings(
                frame, face_locations)
            print(face_encodings[0])
            # Get the face encoding for the face
            # Store the position and encoding data for the face in a dictionary
            face_data.update({
                "position": [top, right, bottom, left],
                "encoding": list(face_encodings[0])
            })
        with open('data.json', 'w') as outfile:
            # Write the dictionary to the file as pretty-printed JSON
            json.dump(face_data, outfile, indent=4)
        return face_data
    else:
        return False


status = True
while status == True:
    status = get_webcam_screenshot()
    print(status == True)

print("data saved")
