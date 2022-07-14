import sys
import os
import cv2 as cv
import math
import time
import numpy as np

cam = cv.VideoCapture(int(sys.argv[1])) #0 is integrated cam, 2 is usb cam
if not cam.isOpened():
    print("Cannot open camera, make sure it is connected to the computer.")
    exit()

#ret, frame = cam.read() #for reading a single frame

def scaleDownFrame(frame, templatePath):
    template = cv.imread(templatePath, 0)
    #print(str(frame.shape) + " " + str(template.shape))
    if template.shape[0] > frame.shape[0] or template.shape[1] > frame.shape[1]:
        print("Your template image is larger than your source. Please resize your image, or see ../dev-notes.txt for help.")
        exit()
    frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    res = cv.matchTemplate(frame, template, cv.TM_CCOEFF_NORMED) #outputs a probability matrix, NOT an image
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    x, y = max_loc
    h, w = template.shape
    cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
    #print(str(x) + "," + str(y) + " ; " + str(x+w) + "," + str(y+h))
    return frame#[y:y + h, x:x + w]

while True:
    ret, frame = cam.read()
    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    #frame = frame[:, 60:415] #crop to get rid of extra space on the sides of frame, helps a bit with accuracy
    frame = scaleDownFrame(frame, "calc-screen.jpg")
    #imgray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #frame = cv.Canny(frame, 100, 150)
    #ret, thresh = cv.threshold(imgray, 145, 255, 0)
    #contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #frame = cv.drawContours(frame, contours, -1, (0,255,0), 3)
    
    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'): #REQUIRED LINE
        break

cam.release()
cv.destroyAllWindows()