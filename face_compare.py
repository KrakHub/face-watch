import face_recognition
import cv2
import os
import numpy as np
import tkinter as tkin
import threading
import datetime
import random

imagefile = '/home/kraken/Pictures/unknown.png'
imcap = face_recognition.load_image_file(imagefile)

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
firebaseadmin = firebase_admin.initialize_app(cred, {'databaseURL': 'https://faces-c07d3-default-rtdb.firebaseio.com'})

from firebase_admin import db

Faces = [] #A constant, list of all of the face names
known_faces = []
face_locations = []
face_names = [] #
found_faces = []

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
    ref.set({"Encoding": Encoding.tolist()})

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

#Reads the current video capture, and sets it to RGB format
faces_found = []

face_locations = face_recognition.api.face_locations(imcap) 
face_encodings = face_recognition.api.face_encodings(imcap, face_locations)

face_names=[]
for face_encoding in face_encodings:
    name = CompareFaces(0.35)
    print(name)
    if name == "Unknown":
        name = CompareFaces(0.55)
        print(name)
    face_names.append(name) #face_names will be the names of the faces currently detected
    faces_found.append(face_encoding)


# for (top, right, bottom, left), name, face_encodings in zip(face_locations, face_names, faces_found):
#     boxColor = (0,255,0)
#     if name == "Unknown":
#         boxColor = (0,0,255)

#     cv2.rectangle(imagefile, (left, top), (right, bottom), (boxColor), 2)
#     font = cv2.FONT_HERSHEY_DUPLEX
#     cv2.putText(imagefile, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

# cv2.imshow('Image', imagefile) #Displays the video