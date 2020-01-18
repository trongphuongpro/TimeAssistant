from gtts import gTTS
from io import BytesIO
import pygame
import pygame.mixer as audio


notifications = ["It's time to sleep, sir", "Relax, please", "Good morning, sir"]

months = ['January', 'February', 'March', 'April', 'May', 'June', 
	'July', 'August', 'September', 'October', 'November', 'December']

wdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


audio.init()

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


if __name__ == '__main__':
	pass