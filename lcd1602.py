#! /home/ntppro/Work/pet/bin/python

import RPi.GPIO as GPIO
import time


class LCD1602:
	def __init__(self, *, en, rs, d4, d5, d6, d7):
		self.en = en
		self.rs = rs

		self.d5 = d5
		self.dataPins = [d4,d5,d6,d7]

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		GPIO.setup(self.en, GPIO.OUT)
		GPIO.setup(self.rs, GPIO.OUT)
		GPIO.output(self.en, False)
		GPIO.output(self.rs, False)

		for pin in self.dataPins:
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, False)

		time.sleep(0.5)

		self.__awake()
		self.__functionSet()
		self.__displayControl()
		self.clear()
		self.goHome()
		self.__entryModeSet()


	def __awake(self):
		for i in range(5):
			self.__writeData(0x00)


	def __functionSet(self):
		# 4-bit mode
		GPIO.output(self.d5, True)
		GPIO.output(self.en, True)
		GPIO.output(self.en, False)
		GPIO.output(self.d5, False)

		self.sendInstruction(0x28)


	def __displayControl(self):
		# Display control: cursor, no blink
		self.sendInstruction(0x0C)


	def __entryModeSet(self):
		# Entry set mode: Increase, no shift
		self.sendInstruction(0x06)


	def goHome(self):
		self.sendInstruction(0x02)


	def setCursor(self, row, col):
		address = (col-1) + (row-1) * 64
		self.sendInstruction(address | 0x80)


	def clear(self):
		self.sendInstruction(0x01)


	def putchar(self, char):
		self.sendData(ord(char))


	def print(self, text):
		for c in text:
			self.putchar(c)


	def scrollLeft(self):
		self.sendInstruction(0x18)


	def scrollRight(self):
		self.sendInstruction(0x1C)


	def __writeData(self, data):
		
		for i in range(4,8):
			GPIO.output(self.dataPins[i-4], (data >> i) & 1 == 1)


		GPIO.output(self.en, True)
		GPIO.output(self.en, False)

		for i in range(0,4):
			GPIO.output(self.dataPins[i], (data >> i) & 1 == 1)

		GPIO.output(self.en, True)
		GPIO.output(self.en, False)


	# def __waitBusy(self):
	# 	GPIO.output(self.rs, False)
	# 	GPIO.output(self.rw, True)

	# 	GPIO.setup(self.dataPins[3], GPIO.IN)

	# 	while True:
	# 		GPIO.output(self.en, True)
	# 		GPIO.output(self.en, False)

	# 		if (GPIO.input(self.dataPins[3]) == False):
	# 			break

	# 	GPIO.setup(self.dataPins[3], GPIO.OUT)
	# 	GPIO.output(self.dataPins[3], False)
	# 	GPIO.output(self.rs, False)
	# 	GPIO.output(self.rw, False)



	def sendInstruction(self, data):
		GPIO.output(self.rs, False)
		self.__writeData(data)
		
		#self.__waitBusy()
		time.sleep(0.01)


	def sendData(self, data):
		GPIO.output(self.rs, True)
		self.__writeData(data)

		#self.__waitBusy()
		time.sleep(0.01)


if __name__ == '__main__':
	display = LCD1602(en=17,rs=22,d4=25,d5=24,d6=23,d7=18)

	while True:
		display.setCursor(1,1)
		display.print("[timeassistant]")
		display.setCursor(2,1)
		display.print("Good morning, sir")
		time.sleep(3)
		display.clear()

		display.setCursor(1,1)
		display.print("Welcome")
		display.setCursor(2,5)
		display.print("Goodbye")
		time.sleep(3)
		display.clear()