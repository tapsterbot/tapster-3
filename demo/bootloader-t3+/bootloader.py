import sys
sys.path.append("..")

import robot
import time

#---------------------------------------------------------------------------------------#
#                          Bootloader Demo for Tapster T3+

#Settings for Samsung Galaxy Tab S7:
# - Developer mode enabled
# - OEM Bootloader Unlocking enabled
# - USB Debugging enabled

# - Tablet is SHUT DOWN at the start of the demo.

#---------------------------------------------------------------------------------------#

if len(sys.argv) > 1: #take in the serial port name from the args
    PORT = sys.argv[1]
else:
    print("Please specify a port.")
    raise SystemExit

bot = robot.Robot(PORT, -15, -22, False, 0.09)

bot.pbmGo(False, True, True)

#Plug tablet into PC via USB C cable
while input("Plug the tablet into a PC, then press enter.") != "": pass

bot.pbmGo(False, False, False)
time.sleep(2)
bot.pbmPress(False, False, True) #bail out of the bootloader menu