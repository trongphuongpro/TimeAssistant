#! /home/ntppro/Work/pet/bin/python

import time
from datetime import date
import board
import digitalio
from gtts import gTTS
from io import BytesIO
import pygame
import pygame.mixer as audio
 
led = digitalio.DigitalInOut(board.D2)
led.direction = digitalio.Direction.OUTPUT
led.value = False

audio.init()

audiofile = "demo.mp3"

notifications = ["It's time to sleep, sir", "Relax, please", "Good morning, sir"]

months = ['January', 'February', 'March', 'April', 'May', 'June', 
	'July', 'August', 'September', 'October', 'November', 'December']

wdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def say(text, language='en'):
	fp = BytesIO()

	tts = gTTS(text, lang=language)
	tts.write_to_fp(fp)

	fp.seek(0)
	audio.music.load(fp)
	audio.music.play()
	while audio.music.get_busy():
		pygame.time.Clock().tick(10)

	fp.close()
	
today = date.today().timetuple()

greeting = "Welcome to time assistant. Today is {}, {}, {}, {}".format(wdays[today.tm_wday], today.tm_mday,
							months[today.tm_mon-1], today.tm_year)

say(greeting)

with open('speech.txt', 'r', encoding='utf-8') as f:
	say(f.read(), 'vi')

while True:
	for n in notifications:
		led.value = True
		say(n)
		led.value = False
		time.sleep(1)
