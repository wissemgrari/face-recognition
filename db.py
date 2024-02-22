import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Global variable to store the connection instance
connection = None

def run_db():

    global connection

    # If a connection already exists, return it
    if connection is not None:
        return connection

    load_dotenv()

    username = os.getenv('DATABASE_USERNAME')
    password = os.getenv('DATABASE_PASSWORD')

    uri = f'mongodb+srv://{username}:{password}@face-recognition.3otruq6.mongodb.net/?retryWrites=true&w=majority&appName=face-recognition'
    client = MongoClient(uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Connected successfully to MongoDB!")
        # Access database 
        connection = client['face-recognition'] 
        return connection
    except Exception as e:
        print(e)
        client.close()
        return None

# Insert a face recognition result into the database
def insert_face(connection, username, encoding, timestamp):
    if connection is None:
        print("Database connection is not established.")
        return

    face_data = {
        "username": username,
        "encoding": encoding.tolist(),  # Convert numpy array to list
        "timestamp": timestamp,
    }
    faces_collection = connection["faces"]
    faces_collection.insert_one(face_data)

# Fetch all the faces from the database
def fetch_faces(connection):
    if connection is None:
        print("Database connection is not established.")
        return None

    faces_collection = connection["faces"]
    faces_data = faces_collection.find()

    return faces_data