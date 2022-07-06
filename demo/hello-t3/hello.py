import sys
sys.path.append("..")

import math
import time
import robot
from calc import calculator, strToCalc
from cv import checkAnswer

if len(sys.argv) > 1: #take in the serial port name from the args
    PORT = sys.argv[1]
else:
    print("Please specify a port.")
    raise SystemExit

bot = robot.Robot(PORT, -15, -23.5, False, 0.09)

#target: 0.7734
calculator(bot, "c")
calculator(bot, "1+1=")
time.sleep(1)
calculator(bot, "c")
calculator(bot, "12.5-8.5*64+37+4869*1.5-9/10000=")

#computer vision-y stuff here