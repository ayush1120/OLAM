import os
import cv2.cv2 as cv2
import numpy as np
import logging
import json
from PIL import Image, ImageDraw, ImageFont
from bbox import BBox2D, XYXY

from utils import get_colors


class ImageFunctions:
    
    def __init__(self):
        pass


    def expectedBoundingBox(self, img,
        text = "Helo helo",
        startPostion = (50, 50),
        fontPath = os.path.join('font', 'Roboto-Bold.ttf'),
        fontSize = 45):

        # openCV to PIL
        img = Image.fromarray(img)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(fontPath , size=fontSize)
        size_width, size_height = draw.textsize(text, font)
        endPosition = (startPostion[0]+size_height, startPostion[1]+size_width)

        box = BBox2D([startPostion[0],
                      startPostion[1],
                      endPosition[0],
                      endPosition[1]], mode=XYXY) 

        return box


    def getBoundingBox(self, diff, padding = 5):
        
        height, width = diff.shape
        arr = np.nonzero(diff)
        x1 =  max(min(arr[0]) - padding, 0)
        y1 =  max(min(arr[1]) - padding, 0)
        x2 =  min(max(arr[0]) + padding, height - 1)
        y2 =  min(max(arr[1]) + padding, width - 1)
        # point1 = (y1, x1)
        # point2 = (y2, x2)
        # return (point1, point2)
        box = BBox2D([x1, y1, x2, y2], mode=XYXY)
        return box


    def differenceBoundingBox(self, img1, img2, padding=5):
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        diff = np.abs(gray1 - gray2)

        return self.getBoundingBox(diff, padding=padding)

