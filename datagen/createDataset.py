import os

from textGenerator import TextGenerator
from ImageGenerator import ImageGenerator
from textImage import TextImage


imageGen = ImageGenerator()

from textGenerator import TextGenerator
textGen = TextGenerator(filePath=os.path.join('hindiTexts.csv'))
data = textGen.data['text']
# print(data[0])

textImageSaveDir = os.path.join('data', 'text', 'images')
textLabelSaveDir = os.path.join('data', 'text', 'labels')
lineImageSaveDir = os.path.join('data', 'lines', 'images')
lineLabelSaveDir = os.path.join('data', 'lines', 'labels')
for i in range(1568, 1570):
    text = data[i]
    textImage = TextImage(imageGen=imageGen, imageIndex=i)
    textImage.addNoiseToImage()
    textImage.addTextToImage(text)
    textImage.addGaussianNoiseToImage()
    textImage.saveImage(textImageSaveDir, textLabelSaveDir)
    textImage.saveLineImages(lineImageSaveDir, lineLabelSaveDir)
# print(textImage.getBBoxData())