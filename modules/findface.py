from modules.cameracontrol import CameraControl
from modules.detectface import DetectFace
from modules.pantilt import PanTilt

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
    
# usage:
# FindFace().search()