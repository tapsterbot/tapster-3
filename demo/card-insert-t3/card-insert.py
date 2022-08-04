###################################################################################################
#
#                                 Card Insert Demo for Tapster T3
#                                  Device Used: ????
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

for i in range(3): #repeat 3 times
    bot.paybotInsert(True)
    time.sleep(1.5)
    bot.paybotInsert(False)
    time.sleep(1.5)