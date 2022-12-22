import cv2

# Open the webcam
cap = cv2.VideoCapture(0)
frontal_face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml")
profile_face_cascade = cv2.CascadeClassifier("haarcascade_profileface.xml")

while True:
    # Take a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    frontal_faces = frontal_face_cascade.detectMultiScale(gray_frame, 1.3, 5)
    profile_faces = profile_face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    # Iterate over the faces and draw a rectangle around them
    for (x, y, w, h) in frontal_faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        center_x = (x + w)/2
        center_y = (y + h)/2
        if cv2.waitKey(1) & 0xFF == ord("r"):
            center_x == default_x, default_x
    for (x, y, w, h) in profile_faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if cv2.waitKey(1) & 0xFF == ord("5"):
            print(center_x, center_y)

        # cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

    # Display the frame on the screen
    cv2.imshow("Live Video with Face Rectangle", frame)

    # Check if the user pressed the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the webcam
cap.release()

# Close all windows
cv2.destroyAllWindows()
