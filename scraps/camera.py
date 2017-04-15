from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.rotation = 180

sleep(3)
camera.capture('image.jpg')

# sleep(2)
# camera.start_recording('video.h264')
# sleep(10)
# camera.stop_recording()
