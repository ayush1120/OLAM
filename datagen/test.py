import os
import cv2.cv2 as cv2
import numpy as np
import logging
import json
from PIL import Image, ImageDraw, ImageFont
from bbox import BBox2D, XYXY
import textwrap

from ImageGenerator import ImageGenerator
from ImageFunctions import ImageFunctions
from textGenerator import TextGenerator


from utils import get_colors
from logger import log
log.setLevel(logging.DEBUG)


# See How to properly calculate text size in PIL images
# https://levelup.gitconnected.com/how-to-properly-calculate-text-size-in-pil-images-17a2cc6f51fd



if __name__ == '__main__':
    imageGen = ImageGenerator()
    img = imageGen.createBackgroundImage()
    background = img[:,:,:].copy()
    
    textGenerator = TextGenerator()

    text = textGenerator.getRandomText()
    fontPath = os.path.join(os.getcwd(), 'hindiFonts', 'Poppins-BlackItalic.ttf')
    fontSize = 20

    # print(text)

    wrapped_text = textwrap.wrap(text, width=80)
    print(wrapped_text)

    img = imageGen.addText(img, text = text, fontPath=fontPath, fontSize=40)

    imgProcess = ImageFunctions()
    
    box1 = imgProcess.differenceBoundingBox(img, background, padding=0)
    # imgNoBoundingBox = img[:,:,:].copy()

    img = imageGen.drawBoundingBox(img, box1)
    imageGen.showImage(img)

    # box2 = imgProcess.expectedBoundingBox(background, text=text, fontPath=fontPath, fontSize=20)
    # img2 = imageGen.drawBoundingBoxes(imgNoBoundingBox, [box1, box2], labels=['Box1', 'Box2'], thickness=3)
    # imageGen.showImage(img2)
    

    