###################################################################################################
#
#                              Shapes and Drawing Demo for Tapster 3+
#                                    Device Used: Samsung Galaxy Tab S7
#
#                                          Requirements
# - The svgToGcode Python module
# - The Samsung Notes app (or any other drawing app, i.e. Autodesk Sketchbook)
# - The phone has the drawing app open
#
#                                          Special Usage
# - This demo contains the Draw class, which includes a wide variety of methods for drawing shapes,
#   drawing from SVGs, and drawing curves. This class is portable to any device, and does not
#   require any dictionaries of data as every point for drawing is specified in the method calls.
# - The Draw.svgDraw() takes in an SVG from a program such as Inkscape, and converts it to robot
#   movements. The file it takes in is specified in the *method call*, not in a command argument.
#   It also must be in the working directory.
#
#                                              Note
# - This file is not substantially different from the /shapes-t3/shapes.py file. The only changed
#   values are in the constructor for the Draw object, to T3+ specific tap and clearance heights,
#   and the coordinates for the bounding box in the call to Draw.drawSVG(). The Draw class is identical.
#
###################################################################################################

import sys
sys.path.append("..")

import math
import time
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
import robot

class Draw:
    def __init__(self, robotObj):
        self.bot = robotObj
    
    def setClearanceHeight(self, val):
        self.bot.clearance_height = val
    
    def setTapHeight(self, val):
        self.bot.tap_height = val
    
    def drawLine(self, x1, y1, x2, y2, pickUpPen = True, moveDelay = 0):
        self.bot.go(round(x1, 4), round(y1, 4))
        self.bot.go(round(x1, 4), round(y1, 4), self.bot.tap_height)
        time.sleep(moveDelay)
        self.bot.go(round(x2, 4), round(y2, 4))
        if pickUpPen: self.bot.go(round(x2, 4), round(y2, 4), self.bot.clearance_height)
    
    def drawCartesianCurve(self, expressionSolvedForY, xStart, xEnd, numSteps): #Params: expressionSolvedForY is a lambda expression of the curve, in terms of x/solved for y
        x = float(xStart)
        self.bot.go(round(x, 2), round(expressionSolvedForY(x), 2))
        self.bot.go(round(x, 2), round(expressionSolvedForY(x), 2), self.bot.tap_height)
        time.sleep(0.05)
        while x < xEnd:
            x += (float(xEnd - xStart))/numSteps
            self.bot.go(round(x, 2), round(expressionSolvedForY(x), 2))
        self.bot.go(None, None, self.bot.clearance_height)
    
    def drawParametricCurve(self, x, y, tStart, tEnd, numSteps): #Params: x and y are lambda expressions in terms of t
        t = float(tStart)
        self.bot.go(round(x(t), 2), round(y(t), 2))
        self.bot.go(round(x(t), 2), round(y(t), 2), self.bot.tap_height)
        time.sleep(0.05)
        while t < tEnd:
            t += (float(tEnd - tStart))/numSteps
            self.bot.go(round(x(t), 2), round(y(t), 2))
        self.bot.go(None, None, self.bot.clearance_height)
    
    def drawCircle(self, x, y, radius):
        self.drawParametricCurve(lambda t : radius*math.cos(t) + x, lambda t : radius*math.sin(t) + y, 0, 2*math.pi, 16)
    
    def drawTriangle(self, x1, y1, x2, y2, x3, y3): #Params: The 3 points of the triangle
        self.drawLine(x1, y1, x2, y2, False, 0.05)
        self.drawLine(x2, y2, x3, y3, False)
        self.drawLine(x3, y3, x1, y1, True)

    def drawRectangle(self, x1, y1, x2, y2): #Params: 2 siagonal corners, the bottom left and top right.
        self.drawLine(x1, y1, x2, y1, False, 0.05)
        self.drawLine(x2, y1, x2, y2, False)
        self.drawLine(x2, y2, x1, y2, False)
        self.drawLine(x1, y2, x1, y1, True)

    def drawSpiral(self, x, y, tEnd, radiusGrowthPerRev):
        self.drawParametricCurve(lambda t : radiusGrowthPerRev*(t/(2*math.pi))*math.cos(t) + x,
                                 lambda t : radiusGrowthPerRev*(t/(2*math.pi))*math.sin(t) + y, 0, tEnd, (tEnd/(2*math.pi))*16)

    def drawStar(self, x, y, radius, rotation): #Params: (x, y) coordinates of the center, the radius of the star, and the rotation in radians
        starAngleConst = (2*math.pi)/5
        self.drawLine(radius*math.cos(math.pi/2 + rotation) + x, radius*math.sin(math.pi/2 + rotation) + y,
                      radius*math.cos(math.pi/2 + 2*starAngleConst + rotation) + x, radius*math.sin(math.pi/2 + 2*starAngleConst + rotation) + y, False, 0.05)
        self.drawLine(radius*math.cos(math.pi/2 + 2*starAngleConst + rotation) + x, radius*math.sin(math.pi/2 + 2*starAngleConst + rotation) + y,
                      radius*math.cos(math.pi/2 + 4*starAngleConst + rotation) + x, radius*math.sin(math.pi/2 + 4*starAngleConst + rotation) + y, False)
        self.drawLine(radius*math.cos(math.pi/2 + 4*starAngleConst + rotation) + x, radius*math.sin(math.pi/2 + 4*starAngleConst + rotation) + y,
                      radius*math.cos(math.pi/2 + 1*starAngleConst + rotation) + x, radius*math.sin(math.pi/2 + 1*starAngleConst + rotation) + y, False)
        self.drawLine(radius*math.cos(math.pi/2 + 1*starAngleConst + rotation) + x, radius*math.sin(math.pi/2 + 1*starAngleConst + rotation) + y,
                      radius*math.cos(math.pi/2 + 3*starAngleConst + rotation) + x, radius*math.sin(math.pi/2 + 3*starAngleConst + rotation) + y, False)
        self.drawLine(radius*math.cos(math.pi/2 + 3*starAngleConst + rotation) + x, radius*math.sin(math.pi/2 + 3*starAngleConst + rotation) + y,
                      radius*math.cos(math.pi/2 + rotation) + x, radius*math.sin(math.pi/2 + rotation) + y, True)

    #            SVG Drawing Method
    # Params:
    # - x1, y1, x2, y2 : the coordinates for the 'box' to draw the svg in on the phone screen.
    # - pickUpPen : a threshold for picking up the pen. This threshold is measured when the program encounters a command to pick up
    #               the pen -- it is the distance between the current position of the robot and the position it will move to after
    #               the pick-up command. If the distance is less than pickUpPen, the command will be ignored. Set to 0 to never pick it up.
    # - feedRate : Feed rate override for this method only. Will run the svg drawer with that feed rate, and then reset to machine default (35000)
    # - moveDelay : the delay in between each of the moves/points along the svg curves.
    # - tapHeightOverride : changes the tap height for this method only, sometimes required for better accuracy. Resets at the end of the method.
    def drawSVG(self, file, x1, y1, x2, y2, pickUpPen = 0, feedRate = 5000, moveDelay = 0.25, tapHeightOverride = None): #(x1, y1): bottom left corner ; (x2, y2): top right corner
        oldTapHeight = self.bot.tap_height
        if tapHeightOverride != None: self.bot.tap_height = tapHeightOverride #sometimes required for accuracy

        # Instantiate a compiler, specifying the interface type and the speed at which the tool should move. pass_depth controls
        # how far down the tool moves after every pass. Set it to 0 if your machine does not support Z axis movement.
        gcode_compiler = Compiler(interfaces.Gcode, movement_speed=30000, cutting_speed=30000, pass_depth=0)

        curves = parse_file(file) # Parse an svg file into geometric curves

        gcode_compiler.append_curves(curves) 
        gcode_compiler.compile_to_file(file[:-3] + "gcode", passes = 1) #passes = 1, only calculate 1 pass
        gcode = open(file[:-3] + "gcode", 'r')
        lines = gcode.readlines()
        
        #Find the x and y ranges of the gcode file
        greatest = [-1000000, -1000000] #(x, y)
        least = [1000000, 1000000] #(x, y)
        for i, line in enumerate(lines):
            if line[:3] == "G0 " or line[:3] == "G1 ":
                xIndex = line.find("X")
                yIndex = line.find("Y")
                xVal = float(line[xIndex + 1:line.find(" ", xIndex) - 1])
                yVal = float(line[yIndex + 1:line.find(" ", yIndex) - 1])
                if xVal > greatest[0]: greatest[0] = xVal
                if yVal > greatest[1]: greatest[1] = yVal
                if xVal < least[0]: least[0] = xVal
                if yVal < least[1]: least[1] = yVal
        
        #calculate the scale fraction for the svg and the specified coordinates
        scale = 1
        if abs((x2-x1)/(greatest[0] - least[0])) < abs((y2 - y1)/(greatest[1] - least[1])): scale = abs((x2 - x1)/(greatest[0] - least[0]))
        else: scale = abs((y2 - y1)/(greatest[1] - least[1]))

        #go through the gcode lines, send commands to the robot
        current = [1000, 1000] #keeps track of the current robot position
        for a, line in enumerate(lines):
            if line[:2] == "M5" and pickUpPen: #gcode commands to start/stop the spindle/put the pen up/down
                if a == len(lines) - 1: #prevent exceptions
                    self.bot.go(None, None, self.bot.clearance_height)
                    break
                line = lines[a + 1][:-2] + " "
                coordinates = [0, 0] #(x, y)
                for i in range(len(line)):
                    if line[i] == 'X': coordinates[0] = float(line[i + 1:line.find(" ", i)]) #translate from string to float
                    elif line[i] == 'Y': coordinates[1] = float(line[i + 1:line.find(" ", i)])
                coordinates[0] = round((coordinates[0] - least[0])*scale + x1, 2)
                coordinates[1] = round((coordinates[1] - least[1])*scale + y1, 2)

                if math.dist(current, coordinates) > pickUpPen:
                    self.bot.go(None, None, self.bot.clearance_height)
            elif line[:2] == "M3": self.bot.go(None, None, self.bot.tap_height)
            elif line[:3] == "G0 " or line[:3] == "G1 ":
                line = line[:-2] + " "
                coordinates = [0, 0] #(x, y)
                for i in range(len(line)):
                    if line[i] == 'X': coordinates[0] = float(line[i + 1:line.find(" ", i)]) #translate from string to float
                    elif line[i] == 'Y': coordinates[1] = float(line[i + 1:line.find(" ", i)])
                
                coordinates[0] = round((coordinates[0] - least[0])*scale + x1, 2)
                coordinates[1] = round((coordinates[1] - least[1])*scale + y1, 2)
                self.bot.go(coordinates[0], coordinates[1], None, feedRate) #note the slow default feed rate, this is for improved accuracy
                time.sleep(moveDelay)
                current = coordinates
        self.bot.tap_height = oldTapHeight #reset the tap height
        self.bot.send("G1 F35000")


#=========================================================================#

if __name__ == "__main__":
    if len(sys.argv) > 1: #take in the serial port name from the args
        PORT = sys.argv[1]
    else:
        print("Please specify a port.")
        raise SystemExit
    
    draw = Draw(robot.Robot(PORT, -24, -30, False, 0.09))
    draw.bot.go(0, 0, 0)
    time.sleep(0.5)

    draw.drawSVG("hello.svg", -60, -90, 45, 75, 14, 10000, 0, -30)

    draw.bot.go(0, 65, 10)