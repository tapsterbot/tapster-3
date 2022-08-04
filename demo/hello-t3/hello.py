###################################################################################################
#
#                             Hello/Unboxing Experience for Tapster 3
#                                Device Used: 4-Function Calculator
#
#                                          Requirements
# - Read README.md and follow the installation instructions for:
#    - OpenCV 4.x
#    - Tesseract and pytesseract
#    - imutils
#    - Miscellaneous Python dependencies required for computer vision
#
#                                             Usage
# - Run with: python3 hello.py [ROBOTPORT] [CAMERAPORT]
#    - Linux example (Ubuntu 22.04): python3 hello.py /dev/ttyUSB0 0
#    - At least on Linux, the camera port will be a single number. Start with 0, and keep going up
#      until the camera opens successfully (no error message from Python)
#
#                                              Note
# - This version of the Hello/Unboxing Experience program has hard-coded values for the locations
#   of buttons on the calculator used for the demo, and only makes use of computer vision to check
#   the calculator output. See ../hello-no-coordinates-t3/ for a completely computer-vision-based
#   version.
#
###################################################################################################

import sys
sys.path.append("..")

import time
import robot
from calc import calculator, strToCalc
from cv import checkAnswer

if len(sys.argv) > 2: #take in the serial port name from the args
    PORT = sys.argv[1]
    #Camera port is assigned later, but still check that both args are here.
else:
    print("Please specify a port for both the robot and camera.")
    raise SystemExit

bot = robot.Robot(PORT, -15, -23.5, False, 0.09)
bot.go(0, 0, 0)

#target: 0.1134
calculator(bot, "cc")
calculator(bot, "1+1=")
bot.go(0, 90, 53) #move the bot so the user can see
time.sleep(2)

while True:
    calculator(bot, "cc")
    calculator(bot, "27.0692+186.4*10/1.69420-126/10000=")

    bot.go(0, 90, 53) #move the delta linkages out of the way of the camera

    if checkAnswer(0.1134):
        bot.go(0, 0, 0)
        time.sleep(0.1)
        #Dance! (if it's correct)
        for i in range(4):
            for i in range(2):
                bot.go(60, 0, 33)
                bot.go(0, 0, -15)
                bot.go(-60, 0, 33)
                bot.go(0, 0, -15)
            bot.go(0, 0, -15)
            for i in range(8):
                bot.go(0, 0, -15)
                bot.go(0, 0, 10)
        break
    #If the answer is not correct, loop back and try typing into the calculator again.