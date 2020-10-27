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


    
if __name__ == '__main__':
    
    log.debug('Initializing Image')

    imageGen = ImageGenerator()

    imageSize = (1080, 720)
    backgroundColor = (255, 255, 255)
    
    img = imageGen.createBackgroundImage(size=imageSize, color=backgroundColor)
    background = img[:,:,:].copy()
    
    log.debug('Image Initialized')

    textGenerator = TextGenerator()

    # text = textGenerator.getRandomText()
    # text = 'उधर, ईरान ने परमाणु बम बनाने से इंकार किया है और कहा है कि उसका परमाणु कार्यक्रम शातिपूर्ण उद्देश्य के लिए है।'

    text = '''पूर्व पाकिस्तानी कप्तान अकरम ने कहा कि यदि खिलाड़ी दबाव भूलना भी चाहे तो दर्शक, क्रिकेट प्रेमी और मीडिया ऐसा नहीं करने देता है। उन्होंने कहा, लोग कहते हैं कि एशेज में बहुत दबाव होता है लेकिन भारत पाकिस्तान के मैचों में जितना दबाव होता उतना किसी अन्य के साथ खेलने में नहीं होता है। हर खिलाड़ी इन मैचों में अच्छा प्रदर्शन करना चाहता है। 
- मार्केट में एक्सफोलिएटिंग लिप स्क्रब आसानी से मिल जाएंगे। नहीं, तो आप बच्चों के मुलायम ब्रिसल वाले ब्रश को गोलाई में घुमाते हुए स्क्रब करें।
पूर्वी कैनाल मार्ग-
संपत्ति लंबे समय में बनाई जाती है और इस काम को मौजूदा जीवनशैली से समझौता करके नहीं किया जाना चाहिए। हमारे निवेश का तरीका कुछ ऐसा होना चाहिए कि निवेश से मिलने वाले रिटर्न की रकम मुद्रास्फीति यानी महंगाई दर से अधिक हो, और यही है संपत्ति सृजन का तरीका, अन्यथा मुद्रास्फीति संपत्ति को गटक जाएगी।
-amazon.com के किंडल ई-रीडर्स पर अब हैरी पॉटर की ई किताबें पढ़ी जा सकेंगी। कंपनी ने जे. के. रोलिंग की हैरी पॉटर सीरीज के एक लिए एक खास लाइसेंस हासिल किया है। इसके बाद हैरी पॉटर की सभी सात किताबें किंडल प्लैटफॉर्म पर उपलब्ध होंगी। इसकी शुरुआत 19 जून से होगी।
शिमला डिवीजन में 140 रूट रद्द हुए।'''

#     text = '''पूर्व पाकिस्तानी कप्तान अकरम ने कहा कि यदि खिलाड़ी दबाव भूलना भी चाहे तो दर्शक, क्रिकेट प्रेमी और मीडिया ऐसा नहीं करने देता है। उन्होंने कहा, लोग कहते हैं कि एशेज में बहुत दबाव होता है लेकिन भारत पाकिस्तान के मैचों में जितना दबाव होता उतना किसी अन्य के साथ खेलने में नहीं होता है। हर खिलाड़ी इन मैचों में अच्छा प्रदर्शन करना चाहता है। 
# - मार्केट में एक्सफोलिएटिंग लिप स्क्रब आसानी से मिल जाएंगे। नहीं, तो आप बच्चों के मुलायम ब्रिसल वाले ब्रश को गोलाई में घुमाते हुए स्क्रब करें।'''

    text = str(text)

    log.debug('Text Initialized')

    fontPath = os.path.join(os.getcwd(), 'hindiFonts', 'NotoSans-Regular.ttf')
    fontSize = 20

    log.debug('Font Initialized')

    startPostion=(100, 70)
    maxWidth = int(0.6*imageSize[1])

    img = imageGen.addText(img, text = text, fontPath=fontPath, fontSize=fontSize, startPostion=startPostion, maxWidth=maxWidth)


    # text = text.replace(' ', '\n')
    # print(text)
    
    size = imageGen.getTextSize(text=text, fontPath=fontPath, fontSize=fontSize)
    log.debug(f"Text Size : {size}")
    log.debug('Text Added')

    imgProcess = ImageFunctions()
    
    box1 = imgProcess.differenceBoundingBox(img, background, padding=0)
    
    font = ImageFont.truetype(fontPath , size=fontSize, layout_engine=ImageFont.LAYOUT_RAQM)

    
    textLines = imageGen.textwrap(text, font, maxWidth)
    bboxes = imageGen.getBoundingBoxes(textLines, startPostion=startPostion, fontPath=fontPath, fontSize=fontSize)

    boxes = []
    for item in  bboxes["lines"]:
        boxes.append(item['bounding_box'])
    for item in  bboxes["text"]:
        boxes.append(item)

    num = len(boxes)
    labels = [f'Line {i}' for i in range(1, num)]
    labels.append('Text Box')

    imgNoBoundingBox = img[:,:,:].copy()
    # imageGen.showImage(imgNoBoundingBox)

    newImg = imageGen.drawBoundingBoxes(imgNoBoundingBox, boxes, labels=labels)
    imageGen.showImage(newImg)

    # img = imageGen.drawBoundingBox(img, box1)
    # imageGen.showImage(img)
    # cv2.imwrite(f'Screenshot_{int(time.time())}.jpeg', img)

    noiseAmount = 0.1
    noisyImage = random_noise(imgNoBoundingBox, mode='poisson')
    noisyImage = np.array(255*noisyImage, dtype = 'uint8')
    noisyImage = imageGen.drawBoundingBox(noisyImage, box1)
    # cv2.imwrite(f'Screenshot_noisy_{int(time.time())}.jpeg', noisyImage)
    imageGen.showImage(noisyImage)

    # box2 = imgProcess.expectedBoundingBox(background, text=text, fontPath=fontPath, fontSize=20)
    # img2 = imageGen.drawBoundingBoxes(imgNoBoundingBox, [box1, box2], labels=['Box1', 'Box2'], thickness=3)
    # imageGen.showImage(img2)
    

    