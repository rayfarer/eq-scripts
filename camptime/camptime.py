import sys
import colorama
import sched
import time
import threading
from datetime import datetime
from playsound import playsound
from colorama import Fore, Back, Style


# Fun title text
colorama.init()
print('')

print('\033[31m' + ' Welcome to Camp Time!')
print('\033[39m')
playsound('icefreti_atk.wav')

mobname = input(" Name of mob camping: ")
print("")

# The bestiary has mob types and their respawn times
bestiary = {
    "an ice giant": 480
}

popTime = bestiary.get('an ice giant')
popMins = str(popTime / 60)
print(" Respawn time for " + mobname + " is " +
      popMins + " minutes. Happy camping!")

s = sched.scheduler(time.time, time.sleep)
t = 0


def printTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)


def minuteElapsed():
    threading.Timer(60.0, printTime).start()  # called every minute


def do_something(sc):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(" Pop! " + mobname + " should be up as of ", current_time)
    # do your stuff
    playsound('icefreti_atk.wav')
    s.enter(popTime, 1, do_something, (sc,))


s.enter(popTime, 1, do_something, (s,))
for remaining in range(popTime, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining))
    sys.stdout.flush()
    time.sleep(1)
s.run()