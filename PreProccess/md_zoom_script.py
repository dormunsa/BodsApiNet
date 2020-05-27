import cv2
import numpy as np
from PIL import Image
import os.path
import argparse
import requests

# python motion_detector.py --video videos/bm.mp4

#globals
Image.MAX_IMAGE_PIXELS = 10000000000
i = 0

def crop_image(img, xy, scale_factor):

    global i

    if ( i % 7 == 0 ):
        axisX = xy[0]
        axisY = xy[1]

        while (axisX > 1):
            axisX = axisX / 10
        while (axisY > 1):
            axisY = axisY / 10

        center = (img.size[0] * axisX, img.size[1] * axisY)
        new_size = (img.size[0] / scale_factor, img.size[1] / scale_factor)
        left = max (0, (int) (center[0] - new_size[0] / 2))
        right = min (img.size[0], (int) (center[0] + new_size[0] / 2))
        upper = max (0, (int) (center[1] - new_size[1] / 2))
        lower = min (img.size[1], (int) (center[1] + new_size[1] / 2))
        cropped_img = img.crop((left, upper, right, lower))
        cropped_img = cropped_img.resize((1600,1200))


        cropped_img.save('output/newzoom' + str(i / 7) + '.JPEG', quality=95)

        content_type = 'image/jpeg'
        headers = {'content-type': content_type}

        img = cv2.imread('output/newzoom' + str(i / 7) + '.JPEG')
        # encode image as jpeg
        _, img_encoded = cv2.imencode('.jpg', img)
        # send http request with image and receive response
        response = requests.post("http://localhost:5000/pic", data=img_encoded.tostring(), headers=headers)

        print("api response: ")
        print(response.content)
        # here should be cod that sand current picture to ******Detection Machine******
        print(axisX, axisY, i / 3)
        
    i = i + 1

def getVideo(videoName):

   cap=cv2.VideoCapture(videoName)

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
      dilated=cv2.dilate(th,np.ones((3,3),np.uint8),iterations=3)
      contours, h = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      cv2.drawContours(frame1,contours,-1,(0,255,0),2)

      for c in contours:
            if cv2.contourArea(c) < 50:
                continue
            x,y,w,h = cv2.boundingRect(c)

      if ( type(h) == int):
          y = y + (2.5 * h)
          print(y)     
        
      #cv2.imshow("inter",frame1)
      cv2.imwrite("output/motion.jpg", frame2)

      if cv2.waitKey(40) == 27:
         break

      img = Image.open("output/motion.jpg")
      crop_image(img, (x, y), 0.000000000000001)


      frame1 = frame2
      ret,frame2= cap.read()

   cv2.destroyAllWindows()
   #VideoFileOutput.release()
   cap.release()
