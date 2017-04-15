import pigpio

class Move:
  def __init__():
    self.pwmFrequency = 100
    self.pinMap = {
      # motor 1
      'right': {
        'in1': 6,
        'in2': 13,
        'en': 17 # speed
      }
      # motor 2
      'left': {
        'in1': 19,
        'in2': 26,
        'en': 27 # speed
      }
    }
    
    self.pins = pigpio.pi()

    # init pwm frequency
    self.pins.set_PWM_frequency(self.pinMap['left']['en'],self.pwmFrequency)
    self.pins.set_PWM_frequency(self.pinMap['right']['en'],self.pwmFrequency)

    # init motor direction (off by default)
    self.pins.set_DC(self.pinMap['left']['in1'],0.0)
    self.pins.set_DC(self.pinMap['left']['in2'],0.0)
    self.pins.set_DC(self.pinMap['right']['in1'],0.0)
    self.pins.set_DC(self.pinMap['right']['in2'],0.0)


  # set motor speed.  0 <= speed <= 1.0
  def setSpeed(self,motor,speed):
    self.pins.set_PWM_dutycycle(self.pinMap[motor]['en'],speed * 255.0)
  
  def setSpeedAll(self,speed):
    self.setSpeed('left',speed)
    self.setSpeed('right',speed)

  def setMotorDirection(self,motor,forwardOrBack):
    if forwardOrBack:
      in1 = False
      in2 = True
    else:
      in1 = True
      in2 = False
    
    self.pins.set_DC(self,pinMap[motor]['in1'],in1)
    self.pins.set_DC(self,pinMap[motor]['in2'],in2)
    
  def moveFwd(self,speed):
    self.setMotorDirection('left',True)
    self.setMotorDirection('right',True)
    self.setSpeedAll(speed)
  
  def moveBwd(self,speed):
    self.setMotorDirection('left',False)
    self.setMotorDirection('right',False)
    self.setSpeedAll(speed)

  def moveLeft(self,speed):
    self.setMotorDirection('left',False)
    self.setMotorDirection('right',True)
    self.setSpeedAll(speed)

  def moveRight(self,speed):
    self.setMotorDirection('left',True)
    self.setMotorDirection('right',False)
    self.setSpeedAll(speed)

  def stop(self):
    self.setSpeedAll(0.0)

  # make this asynchronous
  def runCommand(self,command,duration,speed=0.8):
    self.send(command,speed)
    time.sleep(duration)
    self.stop()