# Import modules
import sys
import ast
import sched
import time
from datetime import datetime
from playsound import playsound


# Fun title text and welcome sound
print('')
print(' Welcome to CampTime!')
print()
playsound('sounds/voc_welcome.wav')

# Scheduler initialization
s = sched.scheduler(time.time, time.sleep)
t = 0

 # Open bestiary text file and read it
file = open("bestiary.txt", "r")
contents = file.read()
dictionary = ast.literal_eval(contents)
file.close()

# Prompt user for mob they are camping
def monsterInput():
    mobName = input(" Name of mob camping: ")
    print()

    # Check if input is in bestiary already
    if mobName in dictionary.keys():
        print(" Ah, yes... " + mobName)
        popTime = dictionary.get(mobName)
        print()
        playsound('sounds/page_turn01.wav')
        modePrompt(mobName, popTime)

    # If input is not in bestiary, ask if user wants to add it.
    else:
        addMob(mobName)

# Define functions

def modePrompt(mobName, popTime):
    prompt = (" Do you want to run the spawn timer automatically? ")
    mode = input(prompt + "(y/n): ").lower().strip()
    while not(mode == "y" or mode == "yes" or
                  mode == "n" or mode == "no"):
            print("Input yes or no")            
            mode = input(prompt + "(y/n):").lower().strip()
            print()
    if mode == "n" or "no":
        runMobTimer(mobName, popTime, mode)
    elif mode =="y" or "yes":
        runMobTimer(mobName, popTime, mode)

# Fire up the mob timer

def runMobTimer(mobName, popTime, mode):
    popMins = str(round(popTime/60, 2))
    if mode == "y":
        modeText = " Automatic"
    elif mode == "n":
        modeText= " Manual"
    playsound('sounds/clock.wav', block=False)
    print()
    print(modeText + " respawn timer for " + mobName + " is set to " +
        popMins + " minutes. Happy camping!")
    print()

    s.enter(popTime, 1, do_something, (s, popTime, mobName, mode))
    for remaining in range(popTime, -1, -1):
        sys.stdout.write("\r")
        sys.stdout.write(
            "{:2d} ".format(remaining) + "seconds remaining...")
        sys.stdout.flush()
        time.sleep(1)
    s.run()

# Time Loop
def countdown(popTime):        
    for remaining in range(popTime, -1, -1):
        sys.stdout.write("\r")
        sys.stdout.write(
            "{:2d} ".format(remaining) + "seconds remaining...")
        sys.stdout.flush()
        time.sleep(1)

# Grab current time
def getTime():
    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")
    return currentTime

def printPop(mobName):
    currentTime = getTime()
    print(" Pop! " + mobName + " should be up as of " + currentTime)

def printTimerStarted():
    currentTime = getTime()
    print(" Manual" + " respawn timer started at " + currentTime)

# Function that runs at beginning of camp timer
def do_something(sc, popTime, mobName, mode):
    printPop(mobName)
    playsound('sounds/icefreti_atk.wav')
    if mode == "y":
        playsound('sounds/clock.wav', block=False)
        s.enter(popTime, 1, do_something, (sc, popTime, mobName, "y"))
        countdown(popTime)
    elif mode== "n":
        print()
        input(" Press enter to reset camp timer.")
        printTimerStarted()
        playsound('sounds/clock.wav', block=False)
        s.enter(popTime, 1, do_something, (sc, popTime, mobName, "n"))
        countdown(popTime)
        


def addMob(newMob):
    question = (" I could not find " + newMob + " in the bestiary. Would you like to add it? ")
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
            " How many seconds does it take for " + newMob + " to spawn? ")
        print()
        newPopTimeInt = int(newPopTime)
        dictionary[newMob] = int(newPopTimeInt)
        print(" I shall make a note of " +
              newMob + ", adventurer.")
        print()
        playsound('sounds/page_turn01.wav')
        import json
        with open('bestiary.txt', 'w') as file:
            # use `json.loads` to do the reverse
            file.write(json.dumps(dictionary))
            file.close()
        modePrompt(newMob, newPopTimeInt)
    else:
        print(" Very well, adventurer. Now begone!")
        print()
        playsound('sounds/voc_yruhere.wav')
        sys.exit()

# End of function defs

# Kick things off
monsterInput()