import sys
sys.path.append("..")

import robot
from keyboard import Keyboard
from keyboard import coordinatesT3
import time

if len(sys.argv) > 1:
    PORT = sys.argv[1]
else:
    print("Please specify a port.")
    raise SystemExit

bot = robot.Robot(PORT, -13, -25, False, 0.1)
keyboard = Keyboard(bot, coordinatesT3, 0)

bot.go(0, 0, 0)
time.sleep(0.5)

bot.tap(10, -64)
time.sleep(2.25)
bot.tap(14, 64, 0.06, 0.03)
time.sleep(1.25)
keyboard.type("tmprkrl85\n", False)
time.sleep(1)
bot.tap(-6, 40)

time.sleep(5.25)
#Dance!
for i in range(3):
    for t in range(16): #16 steps
        bot.go(25*(t/16), -30*(t/16), -10 + ((t-8)**2)/3)
    for t in range(16): #16 steps
        bot.go(-25*(t/16), -30*(t/16), -10 + ((t-8)**2)/3)

bot.go(-8, -72)
time.sleep(0.5)
bot.go(None, None, bot.tap_height)
time.sleep(0.25)
bot.go(-8, -42)
bot.go(None, None, bot.clearance_height)