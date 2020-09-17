import RPi.GPIO as GPIO

def setup():
	GPIO.setmode(GPIO.BCM)

def turnOn(pin):
	while True:
		try:
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, GPIO.HIGH)
			break
		except RuntimeError:
			setup()
def turnOff(pin):
	GPIO.output(pin, GPIO.LOW)
def done():
	GPIO.cleanup()
