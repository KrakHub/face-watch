from xml.etree.ElementTree import tostring
import face_recognition
import cv2
import os
import numpy as np
from sqlalchemy import table

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("Key.json")
firebaseadmin = firebase_admin.initialize_app(cred, ***REMOVED***'databaseURL': 'https://faces-c07d3-default-rtdb.firebaseio.com'***REMOVED***)

from firebase_admin import db

path = "Upload"
AllPics = os.listdir(path)

print("LOADING IMAGES")

ref = db.reference("/")

ref.set("")

for v in AllPics:
    imageFile = face_recognition.load_image_file("Upload\\" + v)
    Encoding = face_recognition.face_encodings(imageFile)[0]
    # send data to firebase
    ref = db.reference("/" + v.rsplit('.', 1)[0])
    ref.set(***REMOVED***"Encoding": Encoding.tolist()***REMOVED***)
    
print("Done")
