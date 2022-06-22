import sys
sys.path.append("..")

import robot
import time

if len(sys.argv) > 1: #take in the serial port name from the args
    PORT = sys.argv[1]
else:
    print("Please specify a port.")
    raise SystemExit

bot = robot.Robot(PORT, -15, -22, False, 0.09)

bot.pbmGo(True, False, True)
time.sleep(1)
bot.pbmGo(False, False, False)

for i in range(6): bot.pbmPress(False, False, True, 0.5)

bot.pbmPress(True)