import board
import digitalio


led = digitalio.DigitalInOut(board.D2)
led.direction = digitalio.Direction.OUTPUT
led.value = False


if __name__ == '__main__':
	pass
