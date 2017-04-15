# import sys,tty,termios
import time
import RPi.GPIO as GPIO

servo1_pin = 22
servo2_pin = 23

GPIO.setmode(GPIO.BCM)

GPIO.setup(servo1_pin,GPIO.OUT)
GPIO.setup(servo2_pin,GPIO.OUT)

servo1 = GPIO.PWM(servo1_pin, 50)
servo2 = GPIO.PWM(servo2_pin, 50)
servo1.start(7.5)
servo2.start(7.5)

# duty_cycle = 2.5 + degree / 180 * (12.5 - 2.5)


try:
  while True:
    servo2.ChangeDutyCycle(7.5) # neutral
    time.sleep(1)
    servo2.ChangeDutyCycle(9.5) # 180deg
    time.sleep(1)
    servo2.ChangeDutyCycle(5.5) # 0deg
    time.sleep(1)
except KeyboardInterrupt:
  servo1.stop()
  servo2.stop()
  GPIO.cleanup()