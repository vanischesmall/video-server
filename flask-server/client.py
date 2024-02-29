import cv2
import requests
import numpy as np

cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()
    
    # Encode frame as JPEG
    _, buffer = cv2.imencode('.jpg', frame)
    frame_as_jpg = buffer.tobytes()

    # Send frame to Flask server
    response = requests.post("http://localhost:5000/process", 
                             data=frame_as_jpg, 
                             headers={'Content-Type': 'image/jpeg'})
                             
    cv2.waitKey(1)