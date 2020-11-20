import os
import logging
import json

from textGenerator import TextGenerator
from ImageGenerator import ImageGenerator
from textImage import TextImage

import cv2.cv2 as cv2
from logger import log

log.setLevel(logging.DEBUG)

characterClasses = None
with open('characterClasses.json', 'r') as fp:
    characterClasses = json.load(fp)

imageGen = ImageGenerator()

from textGenerator import TextGenerator
textGen = TextGenerator(filePath=os.path.join('hindiTexts.csv'))
data = textGen.data['text']
# print(data[0])
limit = 3000
k = 0
bigFlag = 0
start = 600
end = 1000

offset = 25000
flag =  0


imageSaveDir = os.path.join('wordData', 'images')
labelSaveDir = os.path.join('wordData', 'labels')


def saveDetails(start, end, k, offset):
    data = {
        'start' : start,
        'end' : end,
        'lastImage' : k+offset
    }
    with open('wordDataSaveTextIndex.json','w') as fp:
        json.dump(data, fp)


for i in range(start, end):
    text = data[i]
    words = text.split()
    for word in words:
        flag = 0
        label = []
        characters = list(word)
        for character in characters:
            if character not in characterClasses.keys():
                flag=1
                break
            else:
                label.append(characterClasses[character])
        if flag==1:
            continue
        else:
            k = k+1

        if k>=limit:
            bigFlag = 1
            break

        log.info(f'Completed Image {k+offset}/{limit+offset}')
        print(word)
        print(label)

        imageText = word
        print(imageText)
        textImage = TextImage(imageGen=imageGen, imageIndex=offset+k, imageSize = (128, 32), minFontSize=14, maxFontSize=22)
        textImage.addGaussianNoiseToImage()
        textImage.addTextToImage(imageText, maxWidthFactor=0.9)
        # textImage.addNoiseToImage()
        # image = cv2.cvtColor(textImage.image, cv2.COLOR_BGR2GRAY)
        # textImage.imageGen.showImage(image)
        textImage.saveWordImage(imageSaveDir, labelSaveDir, label)


    if bigFlag == 1:
        saveDetails(start, i, k, offset)
        break


if bigFlag == 0:
    saveDetails(start, end, k, offset)


