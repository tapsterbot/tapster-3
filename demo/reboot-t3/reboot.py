###################################################################################################
#
#                                    Reboot Demo for Tapster 3
#                                  Device Used: Google Pixel 5a 5G
#
#                                          Requirements
# - A Push Button Module (PBMv3)
# - Phone is on the home screen
#
###################################################################################################

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

bot.go(0, 0, 0)

bot.pbmPress(True, False, False, 1.25)
bot.tap(0, -18, 0.08, 0.5)

time.sleep(25)

bot.go(0, -60, bot.clearance_height)
time.sleep(0.1)
bot.go(0, -60, bot.tap_height)
bot.go(0, 12, None, 20000)
bot.go(None, None, bot.clearance_height)