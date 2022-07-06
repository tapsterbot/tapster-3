import numpy as np
import cv2 as cv
import time
cap = cv.VideoCapture(2)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    #if not ret:
    #    print("Can't receive frame (stream end?). Exiting ...")
    #    break
    
    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'): #REQUIRED LINE
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()