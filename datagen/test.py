import os
import cv2.cv2 as cv2
import numpy as np
import logging
import json
from PIL import Image, ImageDraw, ImageFont
from bbox import BBox2D, XYXY
import textwrap
import time
from skimage.util import random_noise

from ImageGenerator import ImageGenerator
from ImageFunctions import ImageFunctions
from textGenerator import TextGenerator


from utils import get_colors
from logger import log
log.setLevel(logging.DEBUG)


# See How to properly calculate text size in PIL images
# https://levelup.gitconnected.com/how-to-properly-calculate-text-size-in-pil-images-17a2cc6f51fd


def noisy(noise_typ,image):
    
    if noise_typ == "gauss":
        row,col,ch= image.shape
        mean = 0
        var = 0.1
        sigma = var**0.5
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch).astype('uint8')
        noisy = cv2.add(image, gauss)
        return noisy
    elif noise_typ == "s&p":
        row,col,ch = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                for i in image.shape]
        out[coords] = 1

        # Pepper mode
        num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                for i in image.shape]
        out[coords] = 0
        return out
    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy
    elif noise_typ =="speckle":
        row,col,ch = image.shape
        gauss = np.random.randn(row,col,ch)
        gauss = gauss.reshape(row,col,ch)        
        noisy = image + image * gauss
        return noisy


    
if __name__ == '__main__':
    
    log.debug('Initializing Image')

    imageGen = ImageGenerator()

    imageSize = (1080, 720)
    backgroundColor = (0, 255, 255)
    
    img = imageGen.createBackgroundImage(size=imageSize, color=backgroundColor)
    background = img[:,:,:].copy()
    
    log.debug('Image Initialized')

    textGenerator = TextGenerator()

    text = textGenerator.getRandomText()
    # text = 'उधर, ईरान ने परमाणु बम बनाने से इंकार किया है और कहा है कि उसका परमाणु कार्यक्रम शातिपूर्ण उद्देश्य के लिए है।'

    log.debug('Text Initialized')

    fontPath = os.path.join(os.getcwd(), 'hindiFonts', 'NotoSans-Regular.ttf')
    fontSize = 5

    log.debug('Font Initialized')


    img = imageGen.addText(img, text = text, fontPath=fontPath, fontSize=40)

    # text = text.replace(' ', '\n')
    # print(text)
    
    size = imageGen.getTextSize(text=text, fontPath=fontPath, fontSize=fontSize)
    log.debug(f"Text Size : {size}")
    log.debug('Text Added')

    imgProcess = ImageFunctions()
    
    box1 = imgProcess.differenceBoundingBox(img, background, padding=0)
    
    imgNoBoundingBox = img[:,:,:].copy()
    # imageGen.showImage(imgNoBoundingBox)


    img = imageGen.drawBoundingBox(img, box1)
    imageGen.showImage(img)
    cv2.imwrite(f'Screenshot_{int(time.time())}.jpeg', img)

    noiseAmount = 0.3
    noisyImage = random_noise(imgNoBoundingBox, mode='s&p', amount=noiseAmount)
    noisyImage = np.array(255*noisyImage, dtype = 'uint8')
    noisyImage = imageGen.drawBoundingBox(noisyImage, box1)
    cv2.imwrite(f'Screenshot_noisy_{int(time.time())}.jpeg', noisyImage)
    imageGen.showImage(noisyImage)

    # box2 = imgProcess.expectedBoundingBox(background, text=text, fontPath=fontPath, fontSize=20)
    # img2 = imageGen.drawBoundingBoxes(imgNoBoundingBox, [box1, box2], labels=['Box1', 'Box2'], thickness=3)
    # imageGen.showImage(img2)
    

    