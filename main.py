#! /home/ntppro/Work/pet/bin/python

import time
from datetime import date

from interface import LCD1602, Selector
#import audio
from webapi import getTasks, getEvents
import globalvars
#audio.say(greeting)


def up_callback(channel):
	global index

	if index < totalTasks-1:
		globalvars.exitFlag = True
		time.sleep(0.5)
		index += 1
		showInfo()


def down_callback(channel):
	global index

	if index > 0:
		globalvars.exitFlag = True
		time.sleep(0.5)
		index -= 1
		showInfo()


def select_callback(channel):
	print("button [select] pressed")
	print('Edge detected on channel {}'.format(channel))


def showInfo():
	globalvars.exitFlag = False

	task, duration = tasks[index]
	display.clear()
	display.print("{}/{} min".format(duration["actual"], duration["expect"]), pos=(2,3))
	display.print("{}/{}".format(index+1, totalTasks), length=5, scroll=False, pos=(1,14))
	display.print(task, length=8, scroll=True, pos=(1,1))


today = date.today().timetuple()

display = LCD1602(en=17,rs=22,d4=25,d5=24,d6=23,d7=27)

buttons = Selector(buttonUp=14, buttonDown=15, buttonSelect=18, 
					up_callbackfunc=up_callback, 
					down_callbackfunc=down_callback, 
					select_callbackfunc=select_callback)

index = 0

while True:
	global tasks, events, option, totalTasks

	tasks = getTasks()
	events = getEvents()
	totalTasks = len(tasks)
	
	lastTime = time.time()

	while time.time()-lastTime < 60:
		showInfo()
		time.sleep(5)