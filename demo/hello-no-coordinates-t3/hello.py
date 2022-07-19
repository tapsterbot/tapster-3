import sys
sys.path.append("..")

import time
import robot
from calc import calculator, strToCalc
from cv import checkAnswer

#args: python3 hello.py [robotPort] [cameraPort]

if len(sys.argv) > 1: #take in the serial port name from the args
    PORT = sys.argv[1]
else:
    print("Please specify a port.")
    raise SystemExit

bot = robot.Robot(PORT, -15, -23.5, False, 0.09)
bot.go(0, 0, 0)

#target: 0.1134
calculator(bot, "cc")
calculator(bot, "1+1=")
bot.go(0, 90, 53) #move the bot so the user can see
time.sleep(2)

while True:
    calculator(bot, "cc")
    calculator(bot, "27.0692+186.4*10/1.69420-126/10000=")

    bot.go(0, 90, 53) #move the delta linkages out of the way of the camera

    if checkAnswer(0.1134):
        bot.go(0, 0, 0)
        time.sleep(0.1)
        #Dance! (if it's correct)
        for i in range(4):
            for i in range(2):
                bot.go(60, 0, 33)
                bot.go(0, 0, -15)
                bot.go(-60, 0, 33)
                bot.go(0, 0, -15)
            bot.go(0, 0, -15)
            for i in range(8):
                bot.go(0, 0, -15)
                bot.go(0, 0, 10)
        break