import sys
sys.path.append("..")

import math
import time
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
import robot

if len(sys.argv) > 1: #take in the serial port name from the args
    PORT = sys.argv[1]
else:
    print("Please specify a port.")
    raise SystemExit

bot = robot.Robot(PORT, -17, -23, False, 0.1)

file = "tapster-scaled.svg"
#26, 44
svgX1 = -26 #bottom left corner
svgY1 = -44
svgX2 = 26 #top right corner
svgY2 = 44

# Instantiate a compiler, specifying the interface type and the speed at which the tool should move. pass_depth controls
# how far down the tool moves after every pass. Set it to 0 if your machine does not support Z axis movement.
gcode_compiler = Compiler(interfaces.Gcode, movement_speed=30000, cutting_speed=30000, pass_depth=0)

curves = parse_file(file) # Parse an svg file into geometric curves

gcode_compiler.append_curves(curves) 
gcode_compiler.compile_to_file(file[:-3] + "gcode", passes=2)
gcode = open(file[:-3] + "gcode", 'r')
lines = gcode.readlines()

greatestVal = -10000000000
greatestValLine = ""
greatestValLineNum = 0
for i, line in enumerate(lines):
    if line[:3] == "G0 " or line[:3] == "G1 ":
        xIndex = line.find("X")
        yIndex = line.find("Y")
        xVal = float(line[xIndex + 1:line.find(" ", xIndex) - 1])
        yVal = float(line[yIndex + 1:line.find(" ", yIndex) - 1])
        if xVal > greatestVal:
            greatestVal = xVal
            greatestValLine = line
            greatestValLineNum = i
        if yVal > greatestVal:
            greatestVal = yVal
            greatestValLine = line
            greatestValLineNum = i

print(greatestVal)

bot.go(0, 0, 0)
time.sleep(0.5)
for line in lines:
    if line[:2] == "M5": bot.go(None, None, bot.clearance_height)
    elif line[:2] == "M3": bot.go(None, None, bot.tap_height)
    elif line[:3] == "G0 " or line[:3] == "G1 ":
        line = line[:-2] + " "
        coordinates = [0, 0] #(x, y)
        for i in range(len(line)):
            if line[i] == 'X': coordinates[0] = float(line[i + 1:line.find(" ", i)]) #translate from string to float
            elif line[i] == 'Y': coordinates[1] = float(line[i + 1:line.find(" ", i)])
        coordinates[0] = round(((svgX2 - svgX1)/greatestVal)*coordinates[0] + svgX1, 3)
        coordinates[1] = round(((svgY2 - svgY1)/greatestVal)*coordinates[1] + svgY1, 3)
        print(coordinates)
        bot.go(coordinates[0], coordinates[1], None, 5000)
        time.sleep(0.25)

bot.go(0, 0, 0)