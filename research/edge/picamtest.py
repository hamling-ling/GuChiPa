import io
import picamera
import cv2

import numpy as np

stream = io.BytesIO()

CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

with picamera.PiCamera() as camera:
    camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
    camera.capture(stream, format='jpeg')
    data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    image = cv2.imdecode(data, 1)
    cv2.imshow('image',image)
    cv2.waitKey(0)
