#from xml.etree.ElementTree import tostring
import face_recognition
import cv2
import os
import numpy as np
import tkinter as tkin
#from sqlalchemy import null, table
import threading

from PIL import Image, ImageTk

import firebase_admin
from firebase_admin import credentials
from sqlalchemy import false

cred = credentials.Certificate("Key.json")
firebaseadmin = firebase_admin.initialize_app(cred, {'databaseURL': 'https://faces-c07d3-default-rtdb.firebaseio.com'})

from firebase_admin import db

video_capture = cv2.VideoCapture(0)

#path = "Programming\Projects\Zombies Among Us\zombie-library"
#AllPics = os.listdir(path)

Faces = [] #A constant, list of all of the face names
known_faces = []
face_locations = []
face_names = [] #
found_faces = []
process_currentframe = 0

print("LOADING IMAGES")

ref = db.reference("/")
data = ref.get() or []

for name in data:
    encoding = []
    ref = db.reference("/" + name + "/Encoding")
    code = ref.get()
    for number in code:
        encoding.append(number)
    known_faces.append(np.array(encoding))
    Faces.append(name)

from gtts import gTTS
import playsound

def SayWords(Text):
    def play():
        playsound.playsound(Text+'.mp3')
        os.remove(Text+'.mp3')
    myobj = gTTS(text=Text, lang='en', slow=False)
    myobj.save(Text+'.mp3')
    x = threading.Thread(target=play)
    x.start()


def EncodeFace(input, Encoding):
    # send data to firebase
    if input == "":
        return
    ref = db.reference("/" + input)
    print(input)
    ref.set({"Encoding": Encoding.tolist()})

    known_faces.append(Encoding)
    Faces.append(input)
    SayWords("Welcome to the program, " + input + "!")
    window.destroy()



print("IMAGES HAVE LOADED")

opened = False

while True:
    #Reads the current video capture, and sets it to RGB format
    ret, frame = video_capture.read()

    rgb_small_frame = frame[:, :, ::-1] 
    faces_found = []

    if process_currentframe >= 1: #The codes only run if the frame is set to be read on
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

                found = False

                for names in found_faces:
                    if names == name:
                        found = True
                        break
                
                if found == False:
                    found_faces.append(name)
                    SayWords("Goodmorning " + name + "!")

            
            face_names.append(name) #face_names will be the names of the faces currently detected
            faces_found.append(face_encoding)

    process_currentframe += 1

    for (top, right, bottom, left), name, face_encodings in zip(face_locations, face_names, faces_found):
        if name == "Unknown":
            opened = True
            window = tkin.Tk()
            label = tkin.Label(text="Unknown face detected. Please enter a name you want to save this face as.")
            label.pack()
            unknown_image =  ImageTk.PhotoImage(image=Image.fromarray(rgb_small_frame[top:bottom, left:right]))
            label2 = tkin.Canvas(window, width= 150, height=150)
            label2.pack()
            label2.create_image(20,20, anchor="nw", image=unknown_image)
            nameEntry = tkin.Entry()
            nameEntry.pack()
            submitButton = tkin.Button(text="Submit", command=lambda:EncodeFace(nameEntry.get(), face_encodings))
            submitButton.bind("SubmitButton", lambda event:EncodeFace(nameEntry.get(), face_encodings))
            submitButton.pack()
            #cv2.imshow("Image", frame[top:left, bottom:right])
            window.mainloop()

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