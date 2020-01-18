#! /home/ntppro/Work/pet/bin/python

import time
from datetime import date

import audio
import interface
import webapi


today = date.today().timetuple()

greeting = "Welcome to time assistant. Today is {}, {}, {}, {}".format(wdays[today.tm_wday], today.tm_mday,
							months[today.tm_mon-1], today.tm_year)

say(greeting)

while True:
	for n in notifications:
		led.value = True
		say(n)
		led.value = False
		time.sleep(1)
