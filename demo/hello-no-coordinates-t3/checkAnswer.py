import sys
import cv2 as cv
import numpy as np
from cvUtils import cvUtils

def checkAnswer(val): #the main function to check the outputted result on the calculator
    cvu = cvUtils()
    cam = cv.VideoCapture(int(sys.argv[2]))
    if not cam.isOpened():
        print("Cannot open camera, make sure it is connected to the computer.")
        exit()
    
    cvu.clearImageBuffer(cam)

    for i in range(100): #take in 100 frames
        ret, frame = cam.read()
        frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE) #correct for camera rotation

        frame = cvu.scaleDownFrame(frame, "calc-screen.jpg") #apply template matching and crop
        frame = frame[20:frame.shape[0] - 25, 18:frame.shape[1] - 19] #remove edges (crop again)
        
        frame = cvu.preProcessFrame(frame, [0, 45], True)

        cv.imshow("Frame", frame)
        if cv.waitKey(1) == ord('q'): #REQUIRED LINE
            break
        cvu.processText(frame)
    cv.destroyAllWindows()
    print("Best guess: " + cvu.evalText(100))
    val = str(val)
    val = val.replace(".", "") #remove periods and negative signs -- tesseract just isn't very good at picking these up
    val = val.replace("-", "")
    return (cvu.evalText(100) == val)