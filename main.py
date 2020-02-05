#! /home/ntppro/Work/pet/bin/python

import time
from datetime import date
import pickle
from enum import IntEnum
from interface import LCD1602, Selector
from webapi import getTasks, getEvents
import globalvars
#import audio
#audio.say(greeting)


class Mode(IntEnum):
	normal = 0
	tracking = 1


def up_callback(channel):
	if not isTracking:
		global index, mode
		mode = Mode.normal

		totalTasks = len(taskRecord)

		if index < totalTasks-1:
			globalvars.exitFlag = True
			index += 1


def down_callback(channel):
	if not isTracking:
		global index, mode
		mode = Mode.normal

		if index > 0:
			globalvars.exitFlag = True
			index -= 1


def select_callback(channel):
	global mode, isTracking, currentTask
	mode = Mode.tracking

	globalvars.exitFlag = True
	isTracking = not isTracking
	currentTask = list(taskRecord.keys())[index]


def showInfo():
	global index

	globalvars.exitFlag = False

	totalTasks = len(taskRecord)

	if totalTasks > 0:
		if index >= totalTasks:
			index = totalTasks-1

		taskID, info = list(taskRecord.items())[index]

		display.clear()
		display.print("{}/{} min".format(info["actual"], info["expect"]), pos=(2,3))
		display.print("{}/{}".format(index+1, totalTasks), pos=(1,14))
		display.print(info["task"], length=8, scroll=True, pos=(1,1))

	else:
		display.clear()
		display.print("No task!")


def showTrackingInfo():
	global currentTask, mode

	globalvars.exitFlag = False

	display.clear()

	if isTracking:
		display.print("tracking", pos=(2,9))
	else:
		display.print("paused", pos=(2,11))

	display.print("{}/{}".format(taskRecord[currentTask]["actual"], taskRecord[currentTask]["expect"]), pos=(2,1))
	display.print(taskRecord[currentTask]["task"], length=16, scroll=True, pos=(1,1))


def track():
	global taskRecord

	if isTracking and currentTask in taskRecord:
		taskRecord[currentTask]["actual"] += 1


def delay(duration):
	lastTime = time.time()

	while time.time() - lastTime < duration:
		if globalvars.exitFlag == True:
			break


def updateRecord():
	global taskRecord, mode, isTracking

	tasks = getTasks()

	# if task record is empty
	if len(taskRecord) == 0:
		for taskID, info in tasks.items():
			taskRecord[taskID] = {"task": info["task"], "actual": 0, "expect": info["expect"]}

	else:
		# update existed and new tasks
		for taskID, info in tasks.items():
			# with existed tasks
			if taskID in taskRecord:
				taskRecord[taskID]["expect"] = info["expect"]

			# with new tasks
			else:
				taskRecord[taskID] = {"task": info["task"], "actual": 0, "expect": info["expect"]}

		# delete tasks that were removed from server
		oldTasks = []
		for taskID in taskRecord:
			if taskID not in tasks:
				oldTasks.append(taskID)

		for task in oldTasks:
			del taskRecord[task]

		# if current task was removed from record
		if currentTask not in taskRecord:
			mode = Mode.normal
			globalvars.exitFlag = True
			isTracking = False


	with open("record.txt", "wb") as f:
		pickle.dump(taskRecord, f)


def execute():
	updateRecord()

	lastTime = time.time()

	while time.time() - lastTime < 10:
		if mode is Mode.normal:
			showInfo()
			delay(5)

		elif mode is Mode.tracking:
			showTrackingInfo()
			track()
			delay(5)


today = date.today().timetuple()

display = LCD1602(en=17,rs=22,d4=25,d5=24,d6=23,d7=27)

buttons = Selector(buttonUp=14, buttonDown=15, buttonSelect=18, 
					up_callbackfunc=up_callback, 
					down_callbackfunc=down_callback, 
					select_callbackfunc=select_callback)

index = 0
mode = Mode.normal
currentTask = 0
taskRecord = {}
isTracking = False

try:
	with open("record.txt", "rb") as f:
		taskRecord = pickle.load(f)
except Exception as e:
	print(e)

while True:
	execute()