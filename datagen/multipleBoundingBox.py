import os
import logging
import numpy as np
import cv2.cv2 as cv2
import pandas as pd
import random 
from PIL import Image, ImageFont
from skimage.util import random_noise
from bbox import BBox2D, XYXY


from logger import log
from ImageGenerator import ImageGenerator
from ImageFunctions import ImageFunctions
from textGenerator import TextGenerator
from dataBox import TextBox
log.setLevel(logging.DEBUG)


imageGen = ImageGenerator()
imageSize = (736, 1104)
backgroundColor = (255, 255, 255)
fontPath = os.path.join(os.getcwd(), 'hindiFonts', 'Poppins-ExtraLight.ttf')
fontSize = 35
font = ImageFont.truetype(fontPath , size=fontSize, layout_engine=ImageFont.LAYOUT_RAQM)

data = pd.read_csv('hindiTexts100.csv')['text']
length = len(data)



maxWidthFactor = 0.3 + (0.65*random.random())
maxWidth = maxWidthFactor*imageSize[0]

textGen = TextGenerator()
text = textGen.getRandomText()

textBox = TextBox(text, fontPath=fontPath, fontSize=fontSize, maxWidth=maxWidth,
        imageGen=imageGen)

