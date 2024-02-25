import cv2
from tkinter import *
from PIL import Image, ImageTk

# Open the camera
video_capture = cv2.VideoCapture(0)

# Function to get the current frame from the video feed
def get_frame():
    ret, frame = video_capture.read()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA), frame.shape

# Create a window
frame, shape = get_frame()
window = Tk()
window.title("Face capture")
window.geometry(f'{shape[1]}x{shape[0]}')  # Set the window size to the frame size

# Create a canvas for the video feed
canvas = Canvas(window, width = shape[1], height = shape[0])
canvas.pack()

# Global variable to store the image
imgtk = None

# Function to update the video feed
def update_image():
    global imgtk
    frame, _ = get_frame()  # Ignore the shape
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    canvas.create_image(0, 0, anchor=NW, image=imgtk)
    window.after(1, update_image)

# Create an text field to enter the name of the person
entry = Entry(window)
entry_height = 40
entry.place(x=0, y=shape[0] - entry_height, width=shape[1] - 150, height=entry_height)
# create placeholder
entry.insert(0, 'Enter your name')
# remove placeholder when clicked
entry.bind("<Button-1>", lambda event: entry.delete(0, "end"))
entry.config(font=("Arial", 12))
entry.config(bd=3)


# Create a button to capture an image
btn = Button(window, text="Capture")
btn_width = 150
btn_height = 40
btn.place(x=shape[1] - 150, y=shape[0] - btn_height, width=btn_width, height=btn_height)
btn.config(font=("Arial", 12))
btn.config(bd=3)

# Function to capture an image
def capture_image():
    frame, _ = get_frame()
    filename = entry.get()
    if filename:  # Check if the entry is not empty
        filename = 'captures/' + filename + '.jpg'
    else:  # If the entry is empty, use a default filename
        filename = 'captures/captured_image.jpg'
    cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR))

# Assign the capture_image function to the button's command
btn.config(command=capture_image)

# Start the video feed
update_image()

# Start the Tkinter event loop
window.mainloop()

# Release the camera when the window is closed
video_capture.release()