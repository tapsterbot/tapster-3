import sys
import os
import math
import statistics as stats
import time
import cv2 as cv
import pytesseract
import imutils
import numpy as np

frames = []
results = []

# Clear image buffer
def clearImageBuffer(cam):
    # Need to pull a few frames to clear out the image buffer in the camera hardware
    # It's a bit of a hack, but it works. ¯\_(ツ)_/¯
    for i in range(20):
        ret, frame = cam.read()

def addImages(numFrames):
    global frames
    if len(frames) > numFrames: frames.pop(0)
    frame = frames[0]
    for i in frames[1:]:
        frame = cv.add(frame, i)
    return frame

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
    return frame[y:y + h, x:x + w] #crop frame to the size of the template image

def preProcessFrame(frame, blackLevel):
    global frames

    mask = cv.inRange(frame, np.array([0]), np.array([blackLevel])) #pull out the deepest blacks
    frame = cv.bitwise_not(frame) #invert input frame so text is white -- required for the mask to work correctly
    frame = cv.bitwise_and(frame, frame, mask = mask) #apply mask

    frame = cv.morphologyEx(frame, cv.MORPH_CLOSE, np.ones((4, 4), np.uint8)) #close holes

    frame = cv.medianBlur(frame, 5) #apply blur

    ret, frame = cv.threshold(frame, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU) #apply Otsu thresholding -- used for denoising

    # Contours -- used for removing small noise/unwanted small features from the image. Put into a mask and then applied to image.
    cnts = cv.findContours(frame.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) #find contours
    cnts = cnts[0]

    # make an empty mask 
    mask = np.ones(frame.shape[:2], dtype = "uint8") * 255
    for c in cnts:
        # if the contour is not sufficiently large, ignore it
        if cv.contourArea(c) < 100:
            cv.drawContours(mask, [c], -1, 0, -1)
            continue
    
    # Remove ignored contours
    frame = cv.bitwise_and(frame.copy(), frame.copy(), mask = mask)

    frame = cv.bitwise_not(frame) #invert frame to make black text on white background (rather than white on black) -- tesseract 4.0.0+ requires this
    frames.append(frame)
    return addImages(5) #add together the last 5 frames, helps with noise and inconsistencies in the image

def processText(frame):
    global results

    # Thanks! -> https://pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/

    # in order to apply Tesseract v4 to OCR text we must supply
    # (1) a language in this case our custom seven segment display language, 
    # (2) an OEM flag of 1, indicating that the we
    # wish to use the LSTM neural net model for OCR, and finally
    # (3) an OEM value, in this case, 7 which implies that we are
    # treating the ROI as a single line of text
    # The tessedit_char_whitelist environment var. restricts characters Tesseract
    # looks for in its processing (in this case, numbers 0-9 and period)
    # --tessdata-dir gives tesseract the directory of the data file for our
    # custom seven segment display language, in this case $PWD/tessdata.

    config = ("-c tessedit_char_whitelist=1234567890. --tessdata-dir " + os.getcwd() + "/tessdata -l ssd --oem 1 --psm 7")
    text = pytesseract.image_to_string(frame, config = config)

    text = text.strip() #remove whitespace
    results.append(text)
    return text

def evalText(numResults):
    global results
    if len(results) > numResults: results.pop(0) #remove the oldest
    return stats.mode(results)


#===========================================================================================================================#


def checkAnswer(val): #the main function to check the outputted result on the calculator
    cam = cv.VideoCapture(int(sys.argv[2]))
    if not cam.isOpened():
        print("Cannot open camera, make sure it is connected to the computer.")
        exit()
    
    clearImageBuffer(cam)

    for i in range(100): #take in 100 frames
        ret, frame = cam.read()
        frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE) #correct for camera rotation

        frame = scaleDownFrame(frame, "calc-screen.jpg") #apply template matching and crop
        frame = frame[20:frame.shape[0] - 25, 18:frame.shape[1] - 19] #remove edges (crop again)
        
        frame = preProcessFrame(frame, 45)

        cv.imshow("Frame", frame)
        if cv.waitKey(1) == ord('q'): #REQUIRED LINE
            break
        processText(frame)
    cv.destroyAllWindows()
    print("Best guess: " + evalText(100))
    val = str(val)
    val = val.replace(".", "") #remove periods and negative signs -- tesseract just isn't very good at picking these up
    val = val.replace("-", "")
    return (evalText(100) == val)