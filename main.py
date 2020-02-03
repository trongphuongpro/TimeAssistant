#! /home/ntppro/Work/pet/bin/python

import time
from datetime import date

from interface import LCD1602, Selector
#import audio
from webapi import getTasks, getEvents
import globalvars
#audio.say(greeting)


def up_callback(channel):
	global index, mode
	mode = 0

	if index < totalTasks-1:
		globalvars.exitFlag = True
		index += 1


def down_callback(channel):
	global index, mode
	mode = 0

	if index > 0:
		globalvars.exitFlag = True
		index -= 1


def select_callback(channel):
	global mode
	mode = 1

	globalvars.exitFlag = True


def showInfo():
	print("showInfo")
	globalvars.exitFlag = False

	task, duration = tasks[index]
	totalTasks = len(tasks)
	display.clear()

	display.print("{}/{} min".format(duration["actual"], duration["expect"]), pos=(2,3))
	display.print("{}/{}".format(index+1, totalTasks), pos=(1,14))
	display.print(task, length=8, scroll=True, pos=(1,1))


def showCoundown():
	print("showCoundown")
	globalvars.exitFlag = False

	task, duration = tasks[index]
	display.clear()

	display.print("{}/{} min".format(duration["actual"], duration["expect"]), pos=(2,3))
	display.print(task, length=16, scroll=True, pos=(1,1))


def countdown():
	tasks[index][1]["actual"] += 1



def delay(duration):
	lastTime = time.time()

	while time.time() - lastTime < duration:
		if globalvars.exitFlag == True:
			break


today = date.today().timetuple()

display = LCD1602(en=17,rs=22,d4=25,d5=24,d6=23,d7=27)

buttons = Selector(buttonUp=14, buttonDown=15, buttonSelect=18, 
					up_callbackfunc=up_callback, 
					down_callbackfunc=down_callback, 
					select_callbackfunc=select_callback)

index = 0
mode = 0

while True:
	global tasks, events

	tasks = getTasks()
	events = getEvents()
	
	lastTime = time.time()

	if mode == 0:
		while time.time() - lastTime < 60:
			if mode == 1:
				break

			showInfo()
			delay(30)

	elif mode == 1:
		showCoundown()
		countdown()
		delay(60)