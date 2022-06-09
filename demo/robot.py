import time
import serial

class Robot:
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

    def send(self, command, pause = None):
        message = str.encode(command + '\n')
        self.serial.write(message)
        if pause != None: time.sleep(pause)
        else: time.sleep(self.sendPause)
        result = self.serial.read(self.serial.in_waiting)
        result = result.strip().decode('utf-8')
        if result != "ok":
            print(result)

    def go(self, x = None,y = None, z = None):
        position = ""
        if x != None:
            position += " X" + str(x)
        if y != None:
            position += " Y" + str(y)
        if z != None:
            position += " Z" + str(z)
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
        time.sleep(pause)