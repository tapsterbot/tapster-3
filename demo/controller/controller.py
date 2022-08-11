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
# - Click anywhere within the Camera window, and the robot will go and tap there! Alternatively,
#   you can make the robot follow the cursor, or print data out to a terminal window for you to
#   implement into your own code later on!
#
###################################################################################################

import sys
sys.path.append("..")

import statistics as stats
import cv2 as cv
import numpy as np
import json
import argparse
import robot
#from calibrate import applyDistortionCorrection #reuse distortion correction program

parser = argparse.ArgumentParser()
parser.add_argument("PORT", help = "The COM port of the connection to the robot (i.e. COM3, /dev/ttyUSB0)")
parser.add_argument("CAMPORT", help = "The ID of the camera", type = int)
parser.add_argument("-p", "--print-python", help = "Prints coordinates of places clicked in formatted Python", action = "count")
parser.add_argument("-g", "--print-gcode", help = "Prints coordinates of places clicked in formatted GCode", action = "count")
parser.add_argument("-c", "--coordinate-config", help = "Custom path to coordinate calibration file")
parser.add_argument("-d", "--distortion-config", help = "Custom path to camera distortion calibration file")
parser.add_argument("-f", "--follow", help = "Enables \"follow mode\" -- the robot follows the mouse cursor", action = "count")

args = parser.parse_args()

bot = robot.Robot(args.PORT, -15, -25, False, 0.09)
bot.go(0, 0, 0)
bot.go(0, 80, 60)

if args.print_python: print(f"bot = robot.Robot({args.PORT}, {bot.clearance_height}, {bot.tap_height}, {bot.printCoordinates}, {bot.sendPause})")

mouseCoords = [0, 0]
isNewCoords = False
# mouse callback function
def mouseClick(event, x, y, flags, param):
    global mouseCoords, isNewCoords
    if event == cv.EVENT_LBUTTONUP:
        isNewCoords = True
        mouseCoords[0] = x
        mouseCoords[1] = y

isClick = False
def mouseFollow(event, x, y, flags, param):
    global mouseCoords, isNewCoords, isClick
    if event == cv.EVENT_MOUSEMOVE:
        mouseCoords = [x, y]
        isNewCoords = True
    if event == cv.EVENT_LBUTTONDOWN: isClick = True    

with open(args.coordinate_config if args.coordinate_config else "coordinateCalib.json", "r") as file: calibCoordinates = json.load(file)
if calibCoordinates[0][1] == [0, 0]:
    print("Calibration was not run correctly. Please try again, and read the README for additional help.")
    exit()

#transforms pixel coordinates in the video feed, returns robot coordinates
def transformCoordinates(coordsToTransform):
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


cam = cv.VideoCapture(int(args.CAMPORT))
try: #handle the camera being incorrectly initialized
    ret, frame = cam.read()
    cv.imshow("f", frame)
    cv.destroyAllWindows()
except:
    print("Camera not initialized correctly. Try a different index.")
    exit()

cv.namedWindow("Camera")
cv.setMouseCallback("Camera", mouseFollow if args.follow else mouseClick)

while True:
    ret, frame = cam.read()
    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    cv.imshow("Camera", frame)

    if isNewCoords:
        coords = transformCoordinates(mouseCoords)
        if args.print_gcode:
            print(f"G0 X{coords[0]} Y{coords[1]} Z{bot.tap_height}")
            print(f"G0 X{coords[0]} Y{coords[1]} Z{bot.clearance_height}")
        elif args.print_python: print(f"bot.tap({coords[0]}, {coords[1]})")

        if isClick or args.follow == None:
            bot.go(0, 80, 10)
            bot.tap(coords[0], coords[1], 0.25, 0.1)
            bot.go(0, 80, 10)
            bot.go(0, 80, 60) #move bot back to "home" position
            isClick = False
        else: bot.go(coords[0], coords[1], bot.clearance_height) #for follow mode
        isNewCoords = False
    
    if cv.waitKey(1) == ord("q"): break #q to quit

cam.release()
cv.destroyAllWindows()