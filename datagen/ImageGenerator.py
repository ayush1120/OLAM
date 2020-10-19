import os
import cv2.cv2 as cv2
import numpy as np
import logging
import json

from PIL import Image, ImageDraw, ImageFont
from bbox import BBox2D, XYXY
from utils import get_colors
import textwrap


from logger import log

log.setLevel(logging.DEBUG)


class ImageGenerator:
    
    def __init__(self):
        pass

    def createBackgroundImage(self, size=(200, 400), color=(255, 255, 255)):
        height, width = size
        backgroundImage = np.zeros((height,width,3), np.uint8)
        backgroundImage[:, :] = color
        return backgroundImage

    def addText(self, img,
            text = "Helo helo",
            startPostion = (50, 50),
            color = (0, 0, 0),
            fontPath = os.path.join('font', 'Roboto-Bold.ttf'),
            fontSize = 45):
            
        # openCV to PIL
        img = Image.fromarray(img)
        font = ImageFont.truetype(fontPath , size=fontSize, layout_engine=ImageFont.LAYOUT_RAQM)



        # starting postion 
        x,y = startPostion 
        color = 'rgb' + str(color)

        # textwrap
        textSize = font.getsize(text)
        log.debug(textSize)

        #draw the message on the backgroundImage
        draw = ImageDraw.Draw(img)
        draw.text((x,y), text, fill=color, font=font)        
        
        # PIL to openCV
        img = np.asarray(img)

        return img


    def drawBoundingBox(self, img, box, color=(25, 121, 67), thickness=2,
            label=None,
            fontFace = cv2.FONT_HERSHEY_PLAIN,
            fontScale = 0.9):
        point1 = (int(box.y1), int(box.x1))
        point2 = (int(box.y2), int(box.x2))
        img = cv2.rectangle(img, point1, point2, color, thickness=thickness)
        if label is not None:
            label_x = point1[0]
            label_y = max(point1[1]-2, 0)
            cv2.putText(img, label, (label_x, label_y), fontFace, fontScale, color)
        return img

    def drawBoundingBoxes(self, img, boxes, thickness = 2,
            labels = None,
            fontFace = cv2.FONT_HERSHEY_PLAIN,
            fontScale = 0.8):
        
        n = len(boxes)
        colors = get_colors(n)
        for i, box in enumerate(boxes):
            label = None
            if labels is not None:
                label = labels[i]
            img = self.drawBoundingBox(img, box, color=colors[i],
                     thickness=thickness,
                     label=label,
                     fontFace=fontFace,
                     fontScale=fontScale)

        return img

    def showImage(self, img, windowName='Image'):
        height, width = img.shape[:2]
        cv2.namedWindow(windowName, cv2.WINDOW_GUI_EXPANDED)
        cv2.resizeWindow(windowName, width, height)
        cv2.imshow(windowName, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
