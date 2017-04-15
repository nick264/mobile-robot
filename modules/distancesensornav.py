import time
from modules.pantilt import PanTilt
from modules.move import Move

class DistanceSensorNav:
  def __init__():
    self.pt = PanTilt()
    self.move = Move()
    return True
  
  def getDistance(self):
    # sendPing()
    # echo = recordEcho()
    # return distance
  
  def radialDistance(self):
    self.move.moveLeft(0.8)
    now = time.time()
    turnDuration = 15 # seconds
    measureFrequency = 0.1 # seconds
    
    dist = []
    
    while time.time() < now + turnDuration:
      dist << [ time.time(), self.getDistance() ]
      time.sleep(measureFrequency)
    
    self.move.stop()
    
    return dist
  
  def calcDegreeDistance(self):
    