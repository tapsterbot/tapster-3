import sys
import os
import math
import statistics as stats
import time
import cv2 as cv
import pytesseract
import imutils
import numpy as np
from cvUtils import cvUtils
import json

def pullCoordinates():
    pass

def transformCoordinates(imgCoordinates): #transforms pixel coordinates in the video feed, returns robot coordinates
    with open("coordinateData.json", "r") as file: coordinates = json.load(file)
    print(coordinates)
    
    for i in range(len(coordinates)): coordinates[i][1][1] = coordinates[i][1][1]*-1 #flip over x axis
    print(coordinates)
    translation = (coordinates[1][1][0] - coordinates[1][0][0], coordinates[1][1][1] - coordinates[1][0][1])
    print(translation)
    
    for i in range(len(coordinates)): #translate the pixel coordinates so point [0] lines up on both coordinate systems
        coordinates[i][1][0] -= translation[0]
        coordinates[i][1][1] -= translation[1]

    print(coordinates)

    scaling = (stats.mean((coordinates[0][0][0], coordinates[2][0][0]))/stats.mean((coordinates[0][1][0], coordinates[2][1][0])), 
               stats.mean((coordinates[0][0][1], coordinates[2][0][1]))/stats.mean((coordinates[0][1][1], coordinates[2][1][1])))
    
    coordinates[0][1][0] = coordinates[0][1][0]*scaling[0]
    coordinates[0][1][1] = coordinates[0][1][1]*scaling[1]
    coordinates[2][1][0] = coordinates[2][1][0]*scaling[0]
    coordinates[2][1][1] = coordinates[2][1][1]*scaling[1]

    print(scaling)
    print(coordinates)

    #imgCoordinates[1] = imgCoordinates[1]*-1


def calibrateCamFeed(bot, cam):
    cvu = cvUtils()
    cvu.clearImageBuffer(cam)

    ret, frame = cam.read()

    #if not os.path.exists("calibData.json"):
    #    print("Calibration data does not exist. Running fisheye distortion calibrator...")
    #    cvu.calibFishEyeRemover("./calib-images/*", "calibData.json", False)
    #frame = cvu.removeFishEyeDistortion(frame, "calibData.json")
    #cv.imshow("defisheye", frame)

    # the coordinates of the circle stickers in "robot space" is a known, guaranteed value.
    # the values in the camera feed are unknown, and this list maps the two together. 
    coordinates = [[[-2, 52], [0, 0]], [[-2, 1],[0, 0]], [[-2, -48], [0, 0]]]

    frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY) #grayscale
    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE) #fix rotation

    frame = cvu.preProcessFrame(frame, [220, 255], False)

    contours, hierarchy = cv.findContours(frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for i, c in enumerate(contours):
        x, y, w, h = cv.boundingRect(c)
        centerX = x + (w/2)
        centerY = y + (h/2)
        print(f"Contour {i}: ({centerX}, {centerY})")
        coordinates[i][1] = [centerX, centerY]
    
    with open("coordinateData.json", "w") as file: json.dump(coordinates, file)

    cam.release()
    cv.destroyAllWindows()



transformCoordinates(None)