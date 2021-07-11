import os
import logging
import numpy as np
import cv2.cv2 as cv2
import pandas as pd
import random 
import json

from PIL import Image, ImageFont
from skimage.util import random_noise
from bbox import BBox2D, XYXY


from logger import log
from ImageGenerator import ImageGenerator
from ImageFunctions import ImageFunctions
from textGenerator import TextGenerator
from dataBox import TextBox
from olamUtils import getRandomColor, getDistinctColors 
import olamUtils

log.setLevel(logging.DEBUG)

boxTypes = {
    1 : 'Text Box',
    2 : 'Line Box',
    3 : 'Word Box',
    4 : 'Character Box'
}

class OBox:
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    yolo = []
    boxType = None
    boxTypeString = None
    imagePath = None
    boxSize = None
    imageSize = None
    text = None
    textBoxNum = None
    lineNum = None
    wordNum = None
    characterNum = None

    def __init__(self, box, boxType=1, imagePath=None,
                imageSize = (736, 1104),
                text=None,
                textBoxNum = None,
                lineNum = None,
                wordNum = None,
                characterNum = None):
        
        self.x1 = box.x1
        self.y1 = box.y1
        self.x2 = box.x2
        self.y2 = box.y2
        self.yolo = []
        self.boxType = boxType
        self.boxTypeString = boxTypes[boxType]
        self.imagePath = imagePath
        self.boxSize = (box.w, box.h)
        self.imageSize = imageSize
        self.text = text
        self.textBoxNum = textBoxNum
        self.lineNum = lineNum
        self.wordNum = wordNum
        self.characterNum = characterNum 
        self.yolo = self.getYolo()

    def getYolo(self):
        yolo = []
        box = self
        yolo.append(((box.x1 + box.x2)/2)/box.imageSize[0])
        yolo.append(((box.y1 + box.y2)/2)/box.imageSize[1])
        yolo.append(box.boxSize[0]/box.imageSize[0])
        yolo.append(box.boxSize[1]/box.imageSize[1])
        return yolo

    def getYoloString(self, classNum):
        yoloString = f"{classNum} {self.yolo[0]} {self.yolo[1]} {self.yolo[2]} {self.yolo[3]}\n"
        return yoloString



