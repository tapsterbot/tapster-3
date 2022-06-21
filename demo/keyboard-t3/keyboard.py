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
q = (-38, -30)
a = (-34, -40)
z = (-26, -50)
one = (-36, -30)
dash = (-36, -40)

#Coordinate Dictionary Setup:
# - Each entry is a key on the keyboard.
# - Each entry is a tuple, set up as such: (xCoordinate, yCoordinate, menu indicator)
# - The indicator tells the program the behavior of the button, see table below:

#Indicator Value | Keyboard Behavior
# 0 or no value  | On the main QWERTY layout, is NOT in the numbers/special characters menu
# 1              | In the numbers/special characters menu, and DOES NOT return to the QWERTY layout when it is pressed
# 2              | In the numbers/special characters menu, DOES return to the QWERTY layout when it is pressed (i.e. period on some keyboards)
# 3              | Present in BOTH the QWERTY layout AND special characters menu (locations MUST be the same), returns to QWERTY layout after pressed (i.e. space bar)

#NOTE: Use Option 3 only if you are going for maximum typing speed. Due to inconsistencies in keyboard behavior,
#      it may not always work. Use Option 0 instead.

coordinatesT3Plus = {
    "q": (q[0], q[1]),
    "w": (q[0] + 1*keyOffset, q[1]),
    "e": (q[0] + 2*keyOffset, q[1]),
    "r": (q[0] + 3*keyOffset, q[1]),
    "t": (q[0] + 4*keyOffset, q[1]),
    "y": (q[0] + 5*keyOffset, q[1]),
    "u": (q[0] + 6*keyOffset, q[1]),
    "i": (q[0] + 7*keyOffset, q[1]),
    "o": (q[0] + 8*keyOffset, q[1]),
    "p": (q[0] + 9*keyOffset, q[1]),
    "a": (a[0], a[1]),
    "s": (a[0] + 1*keyOffset, a[1]),
    "d": (a[0] + 2*keyOffset, a[1]),
    "f": (a[0] + 3*keyOffset, a[1]),
    "g": (a[0] + 4*keyOffset, a[1]),
    "h": (a[0] + 5*keyOffset, a[1]),
    "j": (a[0] + 6*keyOffset, a[1]),
    "k": (a[0] + 7*keyOffset, a[1]),
    "l": (a[0] + 8*keyOffset, a[1]),
    "z": (z[0], z[1]),
    "x": (z[0] + 1*keyOffset, z[1]),
    "c": (z[0] + 2*keyOffset, z[1]),
    "v": (z[0] + 3*keyOffset, z[1]),
    "b": (z[0] + 4*keyOffset, z[1]),
    "n": (z[0] + 5*keyOffset, z[1]),
    "m": (z[0] + 6*keyOffset, z[1]),
    " ": (0, -114, 3),
    "1": (one[0], one[1], 1),
    "2": (one[0] + 1*keyOffset, one[1], 1),
    "3": (one[0] + 2*keyOffset, one[1], 1),
    "4": (one[0] + 3*keyOffset, one[1], 1),
    "5": (one[0] + 4*keyOffset, one[1], 1),
    "6": (one[0] + 5*keyOffset, one[1], 1),
    "7": (one[0] + 6*keyOffset, one[1], 1),
    "8": (one[0] + 7*keyOffset, one[1], 1),
    "9": (one[0] + 8*keyOffset, one[1], 1),
    "0": (one[0] + 9*keyOffset, one[1], 1),
    "-": (dash[0], dash[1], 1),
    "/": (dash[0] + 1*keyOffset, dash[1], 1),
    ":": (dash[0] + 2*keyOffset, dash[1], 1),
    ";": (dash[0] + 3*keyOffset, dash[1], 1),
    "(": (dash[0] + 4*keyOffset, dash[1], 1),
    ")": (dash[0] + 5*keyOffset, dash[1], 1),
    "$": (dash[0] + 6*keyOffset, dash[1], 1),
    "&": (dash[0] + 7*keyOffset, dash[1], 1),
    "@": (dash[0] + 8*keyOffset, dash[1], 1),
    "\"": (dash[0] + 9*keyOffset, dash[1], 1),
    ".": (-26, -50, 1),               #backslash
    ",": (-16, -50, 1),
    "?": (-6, -50, 1),
    "!": (4, -50, 1), #quotation mark
    "\'": (14, -50, 2), #apostrophe
    "shift": (-36, -50, 0),
    "back": (24, -50, 0),
    "numMenu": (-38, -60),
    "\n": (20, -60, 3) #enter
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

        inNumMenu = False

        for i, let in enumerate(stringToType):
            if let.isupper():
                self.pressKey("shift")
                self.pressKey(let.lower())
            else:
                if len(self.coordinates[let]) == 2 or self.coordinates[let][2] == 0: self.pressKey(let) #normal key on the QWERTY layout
                elif self.coordinates[let][2] == 3: #key that is in both the standard and number menu
                    self.pressKey(let)
                    inNumMenu = False
                else: #anything in the special characters menu
                    if not inNumMenu: self.pressKey("numMenu")
                    inNumMenu = True
                    self.pressKey(let)
                    if self.coordinates[let][2] == 2: inNumMenu = False
                    if (len(self.coordinates[stringToType[i + 1].lower()]) == 2 or self.coordinates[stringToType[i + 1].lower()][2] == 0) and inNumMenu:
                        self.pressKey("numMenu") #if the next letter is not in the number menu, leave the number menu
                        inNumMenu = False
        
        if printData:
            print("Time to type: " + str(time.time() - tStart) + " sec")
            print("WPM: " + str(((len(stringToType)/5.0))/((time.time() - tStart)/60.0)))


#======================================#

stringToType = "This is a string being typed on the Tapster T3+!\n"

if __name__ == "__main__":
    if len(sys.argv) > 1: #take in the serial port name from the args
        PORT = sys.argv[1]
    else:
        print("Please specify a port.")
        raise SystemExit

    bot = robot.Robot(PORT, -22, -34, False, 0.09) #set sendPause to 0.079 and printCoordinates to False for faster operation
    keyboard = Keyboard(bot, coordinatesT3Plus, 0)

    if len(sys.argv) > 2:
        try: file = open(sys.argv[2], "r") #open a file of text to type
        except FileNotFoundError:
            print("The file you specified cannot be found. Please try again.")
            raise SystemExit
        stringToType = file.read()

    keyboard.type(stringToType, True)