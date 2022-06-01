import time
import serial

class Robot:
    def __init__(self, port):
        self.clearance_height = 0
        self.tap_height = 0
        self.serial = serial.Serial(port, 115200)
        # Wake up Grbl firmware
        self.serial.write(b"\r\n\r\n")
        time.sleep(2)   # Wait for Grbl to initialize
        self.serial.flushInput()  # Flush startup text in serial input
        # Set speed
        self.send("G1 F30000")

    def send(self, command, pause=.1):
        message = str.encode(command + '\n')
        self.serial.write(message)
        time.sleep(pause)
        result = self.serial.read(self.serial.in_waiting)
        result = result.strip().decode('utf-8')
        if result != "ok":
            print(result)
        else:
            pass

    def go(self, x = None,y = None, z = None):
        position = ""
        if x != None:
            position += " X" + str(x)
        if y != None:
            position += " Y" + str(y)
        if z != None:
            position += " Z" + str(z)
        print(position)
        self.send("G1 " + position)

    def tap(self, x = None,y = None, pause=.04):
        position = ""
        if x != None:
            position += " X" + str(x)
        if y != None:
            position += " Y" + str(y)
        print(position)
        self.send("G1 " + position + " Z" + str(self.clearance_height))
        self.send("G1 " + position + " Z" + str(self.tap_height))
        self.send("G1 " + position + " Z" + str(self.clearance_height))
        time.sleep(pause)