#! /home/ntppro/Work/pet/bin/python

import time
from datetime import date

import audio
import interface
import webapi


today = date.today().timetuple()

greeting = "Welcome to time assistant."
notifications = ["It's time to sleep, sir", "Relax, please", "Good morning, sir"]

months = ['January', 'February', 'March', 'April', 'May', 'June', 
	'July', 'August', 'September', 'October', 'November', 'December']

wdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

audio.say(greeting)

while True:
	for n in notifications:
		audio.say(n)
		time.sleep(1)
