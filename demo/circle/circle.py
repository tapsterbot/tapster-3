###################################################################################################
#
#                                Circle Movement Demo for Tapster 3/3+
#                                        Device Used: Any
#
#                                          Requirements
# - None
#
###################################################################################################

import sys
sys.path.append("..")

import time
import math
import robot

if len(sys.argv) > 1:
    PORT = sys.argv[1]
else:
    print("Please specify a port.")
    raise SystemExit

bot = robot.Robot(PORT)
bot.clearance_height = 0
bot.tap_height = -10

t = 0
radius = 16

while True:
    bot.go(radius*((int(10000000*math.cos(t)))/10000000), radius*((int(10000000*math.sin(t))/10000000)))
    t += math.pi/8