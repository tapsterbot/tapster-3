import sys
sys.path.append("..")

import math
import time
import robot
from calc import calculator, strToCalc
from cv import checkAnswer

#args: python3 hello.py [robotPort] [cameraPort]

if len(sys.argv) > 1: #take in the serial port name from the args
    PORT = sys.argv[1]
else:
    print("Please specify a port.")
    raise SystemExit

bot = robot.Robot(PORT, -15, -23.5, False, 0.09)

#target: 0.1134
calculator(bot, "cc")
calculator(bot, "1+1=")
time.sleep(1)
calculator(bot, "c")
calculator(bot, "27.0692+186.4*10/1.69420-126/10000=")

bot.go(0, 90, 53) #move the delta linkages out of the way of the camera

print(checkAnswer(0.1134))