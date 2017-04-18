# from modules.getch import Getch

import time
import pigpio

class Tail:
	def __init__(self):
		self.servo_pin = 24
		self.pwmFrequency = 100
		self.pins = pigpio.pi()
		self.pins.set_PWM_frequency(self.servo_pin,self.pwmFrequency)

	def setAngle(self,degree):
		duty_cycle = ( degree * 0.01 + 0.6) / ( 1000 / self.pwmFrequency ) # fraction 0-1.0
		self.pins.set_PWM_dutycycle(self.servo_pin,duty_cycle * 255.0)

	def wag(self,range = 100):
		while True:
			waitTime = range / 180.0 * 0.5
			self.setAngle(90 - range/2.0)
			time.sleep(waitTime)
			self.setAngle(90 + range/2.0)
			time.sleep(waitTime)

Tail().wag(100)
# Tail().setAngle(90)
