import cv2

# camera lib
from picamera import PiCamera

# gpio lib
import RPi.GPIO as GPIO

# other libs
import time
import sys,tty,termios
from subprocess import call


class DetectFace:
  cascPath = './haarcascade_frontalface_default.xml'
  faceCascade = cv2.CascadeClassifier(cascPath)
  
  def detect(self,imagePath):
    # Read the image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = self.faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
    )
    
    print("Found {0} faces!".format(len(faces)))
    print(faces)
    return len(faces) > 0
    

class CameraControl:
  def __init__():
    # set up camera
    self.camera = PiCamera()
    self.camera.rotation = 180
    self.iPic = 1
    self.iVid = 1
  
  def snap():
    filename = 'tmp-media/image%i.jpg' % self.iPic
    self.camera.capture(filename)
    self.iPic += 1
    return filename
    
  def startRecording():
    self.camera.start_recording('tmp-media/video%i.h264' % iVid)
    self.iVid += 1
    
  def stopRecording():
    self.camera.stop_recording

class PanTilt:
  def __init__():
    self.degree1 = 90
    self.degree2 = 90
  
  def initServos:
    # set up pins
    servo1_pin = 22
    servo2_pin = 23

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(servo1_pin,GPIO.OUT)
    GPIO.setup(servo2_pin,GPIO.OUT)

    self.servo1 = GPIO.PWM(servo1_pin, 50)
    self.servo2 = GPIO.PWM(servo2_pin, 50)
    self.servo1.start(7.5)
    self.servo2.start(7.5)

  def setMotors():
    duty_cycle1 = 2.5 + self.degree1 / 180.0 * (12.5 - 2.5)
    duty_cycle2 = 2.5 + self.degree2 / 180.0 * (12.5 - 2.5)
    
    self.servo1.ChangeDutyCycle(duty_cycle1)
    self.servo2.ChangeDutyCycle(duty_cycle2)

  def pan(leftOrRight):
    if leftOrRight:
      self.degree1 += 15
    else:
      self.degree1 -= 15
    setMotors()
    
  def tilt(upOrDown)
    if upOrDown:
      self.degree2 -= 15
    else:
      self.degree2 += 15
    setMotors()
  
  def setAngles(panAngle,tiltAngle)
    self.degree1 = panAngle
    self.degree2 = tiltAngle
    setMotors()
    
  def pinCleanup():
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()

  
cc = CameraControl()
df = DetectFace()
pt = PanTilt()

# df.detect('../pics/face.jpeg')
df.detect(cc.snap())
