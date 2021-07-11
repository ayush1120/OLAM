import os
import logging

from textGenerator import TextGenerator
from ImageGenerator import ImageGenerator
from textImage import TextImage


from logger import log

log.setLevel(logging.DEBUG)


imageGen = ImageGenerator()

from textGenerator import TextGenerator
textGen = TextGenerator(filePath=os.path.join('hindiTexts.csv'))
data = textGen.data['text']
# print(data[0])

textImageSaveDir = os.path.join('data', 'text', 'images')
textLabelSaveDir = os.path.join('data', 'text', 'labels')
lineImageSaveDir = os.path.join('data', 'lines', 'images')
lineLabelSaveDir = os.path.join('data', 'lines', 'labels')
total = 5000
for i in range(95, 1000):
    log.info(f'Image Done.... {i}/{total}')
    text = data[i]
    textImage = TextImage(imageGen=imageGen, imageIndex=i)
    textImage.addNoiseToImage()
    textImage.addTextToImage(text)
    textImage.addGaussianNoiseToImage()
    textImage.saveImage2(textImageSaveDir, textLabelSaveDir)
    textImage.saveLineImages2(lineImageSaveDir, lineLabelSaveDir)
# print(textImage.getBBoxData())