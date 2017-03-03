import time
import RPi.GPIO as GPIO
import sys,tty,termios

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

class _Getch:
  def __call__(self):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
    finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def get():
  inkey = _Getch()
  while(1):
    k=inkey()
    if k!='':break
  if k=='w': # k=='\x1b[A':
    return "up"
  elif k=='s': # k=='\x1b[B':
    return "down"
  elif k=='d': # k=='\x1b[C':
    return "right"
  elif k=='a': # k=='\x1b[D':
    return "left"
  elif k==' ':
    return 'stop'
  elif k=='p':
    return 'upspeed'
  elif k=='o':
    return 'downspeed'
  elif k == 'q':
    return 'quit'
  else:
    print "unhandled key: "
    print k
    print "\n"
    return k


def terminateProgram():
  print('finishing up')
  GPIO.output(enA,False)
  GPIO.output(in1,False)
  GPIO.output(in2,False)
  GPIO.output(enB,False)
  GPIO.output(in3,False)
  GPIO.output(in4,False)
  GPIO.cleanup()
  quit()


curKey = None

speed = 80

while True:
  try:
    key = get()
    # if curKey == key:
    #   key = 'cancel'
    
    # curKey = key
    
    print "Processing command "
    print key
    print "\n"
    
    brake = False
    
    if key == 'up':
      setMotorDirection(True,True)
      setMotorDirection(False,True)
    elif key == 'down':
      setMotorDirection(True,False)
      setMotorDirection(False,False)
    elif key == 'right':
      setMotorDirection(True,True)
      setMotorDirection(False,False)
    elif key == 'left':
      setMotorDirection(False,True)
      setMotorDirection(True,False)
    elif key == 'stop':
      brake = True
    elif key == 'upspeed':
      speed += 5
      brake = True
    elif key == 'downspeed':
      speed -= 5
      brake = True
    elif key == 'quit':
      terminateProgram()
    else:
      print "Don't understand command"
      print key
      print "\n"
      continue
    
    print "Speed = ", speed

    if brake == True:
      vA.ChangeDutyCycle(0)
      vB.ChangeDutyCycle(0)
    else:
      vA.ChangeDutyCycle(speed)
      vB.ChangeDutyCycle(speed)
      
  except(KeyboardInterrupt):
    terminateProgram()