import face_recognition
import os, sys
import cv2
import numpy as np
import math
import db


# Helper
def face_confidence(face_distance, face_match_threshold=0.6):
	range = (1.0 - face_match_threshold)
	linear_val = (1.0 - face_distance) / (range * 2.0)

	if face_distance > face_match_threshold:
		return str(round(linear_val * 100, 2)) + '%'
	else:
		value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
		return str(round(value, 2)) + '%'


class FaceRecognition:
	face_locations = []
	face_encodings = []
	face_names = []
	known_face_encodings = []
	known_face_names = []
	process_current_frame = True

	def __init__(self):
		# Load the known faces and face encodings
		database = db.run_db()
		known_faces_data = db.fetch_faces(database)
		
		for face in known_faces_data:
			self.known_face_encodings.append(np.array(face['encoding']))  # Convert the list to a numpy array
			self.known_face_names.append(face['username'])

	def run_recognition(self):
		video_capture = cv2.VideoCapture(0)

		if not video_capture.isOpened():
			sys.exit('Video source not found...')

		while True:
			ret, frame = video_capture.read()

			# Only process every other frame of video to save time
			if self.process_current_frame:
				# Resize frame of video to 1/4 size for faster face recognition processing
				small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

				# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
				rgb_small_frame = small_frame[:, :, ::-1]

				# Find all the faces and face encodings in the current frame of video
				self.face_locations = face_recognition.face_locations(rgb_small_frame)
				self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

				self.face_names = []
				for face_encoding in self.face_encodings:
					# See if the face is a match for the known face(s)
					matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
					name = "Unknown"
					confidence = '???'

					# Calculate the shortest distance to face
					face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

					best_match_index = np.argmin(face_distances)
					if matches[best_match_index]:
						name = self.known_face_names[best_match_index]
						confidence = face_confidence(face_distances[best_match_index])

					self.face_names.append(f'{name} ({confidence})')

			self.process_current_frame = not self.process_current_frame

			# Display the results
			for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
				# represents the top-left corner and he bottom-right corner of rectangle 
				top *= 3
				left *= 4
				bottom *= 4
				right *= 4

				# Create the frame with the name
				if(confidence != '???' and float(confidence.split('%')[0]) > 80):   
					cv2.rectangle(frame, (left, top), (right, bottom), (0, 255 ,0), 2)
					cv2.rectangle(frame, (left, top), (right, top + 30), (0, 255 ,0), cv2.FILLED)
					cv2.putText(frame, name, (left + 6, top + 18), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255 ,255), 2)
				else:
					cv2.rectangle(frame, (left, top), (right, bottom), (0, 0 ,255), 2)
					cv2.rectangle(frame, (left, top), (right, top + 30), (0, 0 ,255), cv2.FILLED)
					cv2.putText(frame, name, (left + 6, top + 18), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255 ,255), 2)

			# Display the resulting image
			cv2.imshow('Face Recognition', frame)

			# Hit 'q' on the keyboard to quit!
			if cv2.waitKey(1) == ord('q'):
				break

		# Release handle to the webcam
		video_capture.release()
		cv2.destroyAllWindows()