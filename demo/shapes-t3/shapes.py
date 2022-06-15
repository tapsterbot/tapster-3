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

    def drawSVG(self, file, x1, y1, x2, y2, feedRate = 5000, moveDelay = 0.25): #(x1, y1): bottom left corner ; (x2, y2): top right corner
        oldTapHeight = self.bot.tap_height
        self.bot.tap_height = -20 #required for accuracy

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
        for line in lines:
            if line[:2] == "M5": self.bot.go(None, None, self.bot.clearance_height) #gcode commands to start/stop the spindle/put the pen up/down
            elif line[:2] == "M3": self.bot.go(None, None, self.bot.tap_height)
            elif line[:3] == "G0 " or line[:3] == "G1 ":
                line = line[:-2] + " "
                coordinates = [0, 0] #(x, y)
                for i in range(len(line)):
                    if line[i] == 'X': coordinates[0] = float(line[i + 1:line.find(" ", i)]) #translate from string to float
                    elif line[i] == 'Y': coordinates[1] = float(line[i + 1:line.find(" ", i)])
                
                coordinates[0] = round((coordinates[0]*scale) - least[0] + x1, 2)
                coordinates[1] = round((coordinates[1]*scale) - least[1] + y1, 2)
                self.bot.go(coordinates[0], coordinates[1], None, feedRate) #note the slow feed rate, this is for improved accuracy
                time.sleep(moveDelay)
        self.bot.tap_height = oldTapHeight #reset the tap height
        self.bot.send("G1 F35000")


#=========================================================================#

if __name__ == "__main__":
    if len(sys.argv) > 1: #take in the serial port name from the args
        PORT = sys.argv[1]
    else:
        print("Please specify a port.")
        raise SystemExit
    
    draw = Draw(robot.Robot(PORT, -15, -22, False, 0.1))
    draw.bot.go(0, 0, 0)
    time.sleep(0.5)

    draw.drawSVG("hello.svg", -20, -10, 20, 10, 10000, 0)
    draw.drawLine(-20, -20, 20, -20)
    draw.drawLine(-20, 20, 20, 20)
    draw.drawRectangle(-20, -22, 20, -30)
    draw.drawRectangle(-20, 22, 20, 30)

    draw.bot.tap(24, 56, 0.08, 0.06) #clear the screen

    draw.drawStar(0, 0, 20)
    draw.drawCircle(0, 0, 20)
    draw.drawTriangle(-20, -30, 20, -30, 0, -50)

    draw.bot.tap(22, 56, 0.08, 0.06)

    draw.drawSpiral(0, 0, 6*math.pi, 7.5)

    draw.bot.tap(22, 56, 0.08, 0.06)

    draw.drawSVG("bye.svg", -20, 10, 20, 30, 10000, 0)
    draw.drawSVG("tapster.svg", -20, -40, 20, 0, 1500, 0.25)
    draw.bot.go(0, 50, -10)