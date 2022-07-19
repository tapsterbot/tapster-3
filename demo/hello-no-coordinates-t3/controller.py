import sys
sys.path.append("..")

import robot
import time
import os
import cv2 as cv
import numpy as np
import math

class Controller:
    calibration = [[[0, 0], [0, 0]],
                   [[0, 0], [0, 0]],
                   [[0, 0], [0, 0]],
                   [[0, 0], [0, 0]]]  
    newCoordinatesFlag = False

    def __init__(self, bot, camPort):
        self.bot = bot
        self.camPort = camPort
        self.cam = cv.VideoCapture(camPort)
        #add config file stuff here (to save calibration data between program runs) -- implement later
    
    def mouse(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            self.mouseCoordinates = (x, y)
            self.newCoordinatesFlag = True

    def run(self):
        self.bot.go(0, 90, 53) #move the bot out of the way
        cv.namedWindow("Frame")
        cv.setMouseCallback("Frame", self.mouse)

        ret, frame = self.cam.read() #read a frame from the camera feed
        frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE) #correct for camera rotation
        count = 0
        self.bot.go(0, 0, self.bot.clearance_height)
        while count < 4:
            cv.imshow("Frame", frame)
            if self.newCoordinatesFlag:
                frame = cv.circle(frame, self.mouseCoordinates, 10, [0, 0, 255], -1)
                cv.imshow("Frame", frame)
                self.newCoordinatesFlag = False
                self.calibration[count][0] = self.mouseCoordinates

                while cv.waitKey(1) != ord("q"): #jog the bot to get it into position
                    if cv.waitKey(1) == ord("w"): self.bot.send("$J=G91 Y2 F35000") #GRBL jog commands
                    elif cv.waitKey(1) == ord("a"): self.bot.send("$J=G91 X-2 F35000")
                    elif cv.waitKey(1) == ord("s"): self.bot.send("$J=G91 Y-2 F35000")
                    elif cv.waitKey(1) == ord("d"): self.bot.send("$J=G91 X2 F35000")
                    elif cv.waitKey(1) == ord("r"): self.bot.send("$J=G91 Z1 F35000")
                    elif cv.waitKey(1) == ord("f"): self.bot.send("$J=G91 Z-1 F35000")
                self.calibration[count][1] = self.bot.send("?", None, 'r')
                count += 1
            if cv.waitKey(1) == ord("p"): break #required for cv.imshow()
        cv.destroyAllWindows()


if __name__ == "__main__":
    if len(sys.argv) > 2: #take in the serial port and cam port name from the args
        PORT = sys.argv[1]
        CAM_PORT = int(sys.argv[2])
    else:
        print("Please specify a port.")
        raise SystemExit

    bot = robot.Robot(PORT, -15, -22, False, 0.09) #t3 settings

    controller = Controller(bot, CAM_PORT)
    controller.run()