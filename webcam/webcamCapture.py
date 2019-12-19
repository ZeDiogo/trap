#pip install opencv-python
import cv2
import time, datetime
from os import path

class webcam:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def capture(self):
        # Check if the webcam is opened correctly
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        return self.cap.read()

    def save(self, frame, filepath):
        # timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
        # filename = "intruder_{}.jpg".format(timestamp)
        filename = "intruder.jpg"
        filepath = path.join(filepath, filename)
        cv2.imwrite(filepath, frame)

    def captureAndSave(self, filepath):
        ret, frame = self.capture()
        self.save(frame, filepath)

    def resize(self, frame, x, y):
        return cv2.resize(frame, (x, y), 1, 1, interpolation=cv2.INTER_AREA)
