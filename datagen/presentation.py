import os
import logging
import numpy as np
import time
import cv2.cv2 as cv2
from dataBox import TextBox, LineBox, WordBox
import json
from PIL import Image, ImageFont
from skimage.util import random_noise
from bbox import BBox2D, XYXY

from logger import log
from ImageGenerator import ImageGenerator
from textImage import TextImage

imageGen = ImageGenerator()

imagesFolder = os.path.join('present', 'images')
jsonFolder = os.path.join('present', 'jsons')

images = ['3', '5', '17', '18', '19', '31', '89']

saveFolder = os.path.join('present')


for imageName in images:
    imagePath = os.path.join(imagesFolder, imageName+'.jpg')
    jsonPath = os.path.join(jsonFolder, imageName+'.json')
    with open(jsonPath, 'r') as fp:
        data = json.load(fp)
        boxes = data['boxes']
        for box in boxes:
            bbox = BB