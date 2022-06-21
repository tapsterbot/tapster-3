#Keyboard Demo

#Tab S7 keyboard settings: Using Gboard rather than the default keyboard. All autocorrect and auto capitalization off.

#T3+ and Samsung Galaxy Tab S7 program settings:
#clearance_height = -23
#tap_height = -32
#serialSendRecvDelay = 0.079
#printCoordinates = False
#delayBetweenKeyPresses = 0

import sys
sys.path.append("..")

import robot
import time

keyOffset = 13 #spacing between keys
qX = -56
aX = -50
zX = -42
oneX = -58
atX = -58
backslashX = -44
coordinatesT3Plus = {
    "q": [qX, -73],
    "w": [qX + 1*keyOffset, -73],
    "e": [qX + 2*keyOffset, -73],
    "r": [qX + 3*keyOffset, -73],
    "t": [qX + 4*keyOffset, -73],
    "y": [qX + 5*keyOffset, -73],
    "u": [qX + 6*keyOffset, -73],
    "i": [qX + 7*keyOffset, -73],
    "o": [qX + 8*keyOffset, -73],
    "p": [qX + 9*keyOffset, -73],
    "a": [aX, -85],
    "s": [aX + 1*keyOffset, -85],
    "d": [aX + 2*keyOffset, -85],
    "f": [aX + 3*keyOffset, -85],
    "g": [aX + 4*keyOffset, -85],
    "h": [aX + 5*keyOffset, -85],
    "j": [aX + 6*keyOffset, -85],
    "k": [aX + 7*keyOffset, -85],
    "l": [aX + 8*keyOffset, -85],
    "z": [zX, -101],
    "x": [zX + 1*keyOffset, -101],
    "c": [zX + 2*keyOffset, -101],
    "v": [zX + 3*keyOffset, -101],
    "b": [zX + 4*keyOffset, -101],
    "n": [zX + 5*keyOffset, -101],
    "m": [zX + 6*keyOffset, -101],
    " ": [0, -114],
    "1": [oneX, -74],
    "2": [oneX + 1*keyOffset, -74],
    "3": [oneX + 2*keyOffset, -74],
    "4": [oneX + 3*keyOffset, -74],
    "5": [oneX + 4*keyOffset, -74],
    "6": [oneX + 5*keyOffset, -74],
    "7": [oneX + 6*keyOffset, -74],
    "8": [oneX + 7*keyOffset, -74],
    "9": [oneX + 8*keyOffset, -74],
    "0": [oneX + 9*keyOffset, -74],
    "@": [atX, -90],
    "#": [atX + 1*keyOffset, -90],
    "$": [atX + 2*keyOffset, -90],
    "_": [atX + 3*keyOffset, -90],
    "&": [atX + 4*keyOffset, -90],
    "-": [atX + 5*keyOffset, -90],
    "+": [atX + 6*keyOffset, -90],
    "(": [atX + 7*keyOffset, -90],
    ")": [atX + 8*keyOffset, -90],
    "/": [atX + 9*keyOffset, -90],
    "\\": [backslashX, -102],               #backslash
    "%": [backslashX + 1*keyOffset, -102],
    "*": [backslashX + 2*keyOffset, -102],
    "\"": [backslashX + 3*keyOffset, -102], #quotation mark
    "\'": [backslashX + 4*keyOffset, -102], #apostrophe
    ":": [backslashX + 5*keyOffset, -102],
    ";": [backslashX + 6*keyOffset, -102],
    "!": [backslashX + 7*keyOffset, -102],
    "?": [backslashX + 8*keyOffset, -102],
    ".": [68, -112],
    ",": [-40, -114],
    "shift": [-56, -102],
    "back": [78, -72],
    "numMenu": [-56, -114],
    "\n": [74, -84] #enter
}

class Keyboard:
    def __init__(self, robotObj, coordinates, delayBetweenKeyPresses = 0):
        self.bot = robotObj
        self.coordinates = coordinates
        self.delayBetweenKeyPresses = delayBetweenKeyPresses
    
    def setClearanceHeight(self, val):
        self.bot.clearance_height = val
    
    def setTapHeight(self, val):
        self.bot.tap_height = val
    
    def setSerialSendRecvDelay(self, val): #Advanced users only, recommended value: 0.1
        self.bot.sendPause = val

    def setDelayBetweenKeyPresses(self, val):
        self.delayBetweenKeyPresses = val
    
    def setCoordinates(self, coordinates): #Params: coordinates: a Python dictionary, formatted as above, with the (x, y) coordinates of each key
        self.coordinates = coordinates
    
    def pressKey(self, key):
        self.bot.tap(self.coordinates[key][0], self.coordinates[key][1], self.delayBetweenKeyPresses)
    
    def type(self, stringToType, printData = True):
        self.bot.go(0, 0, 0)
        time.sleep(0.5)
        self.bot.go(self.coordinates[stringToType[0].lower()][0], self.coordinates[stringToType[0].lower()][1], self.bot.clearance_height + 3)

        tStart = time.time()

        for i, let in enumerate(stringToType):
            if let.isupper():
                self.pressKey("shift")
                self.pressKey(let.lower())
            elif let.isnumeric():
                if i == 0 or stringToType[i - 1].isalpha() or stringToType[i - 1] == " ": self.pressKey("numMenu")
                self.pressKey(let)
                if i != len(stringToType) - 1 and stringToType[i + 1].isalpha(): self.pressKey("numMenu")
                if i == len(stringToType) - 1: self.pressKey("numMenu")
            elif not let.isalpha() and not let == " " and not let == "\n":
                if i == 0 or stringToType[i - 1].isalpha() or stringToType[i - 1] == " ": self.pressKey("numMenu")
                self.pressKey(let)
                if i != len(stringToType) - 1 and stringToType[i + 1].isalpha() and let != "\'": self.pressKey("numMenu")
                elif i == len(stringToType) - 1: self.pressKey("numMenu")
            else:
                self.pressKey(let.lower())
        
        if printData:
            print("Time to type: " + str(time.time() - tStart) + " sec")
            print("WPM: " + str(((len(stringToType)/5.0))/((time.time() - tStart)/60.0)))


#======================================#

stringToType = "This is a string being typed on the Tapster T3!\n"
#stringToType = "The quick brown fox jumped over the lazy dog. \n"
#stringToType = "qqwweerrttyyuuiiooppaassddffgghhjjkkllzzxxccvvbbnnmm"

if __name__ == "__main__":
    if len(sys.argv) > 1: #take in the serial port name from the args
        PORT = sys.argv[1]
    else:
        print("Please specify a port.")
        raise SystemExit

    bot = robot.Robot(PORT, -24, -34, False, 0.085) #set sendPause to 0.079 and printCoordinates to False for faster operation
    keyboard = Keyboard(bot, coordinatesT3Plus, 0)
    for i in range(10):
        keyboard.type(stringToType, True)