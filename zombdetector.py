import face_recognition
import cv2
import os
import numpy as np
from sqlalchemy import table

import json

import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate("Programming\Projects\Zombies Among Us\Key.json")
firebase_admin.initialize_app(cred)
    
encond = json.load(***REMOVED***["alex"]: 25***REMOVED***)
ref = db.reference("/")
ref.set(encond)

video_capture = cv2.VideoCapture(0)

path = "Programming\Projects\Zombies Among Us\zombie-library"
AllPics = os.listdir(path)

Faces = []
known_faces = []
face_locations = []
face_names = []
process_currentframe = True

print("LOADING IMAGES")

for v in AllPics:
    imageFile = face_recognition.load_image_file("Programming\Projects\Zombies Among Us\zombie-library\\" + v)
    Encoding = face_recognition.face_encodings(imageFile)[0]
    known_faces.append(Encoding)
    Faces.append(v.rsplit('.', 1)[0])

print("IMAGES HAVE LOADED")

while True:
    ret, frame = video_capture.read()

    rgb_small_frame = frame[:, :, ::-1] 

    if process_currentframe:
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

            face_names.append(name)

    process_currentframe = not process_currentframe

    for (top, right, bottom, left), name in zip(face_locations, face_names):


        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()

# zomblib_detect = face_recognition.load_image_file("Programming\Projects\Zombies Among Us\detect\detect.jpg")
# zombencode_detect = face_recognition.face_encodings(zomblib_detect)[0]

# print("GETTING RESULTS")

# results = face_recognition.compare_faces(known_faces, zombencode_detect)
# index = 0

# for result in results:
#     if result == True:
#         print(Faces[index] + " was included in this picture!")
#     index += 1