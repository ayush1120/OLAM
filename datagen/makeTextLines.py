import os
import logging
import numpy as np
import time
import cv2.cv2 as cv2
from PIL import Image, ImageFont
from skimage.util import random_noise
from bbox import BBox2D, XYXY


from logger import log
from ImageGenerator import ImageGenerator
from ImageFunctions import ImageFunctions

log.setLevel(logging.DEBUG)

imageGen = ImageGenerator()
imageSize = (1080, 720)
backgroundColor = (255, 255, 255)

img = imageGen.createBackgroundImage(size=imageSize, color=backgroundColor)
background = img[:,:,:].copy()

text = '''पूर्व पाकिस्तानी कप्तान अकरम ने'''

text = '''केच्इच्छुक पूर्व पाकिस्तानी कप्तान अकरम ने कहा कि यदि खिलाड़ी दबाव भूलना भी चाहे तो दर्शक, क्रिकेट प्रेमी और मीडिया to detect the effect of different segmentation approaches on the different metrics such as ऐसा नहीं करने देता है। उन्होंने कहा, लोग कहते हैं कि एशेज में बहुत दबाव होता है लेकिन भारत पाकिस्तान के मैचों में जितना To gain insights on questions like what part of the image for दबाव होता उतना किसी अन्य के साथ खेलने में नहीं होता है। हर   खिलाड़ी   इन मैचों में अच्छा प्रदर्शन करना चाहता है। 
- मार्केट में एक्सफोलिएटिंग लिप स्क्रब आसानी से मिल जाएंगे। नहीं, तो आप बच्चों के मुलायम ब्रिसल वाले ब्रश को गोलाई में घुमाते हुए स्क्रब करें।'''


text = '''मनुष्य अपने स्वार्थ सिद्धि और तरक्की  के कारण पर्यावरण को बेहद नुकसान पहुंचा रहा है। पर्यावरण का संतुलन बिगड़ रहा है। इसके कारण कई प्राकृतिक  आपदाओं को इसने जन्म दिया है।  भूकंप एक भयंकर प्राकृतिक आपदा है। यह एक भीषण संकट है।  भूकंप जैसे ही आता है , यह जीव जंतु , मनुष्य सभी की जान ले लेता है। पेड़ पौधे नष्ट हो जाते है।  बड़ी बड़ी इमारतें कुछ ही मिनटों में ताश के पत्तों की तरह ढह जाती है।  भूमि पर दरार पड़ जाती है। अचानक धरती पर तीव्र गति से कम्पन होती है कि एक ही झटके में सब कुछ नष्ट हो जाता है।  कई परिवार भूकंप की इस भयावह आपदा के शिकार हो जाते है।  हर तरफ  त्र्याही त्र्याही मच जाती है। भूकंप दो  अक्षरों -भू + कम्प से बना है।  भू मतलब धरती और कम्प का अर्थ है कम्पन। इस प्रकार भूमि  यानी  धरती पर अचानक आये कम्पन को भूकंप कहते है।'''

# text = '''शिकार हो जाते है।  हर तरफ  त्र्याही त्र्याही मच जाती है।'''

fontPath = os.path.join(os.getcwd(), 'hindiFonts', 'NotoSans-Regular.ttf')
fontSize = 25

font = ImageFont.truetype(fontPath , size=fontSize, layout_engine=ImageFont.LAYOUT_RAQM)

startPostion=(100, 70)
maxWidth = int(0.6*imageSize[1])

img = imageGen.addText(img, text = text, fontPath=fontPath, fontSize=fontSize,
        startPostion=startPostion, maxWidth=maxWidth)

size = imageGen.getTextSize(text=text, fontPath=fontPath, fontSize=fontSize)

multiline_size = font.getsize_multiline(text)
log.debug(f'Size Multiline : {multiline_size}')

textLines = imageGen.textwrap(text, font, maxWidth)

log.debug(f'Line 1 : {textLines[0]}')


# Generating Box for Line 1
myLine = textLines[0]
marginX, marginY = imageGen.getMargin(font=font)

log.debug(f"margin : {(marginX, marginY)}")

ascent, descent = font.getmetrics()
myTextSize = font.getsize(myLine)

log.debug(f'My line size : {myTextSize}')




from dataBox import TextBox
textBox = TextBox(text=text, fontPath=fontPath, fontSize=fontSize,
            maxWidth=maxWidth, imageGen=imageGen)


# Word Bounding Box
line1 = textBox.textLines[0]
line1Words = line1.split(' ')
bbox1 = imageGen.getBoundingBox(startPostion=startPostion, textSize=font.getsize(line1Words[0]))
twoLine1Words = line1Words[0] + ' ' + line1Words[1]
bbox2 = imageGen.getBoundingBox(startPostion=startPostion, textSize=font.getsize(twoLine1Words))
# space bbox
spaceWidth = imageGen.getSpaceWidth(font)
bbox3 = BBox2D([bbox1.x1, bbox1.y2, bbox1.x2, bbox1.y2 + spaceWidth], mode=XYXY)
# log.debug( f"spaceWidth : {spaceWidth}" )
# log.debug( f"x1 : {bbox3.x1}" )
# log.debug( f"y1 : {bbox3.y1}" )
# log.debug( f"x2 : {bbox3.x2}" )
# log.debug( f"y2 : {bbox3.y2}" )



# lineBox = textBox.lineBoxes[0]
# lineBBox = lineBox.getBBox(startPostion=startPostion)

textBBox, otherBoxes = textBox.getBBox(startPostion=startPostion)

lineBBoxes = []
wordBBoxes = []

for item in otherBoxes:
        lineBBox, insideLineBBoxes = item
        lineBBoxes.append(lineBBox)
        wordBBoxes.extend(insideLineBBoxes) 


# bboxes = imageGen.getBoundingBoxes(textLines, startPostion=startPostion, fontPath=fontPath,
#             fontSize=fontSize)

boxes = []
# boxes = lineBBoxes
# boxes.append(textBBox)
boxes.extend(wordBBoxes)

# boxes = [bbox1, bbox2, bbox3]
# boxes = [bbox3]

# for item in bboxes["lines"][1:]:
#     boxes.append(item['bounding_box'])
#     break

# for item in  bboxes["text"]:
#     boxes.append(item)

num = len(boxes)
labels = [f'Line {i}' for i in range(1, num)]
labels.append('Text Box')




# imgNoBoundingBox = img
imgNoBoundingBox = img[:,:,:].copy()
# imageGen.showImage(imgNoBoundingBox, 'Without Bounding Boxes')

newImg = imageGen.drawBoundingBoxes(img, boxes, labels=None)
# imageGen.showImage(newImg)




timeString = time.strftime("%a__%d_%b_%Y_%H_%M_%S")
fileName = f'Screenshot_All_Bounding_Boxes_{timeString}.jpeg'
filePath = os.path.join('out_images', fileName)
imageGen.showImage(newImg, windowName=fileName)

cv2.imwrite(filePath, newImg)


noiseAmount = 0.1
noisyImage = random_noise(imgNoBoundingBox, mode='poisson')
noisyImage = np.array(255*noisyImage, dtype = 'uint8')

for i in range(5):
        noisyImage = random_noise(noisyImage, mode='poisson')
        noisyImage = np.array(255*noisyImage, dtype = 'uint8')

noisyImage = imageGen.drawBoundingBoxes(noisyImage, boxes)
# imageGen.showImage(noisyImage)

noisyFileName = f'Screenshot_Noisy_All_Bounding_Boxes_{timeString}.jpeg'
filePath = os.path.join('out_images', noisyFileName)
cv2.imwrite(filePath, noisyImage)
