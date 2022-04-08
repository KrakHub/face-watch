from gaze_tracking import GazeTracking
from threading import *
import cv2
import os
import yt_dlp as ydl
import PyQt5
import PyQt5.QtWidgets as Qtw
import sys
# import firebase_admin
# from firebase_admin import credentials

# cred = credentials.Certificate("Key.json")
# firebaseadmin = firebase_admin.initialize_app(cred, {'databaseURL': 'https://faces-c07d3-default-rtdb.firebaseio.com'})

# from firebase_admin import db

text = ''

if os.path.exists('Programs/AdTourtureSimulator/resources/'):
    print('Directory Found')
else:
    os.mkdir('Programs/AdTourtureSimulator/resources/')
    print('Makde resources directory, since it doesn\'t exist.')
if os.path.exists('Programs/AdTourtureSimulator/resources/Delivery Dance-G-T3qKl6y-c.webm'):
    print('Videos are already downloaded. Skipping...')
else:
    ydloption = {
        'format':'bestvideo+bestaudio/best',
        'outtmpl':'Programs/AdTourtureSimulator/resources/%(title)s-%(id)s.%(ext)s'
    }
    ydl.YoutubeDL(ydloption).download(['https://www.youtube.com/watch?v=G-T3qKl6y-c'])
    
text = 'Placeholder'

def main():
    app = Qtw.QApplication(sys.argv)
    qtWindow = Qtw.QWidget()
    qtWindow.resize(250, 150)
    qtWindow.move(300, 300)
    qtWindow.setWindowTitle('Window')
    qtWindow.show()
    sys.exit(app.exec_())
    
def runEyetrackerForReal():
    process_currentframe = 0
    gaze = GazeTracking()
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()

        if process_currentframe >= 20: 
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

if __name__ == "__main__":
    main()

