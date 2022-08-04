###################################################################################################
#
#                             Volume and Screenshot Demo for Tapster 3
#                                  Device Used: Google Pixel 5a 5G
#
#                                          Requirements
# - A Push Button Module (PBMv3)
# - A music file is on the screen
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
time.sleep(0.5)

bot.tap(2, -62, 0.1, 0.125)
bot.go(0, 40)
time.sleep(3)
bot.pbmPress(False, True, False, 1.75)
time.sleep(3)
bot.pbmPress(True, False, True, 1)

#Dance!
for i in range(3):
    for t in range(16): #16 steps
        bot.go(25*(t/16), -30*(t/16), -10 + ((t-8)**2)/3)
    for t in range(16): #16 steps
        bot.go(-25*(t/16), -30*(t/16), -10 + ((t-8)**2)/3)