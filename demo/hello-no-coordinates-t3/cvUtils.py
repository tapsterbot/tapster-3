import sys
import os
import math
import time
import statistics as stats
import cv2 as cv
import pytesseract
import numpy as np
import glob
import json

class cvUtils:
    def __init__(self):
        self.frames = []
        self.results = []

    # Clear image buffer
    def clearImageBuffer(self, cam):
        # Need to pull a few frames to clear out the image buffer in the camera hardware
        # It's a bit of a hack, but it works. ¯\_(ツ)_/¯
        for i in range(20):
            ret, frame = cam.read()

    def addImages(self, numFrames):
        if len(self.frames) > numFrames: self.frames.pop(0)
        frame = self.frames[0]
        for i in self.frames[1:]:
            frame = cv.add(frame, i)
        return frame

    def scaleDownFrame(self, frame, templatePath):
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

    def preProcessFrame(self, frame, blackRange, invertSrc):
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
        self.frames.append(frame)
        return self.addImages(5) #add together the last 5 frames, helps with noise and inconsistencies in the image

    def processText(self, frame):
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
        self.results.append(text)
        return text

    def evalText(self, numResults):
        if len(self.results) > numResults: self.results.pop(0) #remove the oldest
        return stats.mode(self.results)
    
    def calibFishEyeRemover(self, imagePath, dataPath, displayResults = True):
        # termination criteria
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6*7,3), np.float32)
        objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.
        images = glob.glob(imagePath + '*.png')

        numFailures = 0

        for fname in images:
            img = cv.imread(fname)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv.findChessboardCorners(gray, (7,6), None)

            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
                imgpoints.append(corners)
                
                if displayResults:
                    # Draw and display the corners
                    cv.drawChessboardCorners(img, (7,6), corners2, ret)
                    cv.imshow('img', img)
                    cv.waitKey(500)
            else: numFailures += 1
        cv.destroyAllWindows()

        try: ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        except:
            if numFailures > 10: print("Too many failed images. Retake your pictures, remove blurry pictures, and try again.")
            else: print("Something went wrong. Check your image path. Try retaking some of your images, and make sure the entire checkerboard is in frame.")
            exit()
        
        rvecsList = []
        tvecsList = []
        for i in rvecs: rvecsList.append(i.tolist()) #these are tuples of numpy arrays, convert them to python lists
        for i in tvecs: tvecsList.append(i.tolist())
        with open(dataPath, 'w') as file:
            json.dump((mtx.tolist(), dist.tolist(), rvecsList, tvecsList), file) #dump matrices out to a json file
        
        mean_error = 0
        for i in range(len(objpoints)):
            imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
            mean_error += error
        print( "total error: {}".format(mean_error/len(objpoints)))

    def removeFishEyeDistortion(self, frame, dataPath):
        frame = frame.copy() #don't modify the original

        with open(dataPath, 'r') as file:
            mtx, dist, rvecsList, tvecsList = json.load(file)
        mtx = np.array(mtx) #change lists back to numpy arrays
        dist = np.array(dist)
        for i, rvec in enumerate(rvecsList): rvecsList[i] = np.array(rvec) #change lists back to numpy arrays
        for i, tvec in enumerate(tvecsList): tvecsList[i] = np.array(tvec)
        rvecs = tuple(rvecsList) #change wrapper lists back to tuples
        tvecs = tuple(tvecsList)
        
        h, w = frame.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))

        # undistort
        frame = cv.undistort(frame, mtx, dist, None, newcameramtx)
        # crop the image
        x, y, w, h = roi
        frame = frame[y:y+h, x:x+w]
        return frame