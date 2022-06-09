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

bot = robot.Robot(PORT, -17, -25, False, 0.079) #set sendPause to 0.079 and printCoordinates to False for faster operation

class Draw:
    def __init__(self, robotObj):
        self.bot = robotObj
    
    def setClearanceHeight(self, val):
        self.bot.clearance_height = val
    
    def setTapHeight(self, val):
        self.bot.tap_height = val
    
    def drawLine(self, x1, y1, x2, y2):
        self.bot.go(x1, y1)
        self.bot.go(x1, y1, self.bot.tap_height)
        self.bot.go(x2, y2)
        self.bot.go(x2, y2, self.bot.clearance_height)
    
    def drawCartesianCurve(self, expressionSolvedForY, xStart, xEnd, numSteps): #Params: expressionSolvedForY is a lambda expression of the curve, in terms of x/solved for y
        for x in range(xStart, xEnd, (float(xEnd - xStart))/numSteps):
            self.bot.go(x, expressionSolvedForY(x), self.bot.tap_height)
        self.bot.go(None, None, self.bot.clearance_height)
    
    def drawParametricCurve(self, x, y, tStart, tEnd, numSteps): #Params: x and y are lambda expressions in terms of t
        for t in range(tStart, tEnd, (float(tEnd - tStart))/numSteps):
            self.bot.go(x(t), y(t), self.bot.tap_height)
        self.bot.go(None, None, self.bot.clearance_height)
    
    def drawCircle(self, x, y, radius):
        self.drawParametricCurve(lambda t : radius*math.cos(t) + x, lambda t : radius*math.sin(t) + y, 0, 2*math.pi, 16)
    
    def drawTriangle(self, x1, y1, x2, y2, x3, y3):
        self.drawLine(x1, y1, x2, y2)
        self.drawLine(x2, y2, x3, y3)
        self.drawLine(x3, y3, x1, y1)

    def drawRectangle(self, x1, y1, x2, y2):
        self.drawLine(x1, y1, x2, y1)
        self.drawLine(x2, y1, x2, y2)
        self.drawLine(x2, y2, x1, y2)
        self.drawLine(x1, y2, x1, y1)

    def drawSpiral(self, x, y, tEnd, radiusGrowthPerRev):
        self.drawParametricCurve(lambda t : radiusGrowthPerRev*(t/(2*math.pi))*math.cos(t),
                                 lambda t : radiusGrowthPerRev*(t/(2*math.pi))*math.sin(t), 0, tEnd, (tEnd/(2*math.pi))*16)

    def drawStar(self, x, y, radius):
        pass #implement this later

    def drawSVG(self, file):
        # Instantiate a compiler, specifying the interface type and the speed at which the tool should move. pass_depth controls
        # how far down the tool moves after every pass. Set it to 0 if your machine does not support Z axis movement.
        gcode_compiler = Compiler(interfaces.Gcode, movement_speed=30000, cutting_speed=30000, pass_depth=0)

        curves = parse_file(file) # Parse an svg file into geometric curves

        gcode_compiler.append_curves(curves) 
        gcode_compiler.compile_to_file(file[:3] + "gcode", passes=2)
        gcode = open(file[:3] + "gcode", 'r')
        #figure the rest of this out


#=========================================================================#

if __name__ == "__main__":
    if len(sys.argv) > 1: #take in the serial port name from the args
        PORT = sys.argv[1]
    else:
        print("Please specify a port.")
        raise SystemExit
    
    bot = robot.Robot(PORT, -17, -25, False, 0.1)
    draw = Draw(bot)