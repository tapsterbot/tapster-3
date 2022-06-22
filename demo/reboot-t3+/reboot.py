import sys
sys.path.append("..")

import robot
import time

if len(sys.argv) > 1: #take in the serial port name from the args
    PORT = sys.argv[1]
else:
    print("Please specify a port.")
    raise SystemExit

bot = robot.Robot(PORT, -22, -34, False, 0.09)

bot.pbmPress(True, False, False, 1.75)
time.sleep(0.5)
bot.tap(20, -26)
time.sleep(0.5)
bot.tap(16, -10)

time.sleep(35)

bot.go(-40, -10, bot.tap_height)
bot.go(40, -30, bot.tap_height, 10000)
bot.go(None, None, bot.clearance_height)

time.sleep(0.5)
bot.tap(-16, 10)
bot.tap(-30, 10)
bot.tap(0, -12)
bot.tap(0, -32)
bot.tap(-40, -32)