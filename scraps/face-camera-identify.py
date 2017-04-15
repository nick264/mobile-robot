import cv2

# camera lib
from picamera import PiCamera

# other libs
import time
import sys,tty,termios
from subprocess import call

# gpio lib
import pigpio
# call('sudo pigpiod')

# opencv face detection
class DetectFace:
  def __init__(self):
    self.cascPath = './haarcascade_frontalface_default.xml'
    self.faceCascade = cv2.CascadeClassifier(self.cascPath)
  
  def detect(self,imagePath):
    # Read the image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = self.faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
    )
    
    print("Found {0} faces!".format(len(faces)))
    print(faces)
    return {
      'dimensions': image.shape,
      'faces': faces
    }
    
# camera picture-taking / recording
class CameraControl:
  def __init__(self):
    # clear media directory
    call(["rm", "-r", "tmp-media"])
    call(["mkdir", "tmp-media"])

    # set up camera
    self.camera = PiCamera()
    self.camera.rotation = 180
    self.iPic = 1
    self.iVid = 1
  
  def snap(self):
    filename = 'tmp-media/image%i.jpg' % self.iPic
    self.camera.capture(filename)
    self.iPic += 1
    return filename
    
  def startRecording(self):
    self.camera.start_recording('tmp-media/video%i.h264' % iVid)
    self.iVid += 1
    
  def stopRecording(self):
    self.camera.stop_recording

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

# find face
class FindFace:
  def __init__(self):
    self.cc = CameraControl()
    self.df = DetectFace()
    self.pt = PanTilt()
  
  def getFaceData(self):
    filename = self.cc.snap()
    return self.df.detect(filename)
  
  def checkForFace(self):
    self.pt.waitUntilDoneMoving()
    return len(self.getFaceData()['faces']) > 0
  
  def panSearch(self,tiltAngle):
    print("pansearch for tiltangle", tiltAngle)
    self.pt.setMotors(90,tiltAngle)
    if self.checkForFace():
      return True 
    self.pt.setMotors(90 + 15,tiltAngle)
    if self.checkForFace():
      return True 
    self.pt.setMotors(90 - 15,tiltAngle)
    if self.checkForFace():
      return True 
    self.pt.setMotors(90 + 2 * 15,tiltAngle)
    if self.checkForFace():
      return True 
    self.pt.setMotors(90 - 2 * 15,tiltAngle)
    if self.checkForFace():
      return True     
    return False
  
  def search(self):
    if self.panSearch(75) or self.panSearch(60) or self.panSearch(90):
      self.centerFace()
    else:
      return False
  
  def centerFace(self):
    for i in [1,2,3]:
      print("moving toward face #%s..." % i)
      self.moveTowardFace()
      
  
  def moveTowardFace(self):
    faceData = self.getFaceData()
    if len(faceData['faces']) == 0:
      print("No face detected!")
    
    centers = []
    for (x, y, w, h) in faceData['faces']:
      # face centers
      centers.append([x + w/2.0,y+h/2.0])
    
    # compute center of gravity
    centerOfGravityPix = [
      sum(map(lambda elem: elem[0],centers)) / len(centers),
      sum(map(lambda elem: elem[1],centers)) / len(centers)
    ]
    
    centerOfGravityPerc = [
      centerOfGravityPix[0] / float(faceData['dimensions'][1]),
      centerOfGravityPix[1] / float(faceData['dimensions'][0])
    ]
    
    print("Image dimensions: ", faceData['dimensions'])
    print("Face count: ", len(faceData['faces']))
    print("Center of gravity pix: ", centerOfGravityPix)
    print("Center of gravity perc: ", centerOfGravityPerc)
    
    degrees_per_frame = 30 # assume about 30 degrees in camera frame
    moveDegreesX = -1 * ( centerOfGravityPerc[0] - 0.5 ) *  degrees_per_frame
    moveDegreesY = ( centerOfGravityPerc[1] - 0.5 ) *  degrees_per_frame
    
    self.pt.setMotors(self.pt.degree1 + moveDegreesX, self.pt.degree2 + moveDegreesY)
    

FindFace().search()

# print(FindFace().getFaceData())
# print(FindFace().checkForFace())

# pt = PanTilt()
# pt.setMotors(50,70)
  
# time.sleep(2.0)
# pt.setMotors(90,90)
# pt.setMotors(90,140)
# pt.setMotors(90,90)
# pt.setMotors(90,50)
# pt.setMotors(90,90)
# time.sleep(2.0)

# cc = CameraControl()
# df = DetectFace()
# pt = PanTilt()

# # df.detect('../pics/face.jpeg')
# df.detect(cc.snap())

# who am i / who is that?
# [OPT] 30 degrees left, 10 degrees up
# => start checking for faces
# => search for face.  can't find it.
# check 30 degrees to the left
# => move.  find / can't find it
# => i don't know you.  who are you?
# 