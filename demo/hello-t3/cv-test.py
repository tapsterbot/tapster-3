import sys
import cv2 as cv
import math
import time
import numpy as np

cam = cv.VideoCapture(int(sys.argv[1])) #0 is integrated cam, 2 is usb cam
if not cam.isOpened():
    print("Cannot open camera, make sure it is connected to the computer.")
    exit()

#ret, frame = cam.read() #for reading a single frame

def scaleDownFrame(frame):
    template = cv.imread("calc.png", 0)
    f = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    while True:
        cv.imshow("f", f)
        if cv.waitKey(1) == ord('q'): #REQUIRED LINE
            break
    f = cv.matchTemplate(f, template, cv.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(f)
    w, h = template.shape[::-1]
    return frame[max_loc[0]:max_loc[0] + w, max_loc[1]:max_loc[1] + h]

while True:
    ret, frame = cam.read()
    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    frame = scaleDownFrame(frame)
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