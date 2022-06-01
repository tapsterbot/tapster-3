import robot
import time

# TODO: Make this a command line flag...
PORT = "/dev/tty.usbserial-1420"

bot = robot.Robot(PORT)
bot.clearance_height = 0
bot.tap_height = -10

# 123-45-67+89 = 100

def one():
    bot.tap(-25, -35)

def two():
    bot.tap(-8,-35)

def three():
    bot.tap(7,-35)

def four():
    bot.tap(-25, -20)

def five():
    bot.tap(-8, -20)

def six():
    bot.tap(7, -20)

def seven():
    bot.tap(-25, -3)

def eight():
    bot.tap(-8, -3)

def nine():
    bot.tap(7, -3)

def zero():
    pass

def plus():
    bot.tap(22, -35)

def minus():
    bot.tap(22, -18)

def equals():
    bot.tap(22,-52)

def all_clear():
    bot.tap(-25, 13)

def addition_demo():
    one()
    plus()
    one()
    equals()

def one_hundred_demo():
    # 123-45-67+89 = 100
    all_clear()
    one()
    two()
    three()
    minus()
    four()
    five()
    minus()
    six()
    seven()
    plus()
    eight()
    nine()

if __name__ == '__main__':
    one_hundred_demo()