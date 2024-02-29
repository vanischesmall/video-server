from flask import Flask, request, Response, render_template_string
import cv2
import numpy as np

app = Flask(__name__)

latest_frame = None

@app.route('/process', methods=['POST'])
def process():
    global latest_frame
    
    # Get video frame from client request
    image = request.data
    np_array = np.frombuffer(image, np.uint8)
    frame = cv2.imdecode(np_array, flags=1) 
    
    # Save for video feed
    latest_frame = frame
    
    return "Success"

def gen_frames(): 
    global latest_frame
    
    while True:
        if latest_frame is not None:
            ret, buffer = cv2.imencode('.jpg', latest_frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    
@app.route('/')
def index():
    return render_template_string("""
        <html>
          <body>
            <h1>Video Feed</h1>
            <img src="{{ url_for('video_feed') }}">
          </body>
        </html>
    """)

if __name__ == '__main__':
    app.run(debug=True)