import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# motor one
enA = 17;
in1 = 6;
in2 = 13;
# motor two
enB = 27;
in3 = 19;
in4 = 26;

GPIO.setup(enA,GPIO.OUT)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)

GPIO.setup(enB,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)

vA = GPIO.PWM(enA, 300)
vB = GPIO.PWM(enB, 300)
vA.start(0.0)
vB.start(0.0)

def setMotorDirection(lOrR,forwardOrBackward):
  if(lOrR):
    channel1 = in3
    channel2 = in4
  else:
    channel1 = in1
    channel2 = in2
  
  if forwardOrBackward:
    channel1Out = False
    channel2Out = True
  else:
    channel1Out = True
    channel2Out = False
    
  GPIO.output(channel1,channel1Out)
  GPIO.output(channel2,channel2Out)


while True:
  try:
    # GPIO.output(in1,False)
    # GPIO.output(in2,True)
    vA.ChangeDutyCycle(0.0)
    # GPIO.output(in3,False)
    # GPIO.output(in4,True)
    vB.ChangeDutyCycle(0.0)

    command = raw_input("Enter command\n")
    commandSplit = command.split(" ")
    
    direction = commandSplit[0]
    speed     = float(commandSplit[1])
    duration  = float(commandSplit[2])
        
    if direction == 'f':
      setMotorDirection(True,True)
      setMotorDirection(False,True)
    elif direction == 'b':
      setMotorDirection(True,False)
      setMotorDirection(False,False)
    elif direction == 'r':
      setMotorDirection(True,True)
      setMotorDirection(False,False)
    elif direction == 'l':
      setMotorDirection(False,True)
      setMotorDirection(True,False)
    else:
      print "Don't understand command"
      print direction
      print "\n"
      continue

    vA.ChangeDutyCycle(speed)
    vB.ChangeDutyCycle(speed)
    time.sleep(duration)
  except(KeyboardInterrupt):
    print('finishing up')
    GPIO.output(enA,False)
    GPIO.output(in1,False)
    GPIO.output(in2,False)
    GPIO.output(enB,False)
    GPIO.output(in3,False)
    GPIO.output(in4,False)
    GPIO.cleanup()
    quit()
  

# print('starting')

# while True:
#   try:
#     GPIO.output(in1,True)
#     GPIO.output(in2,False)

#     vA.ChangeDutyCycle(25.0)
#     time.sleep(2)
#     vA.ChangeDutyCycle(50.0)
#     time.sleep(2)
#     vA.ChangeDutyCycle(75.0)
#     time.sleep(2)
#     vA.ChangeDutyCycle(100.0)
#     time.sleep(2)
#     vA.ChangeDutyCycle(75.0)
#     time.sleep(2)
#     vA.ChangeDutyCycle(50.0)
#     time.sleep(2)
#     vA.ChangeDutyCycle(25.0)
#     time.sleep(2)
#     vA.ChangeDutyCycle(0.0)
#     time.sleep(2)

    
#     # GPIO.output(in1,True)
#     # GPIO.output(in2,False)
#     # GPIO.output(enA,True)
#     # time.sleep(3)
#     # GPIO.output(in1,False)
#     # GPIO.output(in2,True)
#     # GPIO.output(enA,True)
#     # time.sleep(3)
#   except(KeyboardInterrupt):
#     print('finishing up')
#     GPIO.output(enA,False)
#     GPIO.output(in1,False)
#     GPIO.output(in2,False)
#     GPIO.output(enB,False)
#     GPIO.output(in3,False)
#     GPIO.output(in4,False)
#     GPIO.cleanup()
#     quit()
