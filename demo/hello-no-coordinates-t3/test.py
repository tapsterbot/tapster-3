import sys
import cv2 as cv
import numpy as np
from cvUtils import cvUtils

cvu = cvUtils()

cam = cv.VideoCapture(int(sys.argv[1]))

while True:
    ret, frame = cam.read()
    cv.imshow("orig", frame)
    frame = cvu.removeFishEyeDistortion(frame, "calibData.json")
    cv.imshow("frame", frame)

    if cv.waitKey(1) == ord("q"): break