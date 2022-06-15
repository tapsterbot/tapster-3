import sys
sys.path.append("..")

import math
import time
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
import robot

class Draw:
    def __init__(self, robotObj, feedRate = 35000):
        self.bot = robotObj
        self.feedRate = feedRate
    
    def setClearanceHeight(self, val):
        self.bot.clearance_height = val
    
    def setTapHeight(self, val):
        self.bot.tap_height = val
    
    def setFeedRate(self, val):
        self.feedRate = val
    
    def drawLine(self, x1, y1, x2, y2, pickUpPen = True, moveDelay = 0):
        self.bot.go(round(x1, 4), round(y1, 4))
        self.bot.go(round(x1, 4), round(y1, 4), self.bot.tap_height)
        time.sleep(moveDelay)
        self.bot.go(round(x2, 4), round(y2, 4))
        if pickUpPen: self.bot.go(round(x2, 4), round(y2, 4), self.bot.clearance_height)
    
    def drawCartesianCurve(self, expressionSolvedForY, xStart, xEnd, numSteps): #Params: expressionSolvedForY is a lambda expression of the curve, in terms of x/solved for y
        x = float(xStart)
        self.bot.go(round(x, 2), round(expressionSolvedForY(x), 2))
        self.bot.go(round(x, 2), round(expressionSolvedForY(x), 2), bot.tap_height)
        time.sleep(0.05)
        while x < xEnd:
            x += (float(xEnd - xStart))/numSteps
            self.bot.go(round(x, 2), round(expressionSolvedForY(x), 2))
        self.bot.go(None, None, self.bot.clearance_height)
    
    def drawParametricCurve(self, x, y, tStart, tEnd, numSteps): #Params: x and y are lambda expressions in terms of t
        t = float(tStart)
        self.bot.go(round(x(t), 2), round(y(t), 2))
        self.bot.go(round(x(t), 2), round(y(t), 2), bot.tap_height)
        time.sleep(0.05)
        while t < tEnd:
            t += (float(tEnd - tStart))/numSteps
            self.bot.go(round(x(t), 2), round(y(t), 2))
        self.bot.go(None, None, self.bot.clearance_height)
    
    def drawCircle(self, x, y, radius):
        self.drawParametricCurve(lambda t : radius*math.cos(t) + x, lambda t : radius*math.sin(t) + y, 0, 2*math.pi, 16)
    
    def drawTriangle(self, x1, y1, x2, y2, x3, y3):
        self.drawLine(x1, y1, x2, y2, False, 0.05)
        self.drawLine(x2, y2, x3, y3, False)
        self.drawLine(x3, y3, x1, y1, True)

    def drawRectangle(self, x1, y1, x2, y2):
        self.drawLine(x1, y1, x2, y1, False, 0.05)
        self.drawLine(x2, y1, x2, y2, False)
        self.drawLine(x2, y2, x1, y2, False)
        self.drawLine(x1, y2, x1, y1, True)

    def drawSpiral(self, x, y, tEnd, radiusGrowthPerRev):
        self.drawParametricCurve(lambda t : radiusGrowthPerRev*(t/(2*math.pi))*math.cos(t),
                                 lambda t : radiusGrowthPerRev*(t/(2*math.pi))*math.sin(t), 0, tEnd, (tEnd/(2*math.pi))*16)

    def drawStar(self, x, y, radius):
        starAngleConst = (2*math.pi)/5
        self.drawLine(radius*math.cos(math.pi/2) + x, radius*math.sin(math.pi/2) + y,
                      radius*math.cos(math.pi/2 + 2*starAngleConst) + x, radius*math.sin(math.pi/2 + 2*starAngleConst) + y, False, 0.05)
        self.drawLine(radius*math.cos(math.pi/2 + 2*starAngleConst) + x, radius*math.sin(math.pi/2 + 2*starAngleConst) + y,
                      radius*math.cos(math.pi/2 + 4*starAngleConst) + x, radius*math.sin(math.pi/2 + 4*starAngleConst) + y, False)
        self.drawLine(radius*math.cos(math.pi/2 + 4*starAngleConst) + x, radius*math.sin(math.pi/2 + 4*starAngleConst) + y,
                      radius*math.cos(math.pi/2 + 1*starAngleConst) + x, radius*math.sin(math.pi/2 + 1*starAngleConst) + y, False)
        self.drawLine(radius*math.cos(math.pi/2 + 1*starAngleConst) + x, radius*math.sin(math.pi/2 + 1*starAngleConst) + y,
                      radius*math.cos(math.pi/2 + 3*starAngleConst) + x, radius*math.sin(math.pi/2 + 3*starAngleConst) + y, False)
        self.drawLine(radius*math.cos(math.pi/2 + 3*starAngleConst) + x, radius*math.sin(math.pi/2 + 3*starAngleConst) + y,
                      radius*math.cos(math.pi/2) + x, radius*math.sin(math.pi/2) + y, True)

    def drawSVG(self, file):
        # Instantiate a compiler, specifying the interface type and the speed at which the tool should move. pass_depth controls
        # how far down the tool moves after every pass. Set it to 0 if your machine does not support Z axis movement.
        gcode_compiler = Compiler(interfaces.Gcode, movement_speed=30000, cutting_speed=30000, pass_depth=0)

        curves = parse_file(file) # Parse an svg file into geometric curves

        gcode_compiler.append_curves(curves) 
        gcode_compiler.compile_to_file(file[:-3] + "gcode", passes=2)
        gcode = open(file[:-3] + "gcode", 'r')
        lines = gcode.readlines()
        


#=========================================================================#

if __name__ == "__main__":
    if len(sys.argv) > 1: #take in the serial port name from the args
        PORT = sys.argv[1]
    else:
        print("Please specify a port.")
        raise SystemExit
    
    bot = robot.Robot(PORT, -17, -22, False, 0.1)
    bot.go(0, 0, 0)
    draw = Draw(bot)
    #test in repl