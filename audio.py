from gtts import gTTS
from io import BytesIO
import pygame
import pygame.mixer as audio


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


def alarm():
	pass


if __name__ == '__main__':
	pass