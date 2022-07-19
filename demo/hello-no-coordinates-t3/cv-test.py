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
    #cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
    return frame[y:y + h, x:x + w]

frames = []
def averageImages():
    global frames
    frame = frames[0]
    for i in frames[1:]:
        frame = cv.add(frame, i)
    return frame

def preProcessImage(frame):
    global frames
    mask = cv.inRange(frame, np.array([0]), np.array([45])) #pull out the deepest blacks
    cv.imshow("mask", mask)
    frame = cv.bitwise_not(frame)
    frame = cv.bitwise_and(frame, frame, mask = mask)
    cv.imshow("masked source", frame)

    frame = cv.morphologyEx(frame, cv.MORPH_CLOSE, np.ones((4, 4), np.uint8))
    cv.imshow("closing", frame)

    frame = cv.medianBlur(frame, 5)
    cv.imshow("after blur", frame)

    ret, frame = cv.threshold(frame, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    cv.imshow("after thresh", frame)

    # find contours
    cnts = cv.findContours(frame.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0]

    # make an empty mask 
    mask = np.ones(frame.shape[:2], dtype="uint8") * 255
    for c in cnts:
        # if the contour is not sufficiently large, ignore it
        if cv.contourArea(c) < 100:
            cv.drawContours(mask, [c], -1, 0, -1)
            continue
    
    # Remove ignored contours
    frame = cv.bitwise_and(frame.copy(), frame.copy(), mask = mask)

    #newimage = frame
    #newimage = cv.dilate(newimage,None, iterations=3)
    #newimage = cv.erode(newimage,None, iterations=3)
    #ret,newimage = cv.threshold(newimage, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    #frame = newimage

    frame = cv.bitwise_not(frame)
    frames.append(frame)
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

def deFishEye(frame):
    pass


clearImageBuffer(cam)

while True:
    ret, frame = cam.read()
    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    frame = scaleDownFrame(frame, "calc-screen.jpg")
    frame = frame[20:frame.shape[0] - 25, 18:frame.shape[1] - 19]
    
    frame = preProcessImage(frame)

    print(processText(frame))
    evalText()
    
    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'): #REQUIRED LINE
        break

cam.release()
cv.destroyAllWindows()