import os
import logging
import numpy as np
import time
import cv2.cv2 as cv2
from dataBox import TextBox, LineBox, WordBox

from logger import log
from ImageGenerator import ImageGenerator
from textImage import TextImage

text = '''मनुष्य अपने स्वार्थ सिद्धि और तरक्की  के कारण पर्यावरण को बेहद नुकसान पहुंचा रहा है। पर्यावरण का संतुलन बिगड़ रहा है। इसके कारण कई प्राकृतिक  आपदाओं को इसने जन्म दिया है।  भूकंप एक भयंकर प्राकृतिक आपदा है। यह एक भीषण संकट है।  भूकंप जैसे ही आता है , यह जीव जंतु , मनुष्य सभी की जान ले लेता है। पेड़ पौधे नष्ट हो जाते है।  बड़ी बड़ी इमारतें कुछ ही मिनटों में ताश के पत्तों की तरह ढह जाती है।  भूमि पर दरार पड़ जाती है। अचानक धरती पर तीव्र गति से कम्पन होती है कि एक ही झटके में सब कुछ नष्ट हो जाता है।  कई परिवार भूकंप की इस भयावह आपदा के शिकार हो जाते है।  हर तरफ  त्र्याही त्र्याही मच जाती है। भूकंप दो  अक्षरों -भू + कम्प से बना है।  भू मतलब धरती और कम्प का अर्थ है कम्पन। इस प्रकार भूमि  यानी  धरती पर अचानक आये कम्पन को भूकंप कहते है।'''
imageGen = ImageGenerator()
imageSize = (736, 1104) # (width, height)

lineImageSize = (736, 96)

textImage = TextImage(imageGen=imageGen)
textImage.addNoiseToImage()
textImage.addTextToImage(text)
textImage.addGaussianNoiseToImage()


imageGen = ImageGenerator()
imageSize = (736, 1104) # (width, height)
backgroundColor = (255, 255, 255)

img = imageGen.createBackgroundImage(size=imageSize, color=backgroundColor)
textImg = textImage.image

lineBox = textImage.textBoxes[0].lineBoxes[0]

lineImage = imageGen.extractImageROI(textImg, lineBox.bbox, outImageSize=lineImageSize)
(x, y) = imageGen.getStartingPointofRoi(lineBox.bbox, canvasSize=lineImageSize)
newStartPoint = (x+1, y+1)

lineBox.setStartPostion(newStartPoint)

boxes = [lineBox.bbox]
for wordBox in lineBox.wordBoxes:
    boxes.append(wordBox.bbox)


# lineImage = imageGen.drawBoundingBox(lineImage, lineBox.bbox)
lineImage = imageGen.drawBoundingBoxes(lineImage, boxes)
imageGen.showImage(lineImage)
imageGen.showImage(textImg)

log.setLevel(logging.DEBUG)