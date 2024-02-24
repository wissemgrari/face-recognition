from recognition import FaceRecognition
import db
import face_encoder as fe

if __name__ == '__main__':
    # initialize the database connection
    connection = db.run_db()
    # encode the faces
    fe.encode_faces(connection)
    fr = FaceRecognition()
    fr.run_recognition()
