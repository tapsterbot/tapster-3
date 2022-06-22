import sys
sys.path.append("..")

import robot
import time

if len(sys.argv) > 1: #take in the serial port name from the args
    PORT = sys.argv[1]
else:
    print("Please specify a port.")
    raise SystemExit

bot = robot.Robot(PORT, -22, -32, False, 0.09)

bot.pbmPress(True, False, False, 1.75)
time.sleep(0.5)
bot.tap(20, -26)
time.sleep(0.5)
bot.tap(16, -10)