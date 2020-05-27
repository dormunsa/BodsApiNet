import cv2
import numpy as np
from PIL import Image
import os.path
from imutils import paths
import requests

# globals
Image.MAX_IMAGE_PIXELS = 10000000000
i = 0
KNOWN_WIDTH = 9.05
focalLength = 621.681

np.seterr(divide='ignore', invalid='ignore')


def crop_image(img, xy, scale_factor, m):
    global i
    # if (scale_factor == {[]})
    if (scale_factor < 200):
        scale_factor = 2
    if (scale_factor >= 200 and scale_factor < 1000):
        scale_factor = 5
    if (scale_factor > 1000):
        scale_factor = 10

    if (i % 7 == 0):
        w, h = img.size
        img = img.crop((xy[0] - w / scale_factor, xy[1] - h / scale_factor,
                        xy[0] + w / scale_factor, xy[1] + h / scale_factor))
        cropped_img = img.resize((w, h), Image.LANCZOS)
        cropped_img.save('output/newzoom' + str(i / 7) + '-' + str(m) + '.JPEG', quality=95)
        content_type = 'image/jpeg'
        headers = {'content-type': content_type}
        img = cv2.imread('output/newzoom' + str(i / 7) + '-' + str(m) + '.JPEG')
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


def main(videoName):
    cap = cv2.VideoCapture(videoName)

    if cap.isOpened():
        ret, frame = cap.read()
    else:
        ret = False

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    cv2.imwrite("output/motion.png", frame2)
    img = Image.open("output/motion.png")

    while ret:
        ret, frame = cap.read()
        d = cv2.absdiff(frame1, frame2)
        grey = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, (5, 5), 0)
        _, th = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(th, np.ones((3, 3), np.uint8), iterations=3)
        contours, h = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

        for c in contours:
            if cv2.contourArea(c) < 50:
                continue

            x, y, w, h = cv2.boundingRect(c)
            rect = cv2.minAreaRect(c)
            inch = distance_to_camera(KNOWN_WIDTH, focalLength, w)
            imgH, imgW = img.size
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame1, [box], -1, (0, 255, 0), 2)

        cv2.imshow("image", frame1)
        cv2.imwrite("output/motion.png", frame2)

        img = Image.open("output/motion.png")
        if cv2.waitKey(100) == 27:
            break

        try:
            relative = (imgH * imgW) / (w * h)
            crop_image(img, (x, y), (imgH * imgW) / (w * h), inch * 0.0254)
            print((w * h))
        except:
            continue
        frame1 = frame2
        ret, frame2 = cap.read()
        if (not ret):
            break
    cv2.destroyAllWindows()

    cap.release()
