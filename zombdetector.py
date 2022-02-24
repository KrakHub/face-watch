import face_recognition

zomblib_joeBiden = face_recognition.load_image_file("Programming\Projects\Zombies Among Us\zombie-library\Joe Biden.jpg")
zomblib_donaldTrump = face_recognition.load_image_file("Programming\Projects\Zombies Among Us\zombie-library\Donald Trump.jpg")
zomblib_kimUn = face_recognition.load_image_file("Programming\Projects\Zombies Among Us\zombie-library\Kim Jong Un.jpg")
zomblib_vladimirPutin = face_recognition.load_image_file("Programming\Projects\Zombies Among Us\zombie-library\Vladimir Putin.jpg")

zomblib_detect = face_recognition.load_image_file("Programming\Projects\Zombies Among Us\detect\detect.jpg")

try:
    zombencode_joeBiden = face_recognition.face_encodings(zomblib_joeBiden)[0]
    zombencode_donaldTrump = face_recognition.face_encodings(zomblib_donaldTrump)[0]
    zombencode_kimUn = face_recognition.face_encodings(zomblib_kimUn)[0]
    zombencode_vladimirPutin = face_recognition.face_encodings(zomblib_vladimirPutin)[0]

    zombencode_detect = face_recognition.face_encodings(zomblib_detect)[0]
except IndexError:
    print('Error')
    quit()

known_faces = [
    zombencode_donaldTrump,
    zombencode_joeBiden,
    zombencode_kimUn,
    zombencode_vladimirPutin
]

results = face_recognition.compare_faces(known_faces, zombencode_detect)

print(results[0])
