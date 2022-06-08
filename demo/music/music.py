import sys
sys.path.append("..")

import robot
import time

if len(sys.argv) > 1:
    PORT = sys.argv[1]
else:
    print("Please specify a port.")
    raise SystemExit

bot = robot.Robot(PORT)
bot.clearance_height = 0
bot.tap_height = -10


#Music demo: open a music app, play a song.

#open spotify, go to search, search something, click play.