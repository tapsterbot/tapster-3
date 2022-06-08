#Keyboard Demo

#iPhone settings: All autocorrect and auto capitilization off. Caps lock disabled.

import sys
sys.path.append("..")

import robot
import time

if len(sys.argv) > 1:
    PORT = sys.argv[1]
else:
    print("Please specify a port.")
    raise SystemExit

bot = robot.Robot(PORT, False, 0.079)
bot.clearance_height = -17
bot.tap_height = -25

delayBetweenKeyPresses = 0

stringToType = """
Domo arigato misuta Robotto
Domo arigato misuta Robotto
Mata au hi made
Domo arigato misuta Robotto
Himitsu wo shiritai
You\'re wondering who I am (secret secret I\'ve got a secret)
Machine or mannequin (secret secret I\'ve got a secret)
With parts made in Japan (secret secret I\'ve got a secret)
I am the modern man
I\'ve got a secret I\'ve been hiding under my skin
My heart is human, my blood is boiling, my brain I.B.M.
So if you see me acting strangely, don\'t be surprised
I\'m just a man who needed someone, and somewhere to hide
To keep me alive, just keep me alive
Somewhere to hide to keep me alive
I\'m not a robot without emotions, I\'m not what you see
I\'ve come to help you with your problems, so we can be free
I\'m not a hero, I\'m not a savior, forget what you know
I\'m just a man whose circumstances went beyond his control
Beyond my control, we all need control
I need control, we all need control
I am the modern man (secret secret I\'ve got a secret)
Who hides behind a mask (secret secret I\'ve got a secret)
So no one else can see (secret secret I\'ve got a secret)
My true identity
Domo arigato, Mr. Roboto, domo, domo
Domo arigato, Mr. Roboto, domo, domo
Domo arigato, Mr. Roboto
Domo arigato, Mr. Roboto
Domo arigato, Mr. Roboto
Domo arigato, Mr. Roboto
Thank you very much, Mr. Roboto
For doing the jobs nobody wants to
And thank you very much, Mr. Roboto
For helping me escape to where I needed to
Thank you, thank you, thank you
I want to thank you, please, thank you, oh yeah
The problem\'s plain to see, too much technology
Machines to save our lives, machines dehumanize
The time has come at last (secret secret I\'ve got a secret)
To throw away this mask (secret secret I\'ve got a secret)
Now everyone can see (secret secret I\'ve got a secret)
My true identity
I\'m Kilroy! Kilroy! Kilroy! Kilroy!
"""

stringToType = "Guinness World Records has challenged me to type this sentence using one finger in the fastest time.\n"
stringToType = "abcdefghijklmnopqrstuvwxyz"

keyOffset = 6.8 #spacing between keys
qX = -36.5
aX = -34
zX = -26
oneX = -36
dashX = -36
coordinates = {
    "q": [qX, -30],
    "w": [qX + 1*keyOffset, -30],
    "e": [qX + 2*keyOffset, -30],
    "r": [qX + 3*keyOffset, -30],
    "t": [qX + 4*keyOffset, -30],
    "y": [qX + 5*keyOffset, -30],
    "u": [qX + 6*keyOffset, -30],
    "i": [qX + 7*keyOffset, -30],
    "o": [qX + 8*keyOffset, -30],
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
    "\'": [14, -50],
    "shift": [-36, -50],
    "back": [24, -50],
    "numMenu": [-32, -60],
    "\n": [20, -60] #enter
}

def pressKey(key):
    bot.tap(coordinates[key][0], coordinates[key][1], delayBetweenKeyPresses)
    if key == "shift": time.sleep(0.1)

#==========================================================#

bot.go(0, 0, 0)
time.sleep(0.5)
bot.go(coordinates[stringToType[0].lower()][0], coordinates[stringToType[0].lower()][1], bot.clearance_height + 3)

tStart = time.time()

for i, let in enumerate(stringToType):
    if let.isupper():
        pressKey("shift")
        pressKey(let.lower())
    elif let.isnumeric():
        if i == 0 or stringToType[i - 1].isalpha() or stringToType[i - 1] == " ": pressKey("numMenu")
        pressKey(let)
        if i != len(stringToType) - 1 and stringToType[i + 1].isalpha(): pressKey("numMenu")
        if i == len(stringToType) - 1: pressKey("numMenu")
    elif not let.isalpha() and not let == " " and not let == "\n":
        if i == 0 or stringToType[i - 1].isalpha() or stringToType[i - 1] == " ": pressKey("numMenu")
        pressKey(let)
        if i != len(stringToType) - 1 and stringToType[i + 1].isalpha() and let != "\'": pressKey("numMenu")
        elif i == len(stringToType) - 1: pressKey("numMenu")
    else:
        pressKey(let.lower())

print("Time to type: " + str(time.time() - tStart))
print("WPM: " + str(((len(stringToType)/5.0))/((time.time() - tStart)/60.0)))