from PIL import Image, ImageTk
import pyttsx3
from firebase_admin import db
from sqlalchemy import false
from firebase_admin import credentials
import firebase_admin
import cv2
import os
import numpy as np
import tkinter as tkin
import threading
import datetime
import random
import face_recognition


def InitiateLocalDir(inputpath):
    if os.path.isdir(inputpath) != True:
        os.mkdir(inputpath)
        print('Made path ' + str(inputpath) + ', since it does not exist')
        return False
    else:
        return True


cred = credentials.Certificate(***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***)
firebaseadmin = firebase_admin.initialize_app(
    cred, ***REMOVED***'databaseURL': 'https://faces-c07d3-default-rtdb.firebaseio.com'***REMOVED***)


video_capture = cv2.VideoCapture(0)

Faces = []  # A constant, list of all of the face names
known_faces = []
face_locations = []
face_names = []
found_faces = []
greetings = ***REMOVED***
    "morning": ["Good Morning", "How did you sleep", "Good to see you today"],
    "evening": ["Good evening", "Hows your day going", "Nice to finally see you"],
    "night": ["Its getting late", "Goodnight", "Its dark, what are you doing here"]
***REMOVED***
process_currentframe = 0

print("LOADING IMAGES")

ref = db.reference("/")
data = ref.get() or []

#! def old_fb_pull():
#!     for name in data:
#!         ref = db.reference("/" + name)
#!         codes = ref.get()
#!         for discriminator in codes:
#!             encoding = []
#!             print(discriminator)
#!             ref = db.reference("/" + name + "/" + str(discriminator))
#!             code = ref.get()
#!             localfile = open("Cache" + "/" + name + "/" + str(discriminator) + ".enc", "a")
#!             for number in code:
#!                 localfile.write(str(number) + "\n")
#!                 encoding.append(number)
#!             known_faces.append(np.array(encoding))
#!             Faces.append(name)
#!             localfile.close()


def fb_savetocache():
    for name in data:
        ref = db.reference("/" + name)
        codes = ref.get()
        InitiateLocalDir("Cache")
        InitiateLocalDir("Cache" + "/" + name)
        for discriminator in codes:
            ref = db.reference("/" + name + "/" + str(discriminator))
            localref = "Cache" + "/" + name + "/" + str(discriminator) + ".enc"
            code = ref.get()
            if os.path.isfile(localref) != True:
                localfile = open(localref, "a")
                for number in code:
                    localfile.write(str(number) + '\n')
                localfile.close()
            else:
                print('Skipped file ' + localref)


fb_savetocache()


def fb_loadfromcache():
    for name in os.listdir('Cache'):
        print(name)
        for file in os.listdir('Cache/' + name):
            encoding = []
            localfile = open("Cache/" + name + "/" + file, "r").readlines()
            for line in localfile:
                encoding.append(float(line))
            known_faces.append(encoding)
            Faces.append(name)


fb_loadfromcache()


converter = pyttsx3.init()


def SayWords(Text):
    def play():
        converter.setProperty('rate', 200)
        converter.setProperty('volume', 1)
        converter.say(Text)
        converter.runAndWait()

    x = threading.Thread(target=play)
    x.start()


def EncodeFace(input, Encoding):
    # send data to firebase
    if input == "":
        return
    ref = db.reference("/" + input + "/")
    print(input)
    ref.set(***REMOVED***"Encoding": Encoding.tolist()***REMOVED***)

    known_faces.append(Encoding)
    Faces.append(input)
    SayWords("Welcome to the program, " + input + "!")
    window.destroy()


def Greet(name):
    current = datetime.datetime.now()

    morning = current.replace(hour=11, minute=0, second=0, microsecond=0)
    evening = current.replace(hour=16, minute=0, second=0, microsecond=0)
    night = current.replace(hour=23, minute=0, second=0, microsecond=0)

    time = "morning"

    if current < morning:
        time = "morning"
    elif current < evening:
        time = "evening"
    elif current < night:
        time = "night"

    options = greetings[time]
    saying = options[random.randint(0, len(options)-1)]
    SayWords(saying + name)


def CompareFaces(tol):
    match = face_recognition.api.compare_faces(known_faces, face_encoding, tolerance=tol)
    name = "Unknown"
    print("Encoding: " + str(tol))
    face_distances = face_recognition.api.face_distance(known_faces, face_encoding)
    best_match_index = np.argmin(face_distances)
    if match[best_match_index]:
        name = Faces[best_match_index]

        foundInSession = False

        for names in found_faces:
            if names == name:
                foundInSession = True
                break

        if foundInSession == False:
            found_faces.append(name)
            Greet(name)

        ref = db.reference("/" + name)
        data = ref.get()
        getDiscriminator = str(len(data)+1)
        if (getDiscriminator <= str(8)) & (tol == 0.35):
            data["Encoding" + getDiscriminator] = face_encoding.tolist()
            ref.set(data)
            print('Added additional encoding')
    return name


print("IMAGES HAVE LOADED")

opened = False
localfile = open("debug1.txt", "a")
localfile.write(str(known_faces))
localfile.close()
while True:
    # Reads the current video capture, and sets it to RGB format
    ret, frame = video_capture.read()

    rgb_small_frame = frame[:, :, ::-1]
    faces_found = []

    if process_currentframe >= 1:  # The codes only run if the frame is set to be read on
        process_currentframe = 0
        face_locations = face_recognition.api.face_locations(rgb_small_frame)
        face_encodings = face_recognition.api.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            name = CompareFaces(0.35)
            if name == "Unknown":
                print('Face is unknown. Trying agian with a lesser sensitive algorithm...')
                name = CompareFaces(0.55)
                print(name)
            # face_names will be the names of the faces currently detected
            face_names.append(name)
            faces_found.append(face_encoding)

    process_currentframe += 1

    for (top, right, bottom, left), name, face_encodings in zip(face_locations, face_names, faces_found):
        boxColor = (0, 255, 0)
        if name == "Unknown":
            boxColor = (0, 0, 255)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                opened = True
                window = tkin.Tk()
                label = tkin.Label(text="Unknown face detected. Please enter a name you want to save this face as.")
                label.pack()
                unknown_image = ImageTk.PhotoImage(image=Image.fromarray(rgb_small_frame[top:bottom, left:right]))
                label2 = tkin.Canvas(window, width=150, height=150)
                label2.pack()
                label2.create_image(20, 20, anchor="nw", image=unknown_image)
                nameEntry = tkin.Entry()
                nameEntry.pack()
                submitButton = tkin.Button(text="Submit", command=lambda: EncodeFace(nameEntry.get(), face_encodings))
                submitButton.bind("SubmitButton", lambda event: EncodeFace(nameEntry.get(), face_encodings))
                submitButton.pack()
                window.mainloop()

        cv2.rectangle(frame, (left, top), (right, bottom), (boxColor), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    font, 1.0, (0, 255, 0), 1)

    cv2.imshow('Video', frame)  # Displays the video

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
