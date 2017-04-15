from modules.getch import Getch

import time
import pigpio

# moving camera
class PanTilt:
  def __init__(self):
    self.degree1 = 90
    self.degree2 = 90
    self.dontPerformNextMovementBefore = None
    
    # set up pins
    self.servo1_pin = 22
    self.servo2_pin = 23
    self.pwmFrequency = 100

    self.pins = pigpio.pi()
    self.pins.set_PWM_frequency(self.servo1_pin,self.pwmFrequency)
    self.pins.set_PWM_frequency(self.servo2_pin,self.pwmFrequency)
      
  # call this before performing an event to make sure that we've waited an appropriate amount of time
  def waitUntilDoneMoving(self):
    now = time.time()
        
    if self.dontPerformNextMovementBefore:
      if self.dontPerformNextMovementBefore > now:
        time.sleep(self.dontPerformNextMovementBefore - now)
      
  def setMotors(self,panAngle,tiltAngle):
    self.waitUntilDoneMoving()    
    maxAngleChange = max(abs(panAngle - self.degree1),abs(tiltAngle - self.degree2))
    waitTime = maxAngleChange / 180.0 * 1.0 # wait 0.6s for every 180 degrees
    self.dontPerformNextMovementBefore = time.time() + waitTime
    
    self.degree1 = panAngle
    self.degree2 = tiltAngle
    
    duty_cycle1 = ( self.degree1 * 0.01 + 0.6) / ( 1000 / self.pwmFrequency ) # fraction 0-1.0
    duty_cycle2 = ( self.degree2 * 0.01 + 0.6) / ( 1000 / self.pwmFrequency ) # fraction 0-1.0

    self.pins.set_PWM_dutycycle(self.servo1_pin,duty_cycle1 * 255.0)
    self.pins.set_PWM_dutycycle(self.servo2_pin,duty_cycle2 * 255.0)
    
    # self.servo1.ChangeDutyCycle(duty_cycle1)
    # self.servo2.ChangeDutyCycle(duty_cycle2)
  
  def pan(self,leftOrRight):
    if leftOrRight:
      self.setMotors(self.degree1+15,self.degree2)
    else:
      self.setMotors(self.degree1-15,self.degree2)
  
  def tilt(self,upOrDown):
    if upOrDown:
      self.setMotors(self.degree1,self.degree2-15)
    else:
      self.setMotors(self.degree1,self.degree2+15)
    
  def pinCleanup(self):
    self.servo1.stop()
    self.servo2.stop()
    GPIO.cleanup()