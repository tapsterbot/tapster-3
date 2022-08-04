###################################################################################################
#
#                                Robot Class for All Tapster Robots
#
#                                          Requirements
# - A Tapster Robot!
# - A serial (USB) connection to the robot
# - Know the port/port number of the robot (i.e. COM3, /dev/ttyUSB0, etc)
#
#                                             Usage
# - Make a robot object
# - When making the object, set the clearance_height to the height of the stylus when it is moving
#   above the screen, and tap_height to the height of the stylus when it is touching the screen.
# - If you want the coordinates sent to the robot to be printed out to terminal/stdout, set
#   printCoordinates = True. Else set printCoordinates = False.
# - Call the methods you need to move the robot, tap, push buttons on a Push Button Module...
# - To send a command directly, without using a method, call Robot.send().
#
###################################################################################################

import time
import serial

class Robot:
    #PBMv3 Add-on Module Constants (valid range: 100-2000)
    aPressed = 800
    aReleased = 2000
    bPressed = 800
    bReleased = 2000
    cPressed = 800
    cReleased = 2000

    #Paybot Add-on Module Constants
    inserted = 1000
    removed = 2000

    def __init__(self, port, clearance_height = 0, tap_height = 0, printCoordinates = True, sendPause = 0.1):
        self.clearance_height = clearance_height
        self.tap_height = tap_height
        self.printCoordinates = printCoordinates
        self.sendPause = sendPause

        self.serial = serial.Serial(port, 115200)
        # Wake up Grbl firmware
        self.serial.write(b"\r\n\r\n")
        time.sleep(2)   # Wait for Grbl to initialize
        self.serial.flushInput()  # Flush startup text in serial input
        # Set speed
        self.send("G1 F35000")

    def send(self, command, pause = None, printOrReturn = 'p'):
        message = str.encode(command + '\n')
        self.serial.write(message)
        if pause != None: time.sleep(pause)
        else: time.sleep(self.sendPause)

        result = self.serial.read(self.serial.in_waiting)
        result = result.strip().decode('utf-8')
        if result != "ok":
            if printOrReturn == 'p': print(result)
            else: return result

    def go(self, x = None, y = None, z = None, feedRate = None):
        position = ""
        if x != None:
            position += " X" + str(x)
        if y != None:
            position += " Y" + str(y)
        if z != None:
            position += " Z" + str(z)
        if feedRate != None:
            position += " F" + str(feedRate)
        if self.printCoordinates: print(position)
        self.send("G1 " + position)

    def tap(self, x = None,y = None, pause = .06, travelPause = 0):
        position = ""
        if x != None:
            position += " X" + str(x)
        if y != None:
            position += " Y" + str(y)
        if self.printCoordinates: print(position)
        self.send("G1 " + position + " Z" + str(self.clearance_height))
        time.sleep(travelPause)
        self.send("G1 " + position + " Z" + str(self.tap_height))
        time.sleep(pause)
        self.send("G1 " + position + " Z" + str(self.clearance_height))
    
    def pbmGo(self, a = None, b = None, c = None):
        position = ""
        if a != None:
            if a == True: position += " A" + str(self.aPressed)
            elif a == False: position += " A" + str(self.aReleased)
            else: position += " A" + str(a)
        if b != None:
            if b == True: position += " B" + str(self.bPressed)
            elif b == False: position += " B" + str(self.bReleased)
            else: position += " B" + str(b)
        if c != None:
            if c == True: position += " C" + str(self.cPressed)
            elif c == False: position += " C" + str(self.cReleased)
            else: position += " C" + str(c)
        if self.printCoordinates: print(position)
        self.send("G0 " + position)
    
    def pbmPress(self, a = False, b = False, c = False, holdTime = 0.25):
        position = ""
        if a == True: position += " A" + str(self.aPressed)
        elif a == False: position += " A" + str(self.aReleased)
        if b == True: position += " B" + str(self.bPressed)
        elif b == False: position += " B" + str(self.bReleased)
        if c == True: position += " C" + str(self.cPressed)
        elif c == False: position += " C" + str(self.cReleased)

        if self.printCoordinates: print(position)
        self.send("G0 " + position)
        time.sleep(holdTime)
        self.send(f"G0 A{self.aReleased} B{self.bReleased} C{self.cReleased}")

    def paybotGo(self, a = None, b = None, c = None):
        position = ""
        if a != None:
            if a == True: position += " A" + str(self.inserted)
            elif a == False: position += " A" + str(self.removed)
            else: position += " A" + str(a)
        if b != None:
            if b == True: position += " B" + str(self.inserted)
            elif b == False: position += " B" + str(self.removed)
            else: position += " B" + str(b)
        if c != None:
            if c == True: position += " C" + str(self.inserted)
            elif c == False: position += " C" + str(self.removed)
            else: position += " C" + str(c)
        if self.printCoordinates: print(position)
        self.send("G0 " + position)
    
    def paybotInsert(self, a = False, b = False, c = False, holdTime = 0.25):
        position = ""
        if a == True: position += " A" + str(self.inserted)
        elif a == False: position += " A" + str(self.removed)
        if b == True: position += " B" + str(self.inserted)
        elif b == False: position += " B" + str(self.removed)
        if c == True: position += " C" + str(self.inserted)
        elif c == False: position += " C" + str(self.removed)

        if self.printCoordinates: print(position)
        self.send("G0 " + position)
        time.sleep(holdTime)
        self.send(f"G0 A{self.removed} B{self.removed} C{self.removed}")