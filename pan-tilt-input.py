# camera lib
from picamera import PiCamera

# gpio lib
import RPi.GPIO as GPIO

# other libs
import time
import sys,tty,termios
from subprocess import call


print("clearing media...")
call(["rm", "-r", "tmp-media"])
call(["mkdir", "tmp-media"])

# set up camera
camera = PiCamera()
camera.rotation = 180

# set up pins
servo1_pin = 22
servo2_pin = 23

GPIO.setmode(GPIO.BCM)

GPIO.setup(servo1_pin,GPIO.OUT)
GPIO.setup(servo2_pin,GPIO.OUT)

servo1 = GPIO.PWM(servo1_pin, 50)
servo2 = GPIO.PWM(servo2_pin, 50)
servo1.start(7.5)
servo2.start(7.5)

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
    return 'space'
  elif k=='q':
    return 'quit'
  elif k == 'p':
    return 'picture'
  elif k == 'o':
    return 'record'
  elif k == 'i':
    return 'stop recording'    
  else:
    print "unhandled key: "
    print k
    print "\n"
    return k
    terminateProgram()


# duty_cycle = 2.5 + degree / 180 * (12.5 - 2.5)

degree1 = 90
degree2 = 90

i_p = 1
i_v = 1

def terminateProgram():
  print('finishing up')
  servo1.stop()
  servo2.stop()
  GPIO.cleanup()
  quit()

try:
  while True:
    duty_cycle1 = 2.5 + degree1 / 180.0 * (12.5 - 2.5)
    duty_cycle2 = 2.5 + degree2 / 180.0 * (12.5 - 2.5)
    
    servo1.ChangeDutyCycle(duty_cycle1)
    servo2.ChangeDutyCycle(duty_cycle2)

    key = get()
    
    print key
    
    if key == 'up':
      degree2 -= 15
    elif key == 'down':
      degree2 += 15
    elif key == 'left':
      degree1 += 15
    elif key == 'right':
      degree1 -= 15
    elif key == 'picture':
      camera.capture('tmp-media/image%i.jpg' % i_p)
      i_p += 1
    elif key == 'record':
      camera.start_recording('tmp-media/video%i.h264' % i_v)
      i_v += 1
    elif key == 'stop recording':
      camera.stop_recording()
    elif key == 'quit':
      terminateProgram()
      
except KeyboardInterrupt:
  terminateProgram()