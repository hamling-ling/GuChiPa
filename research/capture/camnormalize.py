import cv2.cv as cv
import cv2
import numpy as np


cv.NamedWindow("camera", 1)

capture = cv2.VideoCapture(0)

gamma1 = 0.75
LUT_G1 = np.arange(256, dtype = 'uint8' )
for i in range(256):
    LUT_G1[i] = 255 * pow(float(i) / 255, 1.0 / gamma1)

while True:
    ret,img = capture.read(0)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #gamma=0.001
    #imax = img.max()
    #img = imax * (img/imax)**(1/gamma)

    img = cv2.LUT(img, LUT_G1)
    
    #img = (img-np.mean(img))/np.std(img)*16+25

    cv2.imshow("camera", img)

    if cv.WaitKey(1) > 0:
        break
    
cv2.destroyAllWindows()

    
