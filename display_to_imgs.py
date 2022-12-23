import face_recognition
import cv2
import numpy as np
from error_recognition import get_face_distance, get_face_center
# Load the two images
img2 = face_recognition.load_image_file("face.jpg")
img1 = face_recognition.load_image_file("face2.jpg")

# Get the width and height of the images

face_locations1 = face_recognition.face_locations(img1)[0]
face_locations2 = face_recognition.face_locations(img2)[0]
t1, l1, b1, r1 = face_locations1
t2, l2, b2, r2 = face_locations2
print(f'1: {(face_locations1)}')
print(f'2: {(face_locations2)}')
print(f'1: {get_face_center(face_locations1)}')
print(f'2: {get_face_center(face_locations2)}')
print(f'dist: {get_face_distance(get_face_center(face_locations1), get_face_center(face_locations2))}')
cv2.rectangle(img1, (l1, t1), (r1, b1), (0, 0, 255), 2)
cv2.rectangle(img1, (l2, t2), (r2, b2), (0, 0, 255), 2)
# Display the resulting image
cv2.imshow("Two Images", img1)
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
