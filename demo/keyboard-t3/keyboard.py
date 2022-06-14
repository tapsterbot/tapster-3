#Keyboard Demo

#iPhone keyboard settings: All autocorrect and auto capitilization off. Caps lock disabled.

#T3 and iPhone XS Max program settings:
#clearance_height = -17
#tap_height = -25
#serialSendRecvDelay = 0.079
#printCoordinates = False
#delayBetweenKeyPresses = 0

import sys
sys.path.append("..")

import robot
import time

keyOffset = 6.8 #spacing between keys
qX = -38
aX = -34
zX = -26
oneX = -36
dashX = -36
coordinatesT3 = {
    "q": [qX, -30],
    "w": [qX + 1*keyOffset, -30],
    "e": [qX + 2*keyOffset, -30],
    "r": [qX + 3*keyOffset, -30],
    "t": [qX + 4*keyOffset + 1, -30],
    "y": [qX + 5*keyOffset, -30],
    "u": [qX + 6*keyOffset, -30],
    "i": [qX + 7*keyOffset, -30],
    "o": [qX + 8*keyOffset + 1, -30],
    "p": [qX + 9*keyOffset, -30],
    "a": [aX, -40],
    "s": [aX + 1*keyOffset, -40],
    "d": [aX + 2*keyOffset, -40],
    "f": [aX + 3*keyOffset, -40],
    "g": [aX + 4*keyOffset, -40],
    "h": [aX + 5*keyOffset, -40],
    "j": [aX + 6*keyOffset, -40],
    "k": [aX + 7*keyOffset, -40],
    "l": [aX + 8*keyOffset, -40],
    "z": [zX, -50],
    "x": [zX + 1*keyOffset, -50],
    "c": [zX + 2*keyOffset, -50],
    "v": [zX + 3*keyOffset, -50],
    "b": [zX + 4*keyOffset, -50],
    "n": [zX + 5*keyOffset, -50],
    "m": [zX + 6*keyOffset, -50],
    " ": [-6, -60],
    "1": [oneX, -30],
    "2": [oneX + 1*keyOffset, -30],
    "3": [oneX + 2*keyOffset, -30],
    "4": [oneX + 3*keyOffset, -30],
    "5": [oneX + 4*keyOffset, -30],
    "6": [oneX + 5*keyOffset, -30],
    "7": [oneX + 6*keyOffset, -30],
    "8": [oneX + 7*keyOffset, -30],
    "9": [oneX + 8*keyOffset, -30],
    "0": [oneX + 9*keyOffset, -30],
    "-": [dashX, -40],
    "/": [dashX + 1*keyOffset, -40],
    ":": [dashX + 2*keyOffset, -40],
    ";": [dashX + 3*keyOffset, -40],
    "(": [dashX + 4*keyOffset, -40],
    ")": [dashX + 5*keyOffset, -40],
    "$": [dashX + 6*keyOffset, -40],
    "&": [dashX + 7*keyOffset, -40],
    "@": [dashX + 8*keyOffset, -40],
    "\"": [dashX + 9*keyOffset, -40],
    ".": [-26, -50],
    ",": [-16, -50],
    "?": [-6, -50],
    "!": [4, -50],
    "\'": [14, -50], #apostrophe
    "shift": [-36, -50],
    "back": [24, -50],
    "numMenu": [-38, -60],
    "\n": [20, -60] #enter
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
stringToType = "The quick brown fox jumped over the lazy dog. \n"
#stringToType = "qqwweerrttyyuuiiooppaassddffgghhjjkkllzzxxccvvbbnnmm"

if __name__ == "__main__":
    if len(sys.argv) > 1: #take in the serial port name from the args
        PORT = sys.argv[1]
    else:
        print("Please specify a port.")
        raise SystemExit

    bot = robot.Robot(PORT, -17, -25, False, 0.079) #set sendPause to 0.079 and printCoordinates to False for faster operation
    keyboard = Keyboard(bot, coordinatesT3, 0)
    for i in range(10):
        keyboard.type(stringToType, True)