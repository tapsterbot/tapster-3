###################################################################################################
#
#                                Run for All Tapster Robots
#                              --A simple Gcode file runner--
#
#                                       Requirements
# - A Tapster Robot!
# - A serial (USB) connection to the robot
# - Know the port/port number of the robot (i.e. COM3, /dev/ttyUSB0, etc)
# - A Gcode file to run
#
#                                             Usage
# - Uncomment the appropriate bot = robot.Robot() line for your Tapster robot
# - Run with: python3 run.py [ROBOTPORT] [FILEPATH]
# - This program will run every line in the Gcode file regardless of the content. The GRBL firmware
#   on the robot will ignore unknown commands, illegal moves, etc., but know the contents of the file
#   and the intended behavior before running.
#
###################################################################################################

import sys
import robot

if len(sys.argv) > 2: #take in the serial port name and filename from the args
    PORT = sys.argv[1]
    file = open(sys.argv[2], "r")
else:
    print("Please specify a port and a file to run.")
    raise SystemExit

bot = robot.Robot(PORT, -15, -22, False, 0.09) #settings for T3
#bot = robot.Robot(PORT, -22, -34, False, 0.09) #settings for T3+

lines = file.readlines()
for line in lines:
    bot.send(line)