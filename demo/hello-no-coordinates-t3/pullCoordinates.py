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

def transformCoordinates(coordsToTransform, dataFile = "coordinateData.json"): #transforms pixel coordinates in the video feed, returns robot coordinates
    with open(dataFile, "r") as file: coordinates = json.load(file)
    #print(coordinates)

    p = 1 #point b, used for distance calculations
    
    #Points, top to bottom: a, b, c
    #Deltas: Δab, Δbc, Δac
    #Note: All points on the calibration stick are on x = -2 (robot space), so this ignores the x coordinate altogether
    robotDeltas = (coordinates[0][0][1] - coordinates[1][0][1], coordinates[1][0][1] - coordinates[2][0][1], coordinates[0][0][1] - coordinates[2][0][1])
    camDeltas = (coordinates[0][1][1] - coordinates[1][1][1], coordinates[1][1][1] - coordinates[2][1][1], coordinates[0][1][1] - coordinates[2][1][1])
    print(robotDeltas)
    print(camDeltas)

    #The ratio between the distances in "robot space" and in "camera space"
    scaleFactor = stats.mean((robotDeltas[0]/camDeltas[0], robotDeltas[1]/camDeltas[1], robotDeltas[2]/camDeltas[2]))
    print(scaleFactor)

    #The distance between coordsToTransform and a known point (a, b, c) in camera space
    #Only utilizes one point (b) for now, but it can be changed to use all 3 for (likely) greater accuracy
    toTransformDelta = [coordsToTransform[0] - coordinates[p][1][0], coordsToTransform[1] - coordinates[p][1][1]]
    print(toTransformDelta)

    #Scale the distances by the scale factor
    toTransformDelta = [i*scaleFactor for i in toTransformDelta]
    print(toTransformDelta)

    #Add the scaled distances to the "robot space" coords of point b to get a resulting coordinate in robot space
    #Note: Inverting the y fixed a random issue. Don't know why, but that -1 matters.
    return (coordinates[p][0][0] + toTransformDelta[0], -1*(coordinates[p][0][1] + toTransformDelta[1]))

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