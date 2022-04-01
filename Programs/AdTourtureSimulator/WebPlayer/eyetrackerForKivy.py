from gaze_tracking import GazeTracking
import cv2
# import firebase_admin
# from firebase_admin import credentials

# cred = credentials.Certificate("Key.json")
# firebaseadmin = firebase_admin.initialize_app(cred, {'databaseURL': 'https://faces-c07d3-default-rtdb.firebaseio.com'})

# from firebase_admin import db

def runEyetracker():
    return 'Hello World!'


def runEyetrackerForReal():
    process_currentframe = 0
    gaze = GazeTracking()
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()

        if process_currentframe >= 1: 
            process_currentframe = 0

            gaze.refresh(frame)
            frame = gaze.annotated_frame()

            facestatus = ""
            if gaze.is_right():
                facestatus = "Looking right"
            elif gaze.is_left():
                facestatus = "Looking left"
            elif gaze.is_center():
                facestatus = "Looking center"
            elif gaze.is_blinking():
                facestatus = "Blinking"
            return facestatus

        process_currentframe += 20