###################################################################################################
#
#                                    Controller for Tapster 3
#                                       Device Used: Any
#
#                                          Requirements
# - Read README.md and follow the installation instructions for:
#    - OpenCV 4.x
#    - Tesseract and pytesseract
#    - imutils
#    - Miscellaneous Python dependencies required for computer vision
#
#                                             Usage
# - Run with: python3 controller.py [optArgs] [ROBOTPORT] [CAMERAPORT]
#    - Linux example (Ubuntu 22.04): python3 calibrate.py /dev/ttyUSB0 0
#    - At least on Linux, the camera port will be a single number. Start with 0, and keep going up
#      until the camera opens successfully (no error message from Python)
# - Optional Arguments:
#    - -p : Prints Gcode coordinates for the recorded moves out to the terminal screen.
#
###################################################################################################

import sys
sys.path.append("..")

import statistics as stats
import cv2 as cv
import numpy as np
import json
import robot
#from calibrate import applyDistortionCorrection #reuse distortion correction program

printCoords = False
if len(sys.argv) > 2: #take in the serial port name from the args
    if sys.argv[1][0] == "-":
        if sys.argv[1][1] == "p": printCoords = True
        PORT = sys.argv[2]
        CAMPORT = int(sys.argv[3])
    else: 
        PORT = sys.argv[1]
        CAMPORT = int(sys.argv[2])
else:
    print("Please specify a port for both the robot and camera.")
    exit()

bot = robot.Robot(PORT, -15, -25, False, 0.09)
bot.go(0, 0, 0)
bot.go(0, 80, 60)

mouseCoords = [0, 0]
isNewCoords = False
# mouse callback function
def mouse(event, x, y, flags, param):
    global mouseCoords, isNewCoords
    if event == cv.EVENT_LBUTTONUP:
        isNewCoords = True
        mouseCoords[0] = x
        mouseCoords[1] = y

with open("coordinateCalib.json", "r") as file: calibCoordinates = json.load(file)
if calibCoordinates[0][1] == [0, 0]:
    print("Calibration was not run correctly. Please try again, and read the README for additional help.")
    exit()

#transforms pixel coordinates in the video feed, returns robot coordinates
def transformCoordinates(coordsToTransform, dataFile = "coordinateCalib.json"):
    global calibCoordinates
    coordinates = calibCoordinates

    p = 1 #identifier for point b, used for distance calculations
    
    #Points, top to bottom: a, b, c
    #Deltas: Δab, Δbc, Δac
    #Note: All points on the calibration stick are on x = -2 (robot space), so this ignores the x coordinate altogether
    robotDeltas = (coordinates[0][0][1] - coordinates[1][0][1], coordinates[1][0][1] - coordinates[2][0][1], coordinates[0][0][1] - coordinates[2][0][1])
    camDeltas = (coordinates[0][1][1] - coordinates[1][1][1], coordinates[1][1][1] - coordinates[2][1][1], coordinates[0][1][1] - coordinates[2][1][1])

    #The ratio between the distances in "robot space" and in "camera space"
    scaleFactor = stats.mean((robotDeltas[0]/camDeltas[0], robotDeltas[1]/camDeltas[1], robotDeltas[2]/camDeltas[2]))

    #The distance between coordsToTransform and a known point (a, b, c) in camera space
    #Only utilizes one point (b) for now, but it can be changed to use all 3 for (likely) greater accuracy
    toTransformDelta = [coordsToTransform[0] - coordinates[p][1][0], coordsToTransform[1] - coordinates[p][1][1]]

    #Scale the distances by the scale factor
    toTransformDelta = [i*scaleFactor for i in toTransformDelta]

    #Add the scaled distances to the "robot space" coords of point b to get a resulting coordinate in robot space
    #Note: Inverting the y fixed a random issue. Don't know why, but that -1 matters.
    return (coordinates[p][0][0] + toTransformDelta[0], -1*(coordinates[p][0][1] + toTransformDelta[1]))


cam = cv.VideoCapture(CAMPORT)
try: #handle the camera being incorrectly initialized
    ret, frame = cam.read()
    cv.imshow("f", frame)
    cv.destroyAllWindows()
except:
    print("Camera not initialized correctly. Try a different index.")
    exit()

cv.namedWindow("Camera")
cv.setMouseCallback("Camera", mouse)

while True:
    ret, frame = cam.read()
    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    cv.imshow("Camera", frame)

    if isNewCoords:
        coords = transformCoordinates(mouseCoords)
        if printCoords:
            print(f"G0 X{coords[0]} Y{coords[1]} Z{bot.tap_height}")
            print(f"G0 X{coords[0]} Y{coords[1]} Z{bot.clearance_height}")
        bot.go(0, 80, 10)
        bot.tap(coords[0], coords[1], 0.25, 0.1)
        bot.go(0, 80, 10)
        bot.go(0, 80, 60) #move bot back to "home" position
        isNewCoords = False
    
    if cv.waitKey(1) == ord("q"): break

cam.release()
cv.destroyAllWindows()