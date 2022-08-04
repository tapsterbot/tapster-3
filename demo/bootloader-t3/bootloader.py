###################################################################################################
#
#                                  Bootloader Demo for Tapster 3
#                                  Device Used: Google Pixel 5a 5G
#
#                                          Requirements
# - A Push Button Module (PBMv3)
# - Developer settings are enabled
# - OEM Unlocking is enabled
# - The phone is shut down
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

bot.pbmGo(True, False, True)
time.sleep(5)
bot.pbmGo(False, False, True)
time.sleep(0.25)
bot.pbmGo(False, False, False)

for i in range(5): bot.pbmPress(False, False, True, 0.5)

bot.pbmPress(True)