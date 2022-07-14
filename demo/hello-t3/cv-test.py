import sys
import os
import cv2 as cv
import math
import statistics
import time
import numpy as np
import pytesseract
from imutils.object_detection import non_max_suppression

cam = cv.VideoCapture(int(sys.argv[1])) #0 is integrated cam, 2 is usb cam
if not cam.isOpened():
    print("Cannot open camera, make sure it is connected to the computer.")
    exit()

def scaleDownFrame(frame, templatePath):
    template = cv.imread(templatePath, 0)
    if template.shape[0] > frame.shape[0] or template.shape[1] > frame.shape[1]:
        print("Your template image is larger than your source. Please resize your image, or see ../dev-notes.txt for help.")
        exit()
    frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    res = cv.matchTemplate(frame, template, cv.TM_CCOEFF_NORMED) #outputs a probability matrix, NOT an image
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    x, y = max_loc
    h, w = template.shape
    cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
    return frame[y:y + h, x:x + w]

def preProcessImage(frame):
    # Blur the image
    #frame = cv.GaussianBlur(frame,(13,13), 0)
    # Edge detection
    #frame = cv.Canny(frame, 100, 200)
    #res, frame = cv.threshold(frame, 100, 255 , cv.THRESH_BINARY)
    #frame = cv.GaussianBlur(frame, (5, 5), 0)
    ret, frame = cv.threshold(frame, 45, 255, cv.THRESH_BINARY)
    frame = cv.erode(frame, np.ones((2, 2), np.uint8), iterations=1)
    #frame = cv.Canny(frame, 30, 200)
    
    return frame

def processText(frame):
    # Thanks! -> https://pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/

    # in order to apply Tesseract v4 to OCR text we must supply
    # (1) a language, (2) an OEM flag of 1, indicating that the we
    # wish to use the LSTM neural net model for OCR, and finally
    # (3) an OEM value, in this case, 7 which implies that we are
    # treating the ROI as a single line of text
    config = ("-c tessedit_char_whitelist=1234567890. -l eng --oem 1 --psm 7")
    text = pytesseract.image_to_string(frame, config=config)

    text = text.strip()
    results.append(text)

    text = "Current guess: " + text
    return text

results = []
def evalText():
    print("Best guess: " + statistics.mode(results))
    if len(results) > 100: results.pop(0) #remove the oldest

while True:
    ret, frame = cam.read()
    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    #frame = frame[:, 60:415] #crop to get rid of extra space on the sides of frame, helps a bit with accuracy
    frame = scaleDownFrame(frame, "calc-screen.jpg")
    frame = preProcessImage(frame)
    print(processText(frame))
    evalText()
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