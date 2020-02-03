#! /home/ntppro/Work/pet/bin/python

import time
from datetime import date

from interface import LCD1602, Selector
#import audio
from webapi import getTasks, getEvents
import globalvars
#audio.say(greeting)


def up_callback(channel):
	if globalvars.index < totalTasks-1:
		globalvars.exitFlag = True
		globalvars.index += 1


def down_callback(channel):
	if globalvars.index > 0:
		globalvars.exitFlag = True
		globalvars.index -= 1


def select_callback(channel):
	print("button [select] pressed")
	print('Edge detected on channel {}'.format(channel))


def showInfo():
	globalvars.exitFlag = False

	task, duration = tasks[globalvars.index]
	display.clear()

	display.print("{}/{} min".format(duration["actual"], duration["expect"]), pos=(2,3))
	display.print("{}/{}".format(globalvars.index+1, totalTasks), pos=(1,14))

	display.print(task, length=8, scroll=True, pos=(1,1))


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


while True:
	global tasks, events, option, totalTasks

	tasks = getTasks()
	events = getEvents()
	totalTasks = len(tasks)
	
	lastTime = time.time()

	while time.time()-lastTime < 60:
		showInfo()
		delay(5)