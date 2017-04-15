from picamera import PiCamera
from subprocess import call

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