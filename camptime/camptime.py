# Import modules
import sys
import ast
import colorama
import sched
import time
import threading
import json
from datetime import datetime
from playsound import playsound
from colorama import Fore, Back, Style

# Fun title text and welcome sound
colorama.init()
print('')
print(Fore.RED + ' Welcome to CampTime!')
print('\033[39m')
playsound('sounds/voc_welcome.wav')

# Prompt user for mob they are camping
mobName = input(" Name of mob camping: ")
print('\033[39m')

# Open bestiary text file and read it
file = open("bestiary.txt", "r")
contents = file.read()
dictionary = ast.literal_eval(contents)
file.close()

# Scheduler initialization
s = sched.scheduler(time.time, time.sleep)
t = 0

# Define functions

# Fire up the mob timer


def runMobTimer(mobName, popTime):
    popTime = dictionary.get(mobName)
    popMins = str(popTime / 60)
    playsound('sounds/clock.wav', block=False)
    print(" Respawn time for " + Fore.MAGENTA + mobName + Fore.WHITE + " is " + Fore.GREEN +
          popMins + Fore.WHITE + " minutes. Happy camping!")
    print()
    s.enter(popTime, 1, do_something, (s, popTime))
    for remaining in range(popTime, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(
            Fore.YELLOW + " {:2d}".format(remaining) + Fore.WHITE + " seconds remaining")
        sys.stdout.flush()
        time.sleep(1)
    s.run()

# Grab current time


def printTime():
    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")
    print(" Pop! " + Fore.MAGENTA + mobName + Fore.WHITE +
          " should be up as of " + Fore.GREEN + currentTime)

# Function that runs at beginning of camp timer


def do_something(sc, popTime):
    printTime()
    playsound('sounds/icefreti_atk.wav', block=False)
    s.enter(popTime, 1, do_something, (sc, popTime))
    for remaining in range(popTime, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(
            Fore.YELLOW + " {:2d}".format(remaining) + Fore.WHITE + " seconds remaining")
        sys.stdout.flush()
        time.sleep(1)


def addMob():
    question = (" No such being in the bestiary. Would you like to add it? ")
    answer = input(question + "(y/n): ").lower().strip()
    print("")
    while not(answer == "y" or answer == "yes" or
              answer == "n" or answer == "no"):
        print("Input yes or no")
        answer = input(question + "(y/n):").lower().strip()
        print()
    if answer[0] == "y":
        newMob = input(" What is the exact name of the mob? ")
        print()
        newPopTime = input(
            " How many seconds does it take for this mob to spawn? ")
        print()
        newPopTimeInt = int(newPopTime)
        dictionary[newMob] = int(newPopTimeInt)
        print(" I shall make a note of " + Fore.MAGENTA +
              newMob + Fore.WHITE + ", adventurer. Happy camping!")
        print()
        playsound('sounds/page_turn01.wav')
        import json
        with open('bestiary.txt', 'w') as file:
            # use `json.loads` to do the reverse
            file.write(json.dumps(dictionary))
            file.close()
        runMobTimer(newMob, newPopTimeInt)

    else:
        print(" Very well, adventurer. Now begone!")
        print()
        playsound('sounds/voc_yruhere.wav')
        sys.exit()

# End of function defs


# Check if input is in bestiary already
if mobName in dictionary.keys():
    print(" Ah, yes... " + Fore.MAGENTA + mobName + Fore.WHITE)
    popTime = dictionary.get(mobName)
    print()
    playsound('sounds/page_turn01.wav')
    runMobTimer(mobName, popTime)

# If input is not in bestiary, ask if user wants to add it.
else:
    addMob()
