import cv2

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