class TextImage:
    
    def __init__(self, imageGen = None,
            fontFolder = os.path.join('hindiFonts'),
            imageSize = (736, 1104),
            lineImageSize = (736, 96),
            minFontSize = 18,
            maxFontSize = 70,
            image = None,
            textIndex = None,
            datasetFileName = None,
            imageIndex = None):
        
        if imageGen is None:
            imageGen = ImageGenerator()

        self.textBoxes = []
        self.imageGen = imageGen
        self.fontFolder = fontFolder
        self.minFontSize = minFontSize
        self.maxFontSize = maxFontSize
        self.lineImageSize = lineImageSize
        self.imageIndex = imageIndex 
        
        self.backgroundColor = getRandomColor()
        self.imageSize = imageSize

        if image is None:
            image = imageGen.createBackgroundImage(size=self.imageSize, color=self.backgroundColor)
        self.image = image
    
    def addTextToImage(self, text, startingPosition=None, maxWidthFactor=None):
        fontPath = olamUtils.getRandomFont(fontFolder = self.fontFolder)
        log.debug(f'Font Path: {fontPath}')
        fontSize = random.randint(self.minFontSize, self.maxFontSize)
        textColor = olamUtils.getDistinctColors(color1=self.backgroundColor, minDistance=190)[1]
        if maxWidthFactor is None:
            maxWidthFactor = 0.3 + (0.65*random.random())
        maxWidth = maxWidthFactor*self.imageSize[0]
        textBox = TextBox(text, 
                        fontPath=fontPath,
                        fontSize=fontSize,
                        maxWidth=maxWidth,
                        imageGen=self.imageGen,
                        imageSize=self.imageSize)
        textSize = textBox.textSize
        if startingPosition is None:
            startingPosition = olamUtils.getRandomStartingPostion(textSize, self.imageSize)
        textBox.setStartPostion(startingPosition)
        self.textBoxes.append(textBox)
        text = textBox.text
        self.image = self.imageGen.addText(self.image, text=text,
                                startPostion=startingPosition,
                                color = textColor,
                                fontPath=fontPath,
                                fontSize=fontSize,
                                maxWidth=maxWidth)
    
    def addNoiseToImage(self):
        noiseAmount = random.random()*0.03
        if noiseAmount ==0:
            noiseAmount = 0.0001
        noisyImage = self.image
        imageGen = self.imageGen
        # rangeNum = random.randint(0,1)
        # for i in range(rangeNum):
        #         noisyImage = random_noise(noisyImage, mode='gaussian')
        #         noisyImage = np.array(255*noisyImage, dtype = 'uint8')
        noisyImage = random_noise(noisyImage, mode='s&p', amount=noiseAmount)
        noisyImage = np.array(255*noisyImage, dtype='uint8')
        self.image = noisyImage


    def addGaussianNoiseToImage(self):
        noisyImage = self.image
        noisyImage = random_noise(noisyImage, mode='gaussian')
        noisyImage = np.array(255*noisyImage, dtype = 'uint8')
        self.image = noisyImage

    def getWordBBoxes(self, imagePath = None):
        boxes = []
        for textBoxNum, textbox in enumerate(self.textBoxes):
           
            for lineNum, lineBox in enumerate(textbox.lineBoxes):
                lineBBox = lineBox.bbox
                

                for wordBoxNum, wordBox in enumerate(lineBox.wordBoxes):
                    wordBBox = wordBox.bbox
                    boxes.append(wordBBox)

        return boxes

    def getBBoxData(self, imagePath = None):
        boxes = []
        for textBoxNum, textbox in enumerate(self.textBoxes):
            textBBox = textbox.bbox
            box = OBox(textBBox, boxType=1, imagePath=imagePath,
                        imageSize=self.imageSize, text=textbox.text, 
                        textBoxNum=textBoxNum).__dict__
            boxes.append(box)
            for lineNum, lineBox in enumerate(textbox.lineBoxes):
                lineBBox = lineBox.bbox
                box = OBox(lineBBox, boxType=2, imagePath=imagePath,
                        imageSize=self.imageSize, text=lineBox.text, 
                        textBoxNum=textBoxNum, lineNum=lineNum).__dict__
                boxes.append(box)

                for wordBoxNum, wordBox in enumerate(lineBox.wordBoxes):
                    wordBBox = wordBox.bbox
                    box = OBox(wordBBox, boxType=3, imagePath=imagePath,
                            imageSize=self.imageSize, text=wordBox.text, 
                            textBoxNum=textBoxNum, lineNum=lineNum, wordNum=wordBoxNum).__dict__
                    boxes.append(box)

        boxesData = {"boxes" : boxes}
        return boxesData


    def getTextLineModelData(self, imagePath = None):
        boxesData = ''
        for textBoxNum, textbox in enumerate(self.textBoxes):
            textBBox = textbox.bbox
            box = OBox(textBBox, boxType=1, imagePath=imagePath,
                        imageSize=self.imageSize, text=textbox.text, 
                        textBoxNum=textBoxNum)
            boxesData = boxesData +  box.getYoloString(0)
            for lineNum, lineBox in enumerate(textbox.lineBoxes):
                lineBBox = lineBox.bbox
                box = OBox(lineBBox, boxType=2, imagePath=imagePath,
                        imageSize=self.imageSize, text=lineBox.text, 
                        textBoxNum=textBoxNum, lineNum=lineNum)
                boxesData = boxesData +  box.getYoloString(1)

        return boxesData




    def saveImage(self, imagePath, datapath):
        imageName = f'{self.imageIndex}.jpg'
        dataFileName = f'{self.imageIndex}.json'
        imageFilePath = os.path.join(imagePath, imageName)
        dataFilePath = os.path.join(datapath, dataFileName)
        cv2.imwrite(imageFilePath, self.image)
        data = self.getBBoxData(imagePath=imageFilePath)
        with open(dataFilePath, 'w') as fp:
            json.dump(data, fp, indent=2)

    def saveImage2(self, imagePath, datapath):
        imageName = f'{self.imageIndex}.jpg'
        dataFileName = f'{self.imageIndex}.txt'
        imageFilePath = os.path.join(imagePath, imageName)
        dataFilePath = os.path.join(datapath, dataFileName)
        cv2.imwrite(imageFilePath, self.image)
        data = self.getTextLineModelData(imagePath=imageFilePath)
        with open(dataFilePath, 'w') as fp:
            fp.write(data)
    

    def getLineImageData(self, textBoxNum = 0, lineNum=0, imagePath=None):
        boxes = []
        textbox = self.textBoxes[textBoxNum]
        lineBox = textbox.lineBoxes[lineNum]
        (x, y) = self.imageGen.getStartingPointofRoi(lineBox.bbox, self.lineImageSize)
        newStartingPosition = (x+1, y+1)
        lineBox.setStartPostion(newStartingPosition)
        lineBBox = lineBox.bbox
        box = OBox(lineBBox, boxType=2, imagePath=imagePath,
                imageSize=self.imageSize, text=lineBox.text, 
                textBoxNum=textBoxNum, lineNum=lineNum).__dict__
        boxes.append(box)

        for wordBoxNum, wordBox in enumerate(lineBox.wordBoxes):
            wordBBox = wordBox.bbox
            box = OBox(wordBBox, boxType=3, imagePath=imagePath,
                    imageSize=self.imageSize, text=wordBox.text, 
                    textBoxNum=textBoxNum, lineNum=lineNum, wordNum=wordBoxNum).__dict__
            boxes.append(box)
            
        boxesData = {"boxes" : boxes}
        return boxesData


    def getLineImageData2(self, textBoxNum = 0, lineNum=0, imagePath=None):
        # boxes = []
        boxesData = ''
        textbox = self.textBoxes[textBoxNum]
        lineBox = textbox.lineBoxes[lineNum]
        (x, y) = self.imageGen.getStartingPointofRoi(lineBox.bbox, self.lineImageSize)
        newStartingPosition = (x+1, y+1)
        lineBox.setStartPostion((1, 1))
        lineBBox = lineBox.bbox
        box = OBox(lineBBox, boxType=2, imagePath=imagePath,
                imageSize=self.imageSize, text=lineBox.text, 
                textBoxNum=textBoxNum, lineNum=lineNum)
        # boxes.append(box)

        for wordBoxNum, wordBox in enumerate(lineBox.wordBoxes):
            wordBBox = wordBox.bbox
            box = OBox(wordBBox, boxType=3, imagePath=imagePath,
                    imageSize=self.imageSize, text=wordBox.text, 
                    textBoxNum=textBoxNum, lineNum=lineNum, wordNum=wordBoxNum)
            boxesData = boxesData + box.getYoloString(0)
            # boxes.append(box)

        # boxesData = {"boxes" : boxes}
        return boxesData


    def saveLineImages(self, lineImagePath, lineDataPath):
        for textBoxNum, textBox in enumerate(self.textBoxes):
            for lineNum, lineBox in enumerate(textBox.lineBoxes):
                imageFileName = f'{self.imageIndex}_{textBoxNum}_{lineNum}.jpg'
                dataFileName = f'{self.imageIndex}_{textBoxNum}_{lineNum}.json'
                imageFilePath = os.path.join(lineImagePath, imageFileName)
                dataFilePath = os.path.join(lineDataPath, dataFileName)
                bbox = lineBox.bbox
                image = self.imageGen.extractImageROI(self.image, bbox,
                                    outImageSize=self.lineImageSize,
                                    outImageBackgroundColor=(0,0,0))
                data = self.getLineImageData(textBoxNum=textBoxNum,
                                            lineNum=lineNum,
                                            imagePath=imageFilePath)
                cv2.imwrite(imageFilePath, image)
                with open(dataFilePath, 'w') as fp:
                    json.dump(data, fp, indent=2)

    def saveLineImages2(self, lineImagePath, lineDataPath):
        for textBoxNum, textBox in enumerate(self.textBoxes):
            for lineNum, lineBox in enumerate(textBox.lineBoxes):
                imageFileName = f'{self.imageIndex}_{textBoxNum}_{lineNum}.jpg'
                dataFileName = f'{self.imageIndex}_{textBoxNum}_{lineNum}.txt'
                imageFilePath = os.path.join(lineImagePath, imageFileName)
                dataFilePath = os.path.join(lineDataPath, dataFileName)
                bbox = lineBox.bbox
                # image = self.imageGen.extractImageROI(self.image, bbox,
                #                     outImageSize=self.lineImageSize,
                #                     outImageBackgroundColor=(0,0,0))
                image = self.imageGen.getROI(self.image, bbox)
                data = self.getLineImageData2(textBoxNum=textBoxNum,
                                            lineNum=lineNum,
                                            imagePath=imageFilePath)
                

                # boxes = [ BBox2D([box['x1'], box['y1'], box['x2'], box['y2']], mode=XYXY) for box in data["boxes"]]
                # image = self.imageGen.drawBoundingBoxes(image, boxes)
                # self.imageGen.showImage(image)
                cv2.imwrite(imageFilePath, image)
                with open(dataFilePath, 'w') as fp:
                    fp.write(data)

    def saveWordImage(self, imagePath, dataPath, label):
        imageName = f'{self.imageIndex}.jpg'
        dataFileName = f'{self.imageIndex}.json'
        imageFilePath = os.path.join(imagePath, imageName)
        dataFilePath = os.path.join(dataPath, dataFileName)
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(imageFilePath, image)
        data = {'label' : label}
        with open(dataFilePath, 'w') as fp:
            json.dump(data, fp, indent=2)

    def saveImageOnly(self, save_dir):
        import datetime
        name = f'present_{datetime.datetime.now()}.jpg'
        filePath = os.path.join(save_dir, name)
        cv2.imwrite(filePath, self.image)
        image2 = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        name2 = f'present_{datetime.datetime.now()}_2.jpg'
        filePath = os.path.join(save_dir, name2)
        cv2.imwrite(filePath, image2)
        wordBoxes = textImage.getWordBBoxes()
        image3 =  textImage.imageGen.drawBoundingBoxes(textImage.image, wordBoxes)
        name2 = f'present_{datetime.datetime.now()}_3.jpg'
        filePath = os.path.join(save_dir, name2)
        cv2.imwrite(filePath, image3)
        image4 = textImage.imageGen.drawBoundingBoxes(image2, wordBoxes)
        name2 = f'present_{datetime.datetime.now()}_4.jpg'
        filePath = os.path.join(save_dir, name2)
        cv2.imwrite(filePath, image4)


