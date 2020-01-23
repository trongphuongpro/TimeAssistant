#! /home/ntppro/Work/pet/bin/python

import time
from datetime import date

from interface import LCD1602
#import audio
from webapi import getTasks


today = date.today().timetuple()

display = LCD1602(en=17,rs=22,d4=25,d5=24,d6=23,d7=18)

greeting = "Welcome to time assistant."
notifications = ["It's time to sleep, sir", "Relax, please", "Good morning, sir"]

months = ['January', 'February', 'March', 'April', 'May', 'June', 
	'July', 'August', 'September', 'October', 'November', 'December']

wdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#audio.say(greeting)

while True:
	for task in getTasks().keys():
		#audio.say(n)
		display.clear()
		display.setCursor(1,1)
		display.print(task)
		time.sleep(1)
