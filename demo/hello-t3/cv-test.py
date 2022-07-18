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

# Clear image buffer
def clearImageBuffer(cam):
    # Need to pull a few frames to clear out the image buffer in the camera hardware
    # It's a bit of a hack, but it works. ¯\_(ツ)_/¯
    for i in range(20):
        ret, frame = cam.read()

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

frames = []
def averageImages():
    global frames
    frame = frames[0]
    for i in frames[1:]:
        frame = cv.add(frame, i)
    return frame

def preProcessImage(frame):
    # Blur the image
    #frame = cv.GaussianBlur(frame,(13,13), 0)
    # Edge detection
    #frame = cv.Canny(frame, 100, 200)
    #res, frame = cv.threshold(frame, 100, 255 , cv.THRESH_BINARY)
    frame = cv.GaussianBlur(frame, (5, 5), 0)
    cv.imshow("after blur", frame)
    ret, frame = cv.threshold(frame, 45, 255, cv.THRESH_BINARY)
    cv.imshow("after thresh", frame)
    #frame = cv.erode(frame, np.ones((2, 2), np.uint8), iterations=1)
    frame = cv.dilate(frame, np.ones((4, 4), np.uint8), iterations=1)
    cv.imshow("after erode", frame)
    #frame = cv.Canny(frame, 30, 200)
    
    return frame

def preProcessImage2(frame):
    global frames
    mask = cv.inRange(frame, np.array([0]), np.array([27])) #pull out the deepest blacks
    cv.imshow("mask", mask)
    frame = cv.bitwise_not(frame)
    res = cv.bitwise_and(frame, frame, mask = mask)
    cv.imshow("masked source", res)
    for i in range(10): res = cv.morphologyEx(res, cv.MORPH_CLOSE, np.ones((4, 4), np.uint8))
    cv.imshow("closing", res)

    # Blur the image
    res = cv.GaussianBlur(res,(7,7), 0)
    cv.imshow("after blur", res)

    ret, res = cv.threshold(res, 65, 255, cv.THRESH_BINARY)
    cv.imshow("after thresh", res)
    # Edge detection
    
    #edged = cv.Canny(res, 100, 200)
    #cv.imshow("after canny", edged)
    edged = res
    
    # Dilate it , number of iterations will depend on the image
    dilate = cv.dilate(edged, np.ones((2, 2), np.uint8), iterations=1)
    cv.imshow("after dilation", dilate)
    # perform erosion
    erode = cv.erode(dilate, None, iterations=1)

    erode = cv.bitwise_not(erode)
    frames.append(erode)
    if len(frames) > 5: frames.pop(0) #if frames holds more than the last 5 frames, remove the oldest one
    return averageImages()

results = []
def processText(frame):
    global results
    # Thanks! -> https://pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/

    # in order to apply Tesseract v4 to OCR text we must supply
    # (1) a language in this case our custom seven segment display language, 
    # (2) an OEM flag of 1, indicating that the we
    # wish to use the LSTM neural net model for OCR, and finally
    # (3) an OEM value, in this case, 7 which implies that we are
    # treating the ROI as a single line of text
    # The tessedit_char_whitelist environment var. restricts characters Tesseract looks for in its processing (in this case, numbers 0-9 and period)

    config = ("-c tessedit_char_whitelist=1234567890. --tessdata-dir " + os.getcwd() + "/tessdata -l ssd --oem 1 --psm 7")
    #config = ("-c tessedit_char_whitelist=1234567890. -l eng --oem 1 --psm 7")
    text = pytesseract.image_to_string(frame, config=config)

    text = text.strip()
    results.append(text)

    text = "Current guess: " + text
    return text

def evalText():
    global results
    print("Best guess: " + statistics.mode(results))
    if len(results) > 100: results.pop(0) #remove the oldest


clearImageBuffer(cam)

while True:
    ret, frame = cam.read()
    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    frame = scaleDownFrame(frame, "calc-screen.jpg")
    
    #frame = preProcessImage(frame)
    frame = preProcessImage2(frame)

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