if __name__ == '__main__':
    imageGen = ImageGenerator()
    textImage = TextImage(imageGen=imageGen, imageIndex=1, maxFontSize=50, minFontSize=30)
    textGen = TextGenerator()
    text = textGen.getRandomText()
    text = "ज्ञ"
    # while(len(text) < 400):
    #     text = textGen.getRandomText()
    save_dir = os.path.join(os.getcwd(), 'present')
    for i in range(1):
        imageIndex = f'present{i}_{random.randint(1,100)}' 
        textImage.addNoiseToImage()
        textImage.addTextToImage(text)
        # textImage.saveImage(save_dir, save_dir)
        

        textImage.addGaussianNoiseToImage()
        # wordBoxes = textImage.getWordBBoxes()
        # textImage.image =  textImage.imageGen.drawBoundingBoxes(textImage.image, wordBoxes)

        textImage.imageGen.showImage(textImage.image)
        textImage.saveImageOnly(save_dir)


        # textImage.saveImage(save_dir, save_dir)
        # textImage.saveLineImages(save_dir, save_dir)
        
        # textImage.saveLineImages2(save_dir, save_dir)
        # img3 = textImage.image.copy()
        # boxData = textImage.getBBoxData()
        # filePath = os.path.join(save_dir, 'present1.jpg')

        # for box in boxData['boxes']:
        #     if box['boxType'] == 1:
        #         bbox = BBox2D([box['x1'], box['y1'], box['x2'], box['y2']], mode=XYXY)
        #         img2 =  imageGen.drawBoundingBox(textImage.image, bbox)
        #         filePath = os.path.join(save_dir, 'present1.jpg')
        #         cv2.imwrite(filePath, img2)
            
        #     if box['boxType'] == 2:
        #         bbox = BBox2D([box['x1'], box['y1'], box['x2'], box['y2']], mode=XYXY)
        #         img3 = imageGen.drawBoundingBox(img3, bbox)
        # filePath = os.path.join(save_dir, 'present2.jpg')
        # cv2.imwrite(filePath, img3)




    # print(textImage.getBBoxData())
    imageGen.showImage(textImage.image)
    newImage = cv2.cvtColor(textImage.image, cv2.COLOR_BGR2GRAY)
    imageGen.showImage(newImage)
    

