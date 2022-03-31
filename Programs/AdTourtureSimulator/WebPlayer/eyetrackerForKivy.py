from gaze_tracking import GazeTracking
import cv2
import firebase_admin
from firebase_admin import credentials
from sqlalchemy import false

cred = credentials.Certificate("Key.json")
firebaseadmin = firebase_admin.initialize_app(cred, {'databaseURL': 'https://faces-c07d3-default-rtdb.firebaseio.com'})

from firebase_admin import db

gaze = GazeTracking()
video_capture = cv2.VideoCapture(0)

process_currentframe = 0

opened = False

while True:
    ret, frame = video_capture.read()

    if process_currentframe >= 1: 
        process_currentframe = 0

        gaze.refresh(frame)
        frame = gaze.annotated_frame()

        text = ""
        if gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"
        elif gaze.is_blinking():
            text = "Blinking"
        print(text)

    process_currentframe += 1

    cv2.imshow('Video', frame) #Displays the video

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()