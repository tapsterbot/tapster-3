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

bot = robot.Robot(PORT, -16, -25, False, 0.1)
keyboard = Keyboard(bot, coordinatesT3, 0)

bot.go(0, 0, 0)
time.sleep(0.5)

bot.tap(10, -64, 0.06, 0.02) #open Apple Music
time.sleep(0.2)
bot.tap(22, -68, 0.06) #open search
time.sleep(0.2)
bot.tap()
time.sleep(1.2)

keyboard.setDelayBetweenKeyPresses(0.05)
keyboard.type("m", False)
time.sleep(0.05)
keyboard.type("r. roboto", False)

time.sleep(0.6)
bot.tap(-12, 16)

#Dance!
for i in range(5):
    bot.go(0, 0, 0)
    time.sleep(0.5)
    bot.go(0, 0, -15)
    time.sleep(0.5)
bot.go(0, 0, 0)
time.sleep(0.5)
bot.go(40, 40, 0)
time.sleep(0.25)
bot.go(-40, 40, 0)
time.sleep(0.25)
bot.go(0, 0, 0)
time.sleep(0.25)
bot.go(40, -40, 0)
time.sleep(0.25)
bot.go(-40, -40, 0)
time.sleep(0.25)

while True:
    bot.go(20, 20, 0)
    time.sleep(0.25)
    bot.go(-20, 20, -15)
    time.sleep(0.25)
    bot.go(-20, -20, 0)
    time.sleep(0.25)
    bot.go(20, -20, -15)
    time.sleep(0.25)