from xml.etree.ElementTree import tostring
import face_recognition
import cv2
import os
import numpy as np
import tkinter as tkin
from sqlalchemy import table

from PIL import Image

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("Key.json")
firebaseadmin = firebase_admin.initialize_app(cred, ***REMOVED***'databaseURL': 'https://faces-c07d3-default-rtdb.firebaseio.com'***REMOVED***)

from firebase_admin import db

video_capture = cv2.VideoCapture(0)

#path = "Programming\Projects\Zombies Among Us\zombie-library"
#AllPics = os.listdir(path)

Faces = [] #A constant, list of all of the face names
known_faces = []
face_locations = []
face_names = [] #
process_currentframe = 0

print("LOADING IMAGES")

ref = db.reference("/")
data = ref.get()

for name in data:
    encoding = []
    ref = db.reference("/" + name + "/Encoding")
    code = ref.get()
    for number in code:
        encoding.append(number)
    known_faces.append(np.array(encoding))
    Faces.append(name)

#!for v in AllPics:
    #!imageFile = face_recognition.load_image_file("Programming\Projects\Zombies Among Us\zombie-library\\" + v)
    #!Encoding = face_recognition.face_encodings(imageFile)[0]
    #!known_faces.append(Encoding)
    #! send data to firebase
    #!ref = db.reference("/" + v.rsplit('.', 1)[0])
    #!print(Encoding)
    #!ref.set(***REMOVED***"Encoding": Encoding.tolist()***REMOVED***)
    #!Faces.append(v.rsplit('.', 1)[0])

print("IMAGES HAVE LOADED")

opened = False

while True:
    #Reads the current video capture, and sets it to RGB format
    ret, frame = video_capture.read()

    rgb_small_frame = frame[:, :, ::-1] 
    
    if process_currentframe == 3: #The codes only run if the frame is set to be read on
        process_currentframe = 0
        face_locations = face_recognition.face_locations(rgb_small_frame) 
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names=[]
        for face_encoding in face_encodings:
            match = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_faces, face_encoding)
            best_match_index = np.argmin(face_distances)
            if match[best_match_index]:
                name = Faces[best_match_index]
            
            face_names.append(name) #face_names will be the names of the faces currently detected

    process_currentframe += 1

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if name == "Unknown":
            ##window = tkin.Tk()
            #label = tkin.Label(text="Unknown face detected. Please enter a name you want to save this face as.")
            #label.pack()
            cv2.imshow("Image", frame[top:left, bottom:right])
            ##window.mainloop()

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame) #Displays the video

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()

#! zomblib_detect = face_recognition.load_image_file("Programming\Projects\Zombies Among Us\detect\detect.jpg")
#! zombencode_detect = face_recognition.face_encodings(zomblib_detect)[0]

#! print("GETTING RESULTS")

#! results = face_recognition.compare_faces(known_faces, zombencode_detect)
#! index = 0

#! for result in results:
#!     if result == True:
#!         print(Faces[index] + " was included in this picture!")
#!     index += 1