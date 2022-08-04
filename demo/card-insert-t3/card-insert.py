###################################################################################################
#
#                                 Card Insert Demo for Tapster 3
#                                     Device Used: PAX A920
#
#                                          Requirements
# - A Paybot Add-on Module, with a card mounted
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

bot = robot.Robot(PORT, -17, -25, False, 0.079) #set sendPause to 0.079 and printCoordinates to False for faster operation

bot.inserted = 790 #device-specific rotation values for the Paybot module. change these to work with your device.
bot.removed = 1900

for i in range(3): #repeat 3 times
    bot.paybotInsert(True, None, None, 1.5)
    time.sleep(1.5)