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

    #Fix fisheye calibration, then add this back
    
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

#frame inputted MUST be the same dimensions as the calibration image (currently 480x640 VERTICAL)
#and all features must be in the same position -- no shifting -- for this to accurately translate to robot space
def findButtons(frame, buttonContourSize = None, centerCoords = False): #returns a 2d list of buttons with their x, y loc in robot space, dims, and "value", i.e. [["skip", 10, 20, 5, 5], ...]
    #pseudocode:
    """
    apply a mask to the image to get rid of everything but [color]
    clean image, get rid of non-rectangular things (likely not buttons)
    copy image, display this version
    find contours, I guess? pick out each of the ROIs (buttons), split out into individual "frames"
    clean each individual frame, make each one BLACK ON WHITE for tesseract
    run through tesseract, adding coords from original image and button text to list
    return list

    the user can do whatever they want with the button coordinate and name data, probably
    run it through transformCoordinates() and run the robot to it.

    if centerCoords = True, set the coordinates = the (x, y) of the CENTER of the button.
    else set to top left corner (or whatever the contours alg picks out)
    """
    frame2 = frame.copy()

    frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY) #grayscale
    #frame = cv.medianBlur(frame, 5) #apply blur
    ret, frame = cv.threshold(frame, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU) #apply Otsu thresholding -- used for denoising
    frame = cv.bitwise_not(frame)
    cv.imshow("pre-contour", frame)

    # Contours -- used for removing small noise/unwanted small features from the image. Put into a mask and then applied to image.
    cnts = cv.findContours(frame.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) #find contours
    cnts = cnts[0]

    # make an empty mask 
    mask = np.ones(frame.shape[:2], dtype = "uint8") * 255
    for c in cnts:
        # if the contour is not sufficiently large, ignore it
        if cv.contourArea(c) < 100:
            peri = cv.arcLength(c, True)
            approx = cv.approxPolyDP(c, 0.04 * peri, True)
            if len(approx) <= 4: cv.drawContours(mask, [c], -1, 0, -1) #filter out non-rectangles
            continue

    # Remove ignored contours
    frame = cv.bitwise_and(frame.copy(), frame.copy(), mask = mask)
    cv.imshow("f", frame)
    cv.imshow("M", mask)
    cv.waitKey(0)
    pass

cam = cv.VideoCapture(3)

ret, frame = cam.read()
frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
cv.imshow("asdf", frame)

findButtons(frame, None, False)