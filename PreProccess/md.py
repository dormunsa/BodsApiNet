import cv2
import numpy as np
from PIL import Image
import os.path
from imutils import paths
import requests

#globals
Image.MAX_IMAGE_PIXELS = 10000000000
i = 0
KNOWN_WIDTH = 9.05
KNOWN_DISTANCE = 24.41
focalLength = 3000

def crop_image(img, xy, scale_factor):

   global i

   if ( i % 3 == 0 ):     

      w, h = img.size
      
      img = img.crop((xy[0] - w / scale_factor, xy[1] - h / scale_factor, xy[0] + w / scale_factor, xy[1] + h / scale_factor))

      cropped_img = img.resize((w, h), Image.LANCZOS)

      cropped_img.save('output/newzoom' + str(i / 3) + '.JPEG', quality=95)
      content_type = 'image/jpeg'
      headers = {'content-type': content_type}

      img = cv2.imread('output/newzoom' + str(i / 3) + '.JPEG')
      # encode image as jpeg
      _, img_encoded = cv2.imencode('.jpg', img)
      # send http request with image and receive response
      response = requests.post("http://localhost:5000/pic", data=img_encoded.tostring(), headers=headers)

      print("api response: ")
      print(response.content)


   i = i + 1

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth

def getVideo2(videoName):
   cap = cv2.VideoCapture(videoName)
   zoom = 1
   inch = 1
   x = 1
   y = 1

   if cap.isOpened():
      ret,frame = cap.read()
   else:
      ret =False

   ret,frame1 = cap.read()
   ret,frame2 = cap.read()

   while ret:
      ret,frame = cap.read()
      d=cv2.absdiff(frame1,frame2)
      grey=cv2.cvtColor(d,cv2.COLOR_BGR2GRAY)
      blur =cv2.GaussianBlur(grey,(5,5),0)
      ret,th=cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
      dilated=cv2.dilate(th,np.ones((5,5),np.uint8),iterations=5)
      contours,h = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
       
      cv2.drawContours(frame1,contours,-1,(0,255,0),2)

      for c in contours:
         x,y,w,h = cv2.boundingRect(c)
         if w * h > 400:  
            rect = cv2.minAreaRect(c)
            inch = distance_to_camera(KNOWN_WIDTH, focalLength, w)
        

      cv2.putText(frame1, "%.2fm" % (inch * 0.3048),(frame1.shape[1] - 150, frame1.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,1.0, (0, 0, 255), 3)
      cv2.imshow("image",frame1)

      cv2.imwrite("output/motion.png", frame2)

      img = Image.open("output/motion.png")
      if cv2.waitKey(200) == 27:
         break

      distance = inch * 0.3048

      if (distance <= 100):
         zoom = 1
      if (distance > 100 and distance <= 250):
         zoom = 3
      if (distance > 250):
         zoom = 7    
      
      print(distance, zoom)
      crop_image(img, (x, y), zoom)
      zoom = 1
     

      frame1 = frame2
      ret,frame2= cap.read()

   cv2.destroyAllWindows()
  
   cap.release()
