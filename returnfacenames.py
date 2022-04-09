import face_recognition
import cv2
import os
import numpy as np
import tkinter as tkin
import threading
import datetime
import random

def InitiateLocalDir(inputpath):
    if os.path.isdir(inputpath)!=True:
        os.mkdir(inputpath)
        print('Made path ' + str(inputpath) + ', since it does not exist')
        return False
    else: return True

from PIL import Image, ImageTk

import firebase_admin
from firebase_admin import credentials
from sqlalchemy import false

cred = credentials.Certificate("Key.json")
firebaseadmin = firebase_admin.initialize_app(cred, ***REMOVED***'databaseURL': 'https://faces-c07d3-default-rtdb.firebaseio.com'***REMOVED***)

from firebase_admin import db

video_capture = cv2.VideoCapture(0)

Faces = [] #A constant, list of all of the face names
known_faces = []
face_locations = []
face_names = [] #
found_faces = []
process_currentframe = 0

print("LOADING IMAGES")

ref = db.reference("/")
data = ref.get() or []

def name_function():
    for name in data:
        ref = db.reference("/" + name)
        codes = ref.get()
        for discriminator in codes:
            encoding = []
            ref = db.reference("/" + name + "/" + str(discriminator))
            code = ref.get()
            for number in code:
                encoding.append(number)
            known_faces.append(np.array(encoding))
            Faces.append(name)
name_function()

def EncodeFace(input, Encoding):
    # send data to firebase
    if input == "":
        return
    ref = db.reference("/" + input + "/")
    print(input)
    ref.set(***REMOVED***"Encoding": Encoding.tolist()***REMOVED***)

    known_faces.append(Encoding)
    Faces.append(input)

def CompareFaces(tol):
    match = face_recognition.api.compare_faces(known_faces, face_encoding, tolerance=tol)
    name = "Unknown"
    face_distances = face_recognition.api.face_distance(known_faces, face_encoding)
    best_match_index = np.argmin(face_distances)
    if match[best_match_index]:
        name = Faces[best_match_index]
        ref = db.reference("/" + name)
        data = ref.get()
        getDiscriminator = str(len(data)+1)
        if getDiscriminator <= str(8):
            data["Encoding" + getDiscriminator] = face_encoding.tolist()
            ref.set(data)
    return name

print("IMAGES HAVE LOADED")

opened = False

while True:
    #Reads the current video capture, and sets it to RGB format
    ret, frame = video_capture.read()

    rgb_small_frame = frame[:, :, ::-1] 
    faces_found = []

    if process_currentframe >= 1: #The codes only run if the frame is set to be read on
        process_currentframe = 0
        face_locations = face_recognition.api.face_locations(rgb_small_frame) 
        face_encodings = face_recognition.api.face_encodings(rgb_small_frame, face_locations)

        face_names=[]
        for face_encoding in face_encodings:
            name = CompareFaces(0.35)
            if name == "Unknown":
                name = CompareFaces(0.55)
            face_names.append(name) #face_names will be the names of the faces currently detected
            print(face_names)
            faces_found.append(face_encoding)

    process_currentframe += 1