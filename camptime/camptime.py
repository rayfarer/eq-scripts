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

file = open("bestiary.txt", "r")

contents = file.read()
dictionary = ast.literal_eval(contents)

s = sched.scheduler(time.time, time.sleep)
t = 0

file.close()

def runMobTimer(mobName, popTime):
    popTime = dictionary.get(mobName)
    popMins = str(popTime / 60)
    playsound('sounds/clock.wav', block=False)
    print(" Respawn time for " + mobName + " is " + Fore.GREEN + popMins + Fore.WHITE + " minutes. Happy camping!")
    print()
    s.enter(popTime, 1, do_something, (s, popTime))
    for remaining in range(popTime, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(Fore.CYAN + " {:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
    s.run()

def printTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)


def minuteElapsed():
    threading.Timer(60.0, printTime).start()  # called every minute


def do_something(sc, popTime):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(" Pop! " + mobName + " should be up as of ", current_time)
    # do your stuff
    playsound('sounds/icefreti_atk.wav', block=False)
    s.enter(popTime, 1, do_something, (sc, popTime))
    for remaining in range(popTime, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(Fore.CYAN + " {:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

if mobName in dictionary.keys():
    print(" Ah, yes... " + mobName)
    popTime = dictionary.get(mobName)
    print()
    playsound('sounds/page_turn01.wav')
    runMobTimer(mobName, popTime)

else:
    question = (" No such being in the bestiary. Would you like to add it? ")
    answer = input(question + "(y/n): ").lower().strip()
    print("")
    while not(answer == "y" or answer == "yes" or \
    answer == "n" or answer == "no"):
        print("Input yes or no")
        answer = input(question + "(y/n):").lower().strip()
        print()
    if answer[0] == "y":
        newMob = input(" What is the exact name of the mob? ")
        print()
        newPopTime = input(" How many seconds does it take for this mob to spawn? ")
        print()
        newPopTimeInt = int(newPopTime)
        dictionary[newMob] = int(newPopTimeInt)
        print(" I shall make a note of " + newMob+ ", adventurer. Happy camping!")
        print()
        playsound('sounds/page_turn01.wav')
        import json
        with open('bestiary.txt', 'w') as file:
            file.write(json.dumps(dictionary)) # use `json.loads` to do the reverse
            file.close()
        runMobTimer(newMob, newPopTimeInt)

    else:
        print(" Very well, adventurer. Now begone!")
        print()
        playsound('sounds/voc_yruhere.wav')
        sys.exit()
