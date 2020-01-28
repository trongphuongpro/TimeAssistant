#! /home/ntppro/Work/pet/bin/python

import time
from datetime import date

from interface import LCD1602
#import audio
from webapi import getTasks, getEvents


today = date.today().timetuple()

display = LCD1602(en=17,rs=22,d4=25,d5=24,d6=23,d7=18)

greeting = "Welcome to time assistant."
notifications = ["It's time to sleep, sir", "Relax, please", "Good morning, sir"]

months = ['January', 'February', 'March', 'April', 'May', 'June', 
	'July', 'August', 'September', 'October', 'November', 'December']

wdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#audio.say(greeting)

while True:
	tasks = getTasks()

	for task, duration in tasks.items():
		#audio.say(n)
		display.clear()
		display.print("{}/{} min".format(duration["actual"], duration["expect"]), pos=(2,3))
		display.print(task, length=8, scroll=True, pos=(1,1))
		time.sleep(1)

	events = getEvents()

	for event, moment in events.items():
		#audio.say(n)
		display.clear()
		display.print("{}".format(moment["expect"])[0:-3], pos=(2,3))
		display.print(event, length=8, scroll=True, pos=(1,1))
		time.sleep(1)

	time.sleep(10)
