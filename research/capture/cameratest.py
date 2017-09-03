import cv2.cv as cv
import cv2
import time

cv.NamedWindow("camera", 1)

capture = cv2.VideoCapture(0)

while True:
    ret,img = capture.read(0)
    cv2.imshow("camera", img)

    if cv.WaitKey(10) > 0:
        break
cv2.destroyAllWindows()

    
