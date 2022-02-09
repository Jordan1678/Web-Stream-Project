import time
import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    cap = cv2.VideoCapture(0)


    # Read until video is completed
    while (cap.isOpened()):

        start = time.time()
        # Capture frame-by-frame
        ret, img = cap.read()
        if ret == True:
            img = cv2.resize(img, (0, 0), fx=1, fy=1)
            cv2.line(img, (40, 30), (20, 50), (255, 0, 0), 50)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            end = time.time()

            fps = end-start
            print(int(1/fps))

        else:
            break


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host="0.0.0.0", port=80)
