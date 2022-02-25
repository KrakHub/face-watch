import face_recognition
import os

from sqlalchemy import table

path = "Programming\Projects\Zombies Among Us\zombie-library"
AllPics = os.listdir(path)

Faces = []
known_faces = []

print("LOADING IMAGES")

for v in AllPics:
    imageFile = face_recognition.load_image_file("Programming\Projects\Zombies Among Us\zombie-library\\" + v)
    Encoding = face_recognition.face_encodings(imageFile)[0]
    known_faces.append(Encoding)
    Faces.append(v.rsplit('.', 1)[0])

print("IMAGES HAVE LOADED")

zomblib_detect = face_recognition.load_image_file("Programming\Projects\Zombies Among Us\detect\detect.jpg")
zombencode_detect = face_recognition.face_encodings(zomblib_detect)[0]

print("GETTING RESULTS")

results = face_recognition.compare_faces(known_faces, zombencode_detect)
index = 0

for result in results:
    if result == True:
        print(Faces[index] + " was included in this picture!")
    index += 1