###################################################################################################
#
#                              Controller Calibration for Tapster 3
#                              Device Used: Tapster Calibration Stick
#
#                                          Requirements
# - Read README.md and follow the installation instructions for:
#    - OpenCV 4.x
#    - Tesseract and pytesseract
#    - imutils
#    - Miscellaneous Python dependencies required for computer vision
#    - Robot modifications required for calibration
#    - Collecting the distortion correction dataset
#
#                                             Usage
# - Run with: python3 calibrate.py [BOTMODEL] [CAMERAPORT]
#    - Linux example (Ubuntu 22.04): python3 calibrate.py -t 0
#    - At least on Linux, the camera port will be a single number. Start with 0, and keep going up
#      until the camera opens successfully (no error message from Python)
#    - The BOTMODEL flag is what makes sure the program knows which robot you are calibrating. Use
#      '-t' for the Tapster 3 and '-T' for the Tapster 3+.
#
###################################################################################################

import sys
import cv2 as cv
import numpy as np
import json

MODEL = None
if len(sys.argv) > 2:
    if sys.argv[1][0] == "-":
        if sys.argv[1][1] == "t": MODEL = "t"
        elif sys.argv[1][1] == "T": MODEL = "T"
    
    if MODEL == None:
        print("Please specify a correct robot model.")
        exit()

    CAMPORT = int(sys.argv[2])
else:
    print("Please specify an index/port for the camera and/or a robot model.")
    exit()

input("""
                Calibration for Tapster 3
              =============================

- Remove phone grips
- Place calibration stick on the phone holder base
- Line the calibration stick up with the back and sides of the
  phone holder base
- Make sure the camera is plugged in!
- Have your camera distortion correction images the ./calib-images/
  directory

    --Extended/Detailed Instructions in the README!--

Press enter when ready.""")

#================================================================#

def calDistortionCorrection():
    pass #implement later

def applyDistortionCorrection(frame):
    return frame #implement later

def preProcessFrame(frame, blackRange, invertSrc):
    mask = cv.inRange(frame, np.array([blackRange[0]]), np.array([blackRange[1]])) #pull out the deepest blacks
    if invertSrc: frame = cv.bitwise_not(frame) #invert input frame so text is white -- required for the mask to work correctly
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

    if invertSrc: frame = cv.bitwise_not(frame) #invert frame to make black text on white background (rather than white on black) -- tesseract 4.0.0+ requires this
    return frame

def findCircleContours(contours):
    if len(contours) == 3: return contours #handle an already perfect list

    for i in range(len(contours) - 2):
        x, y, w, h = cv.boundingRect(contours[i])
        centerX = x + (w/2)
        xRange = (centerX - 15, centerX + 15) #valid range for the x coordinate of the other dots

        for c in contours[i + 1:i + 3]:
            x, y, w, h = cv.boundingRect(c)
            centerX = x + (w/2)
            if centerX < xRange[0] or centerX > xRange[1]: break #break if the coordinate is out of valid range
        else:
            return contours[i:i + 3] #return the good contours

#================================================================#


cam = cv.VideoCapture(CAMPORT)
try: #handle the camera being incorrectly initialized
    ret, frame = cam.read()
    cv.imshow("f", frame)
    cv.destroyAllWindows()
except:
    print("Camera not initialized correctly. Try a different index.")
    exit()

while True:
    ret, frame = cam.read()
    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    cv.imshow(f"Camera {CAMPORT}", frame)
    cv.waitKey(1500)
    cv.destroyAllWindows()
    i = input("Was that the correct camera feed? [y/n/[s]how again] ")
    if i.lower() == "y": break
    elif i.lower() == "n": exit()
    for i in range(60): ret, frame = cam.read() #clear camera buffer

print("Calibrating...")

for i in range(60): ret, frame = cam.read() #clear camera buffer
frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE) #fix rotation

calDistortionCorrection()
frame = applyDistortionCorrection(frame) #apply distortion correction before calibration for better accuracy

# the coordinates of the circle stickers in "robot space" is a known, guaranteed value.
# the values in the camera feed are unknown, and this list maps the two together. 
if MODEL == "t": coordinates = [[[-2, 52], [0, 0]], [[-2, 1],[0, 0]], [[-2, -48], [0, 0]]]
elif MODEL == "T":
    print("Feature not implemented yet.")
    exit()

frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY) #grayscale

frame = preProcessFrame(frame, [220, 255], False)

contours, hierarchy = cv.findContours(frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

circleConts = findCircleContours(contours)
if circleConts == None:
    print("Calibration failed. Please try again, or see README for help.")
    exit()
for i, c in enumerate(circleConts):
    x, y, w, h = cv.boundingRect(c)
    centerX = x + (w/2)
    centerY = y + (h/2)
    coordinates[i][1] = [centerX, centerY]

with open("coordinateCalib.json", "w") as file: json.dump(coordinates, file)

cam.release()

print("Done! Results printed here and dumped to coordinateCalib.json\n")
print(coordinates)