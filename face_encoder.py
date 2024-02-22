import os
import face_recognition
import datetime
import db

def encode_faces(connection):
  # load images from the faces directory
  #TODO: build a web UI to upload images
  for image in os.listdir('faces'):
    face_image = face_recognition.load_image_file(f"faces/{image}")
    face_encoding = face_recognition.face_encodings(face_image)[0]
    timestamp = datetime.datetime.now()
    username = image.split('.')[0]
    db.insert_face(connection, username, face_encoding, timestamp)
    print(f"Encoded {username} face and inserted into the database.")