import os
from PIL import Image, ImageFont
from bbox import BBox2D, XYXY
import logging

from ImageGenerator import ImageGenerator
from logger import log
log.setLevel(logging.DEBUG)


class TextBox:
    lineBoxes = []
    def __init__(self, text, 
            fontPath = os.path.join('font', 'Roboto-Bold.ttf'),
            fontSize = 45,
            lineMargin = 1,
            maxWidth = None,
            imageGen = None):
        self.text = text
        self.font = ImageFont.truetype(fontPath, size=fontSize,
                                    layout_engine=ImageFont.LAYOUT_RAQM)
        
        if imageGen is None:
            imageGen = ImageGenerator()

        if maxWidth is None:
            raise ValueError('maxWidth argument is not given or None.')
        
        self.maxWidth = maxWidth 
        self.imageGen = imageGen
        self.textLines = imageGen.textwrap(self.text, self.font, self.maxWidth)
        self.marginX, self.marginY = imageGen.getMargin(self.font)
        self.lineMargin = imageGen.getLineMargin(self.font)
        self.lineBoxes = self.generateLineBoxes()
        self.textSize = self.getTextSize()
        self.textWidth, self.textHeight = self.textSize


    def getTextSize(self):
        _, descent = self.font.getmetrics()
        lineMargin = self.lineMargin

        textHeight = 0
        textWidth = 0
        for lineBox in self.lineBoxes:
            lineSize = lineBox.textSize
            textWidth = max(textWidth, lineSize[0])
            textHeight += lineSize[1] + descent + lineMargin
        
        return (textWidth, textHeight)

    def getBBox(self, startPostion = (0, 0)):
        marginX, marginY = (self.marginX, self.marginY)
        x,y = startPostion
        textWidth, textHeight = self.textSize

        textStartX = max(0, x - marginX)
        textStartY = max(0, y - marginY)
        textEndX = x + textWidth + marginX
        textEndY = y + textHeight + marginY

        box =  BBox2D([textStartY,
                       textStartX,
                       textEndY,
                       textEndX], mode=XYXY)


        _, descent = self.font.getmetrics()

        lineBBoxes = []
        prevStartY = y
        prevLineHeight = 0
        for lineBox in self.lineBoxes:
            lineStartPostion = (x, prevStartY + prevLineHeight)
            prevStartY = prevStartY + prevLineHeight
            prevLineHeight = lineBox.textSize[1] + descent + self.lineMargin
            lineBBox = lineBox.getBBox(startPostion=lineStartPostion)
            lineBBoxes.append(lineBBox)

        return (box, lineBBoxes)



    def generateLineBoxes(self):
        lineBoxes = []
        for line in self.textLines:
            lineBox = LineBox(line, font=self.font, imageGen=self.imageGen)
            lineBoxes.append(lineBox)
        return lineBoxes


class LineBox:
    wordBoxes = []
    def __init__(self, textLine, 
            font = None,
            imageGen = None):

        if imageGen is None:
            imageGen = ImageGenerator()

        if font is None:
            raise ValueError('font argument is not given or None.')

        self.imageGen = imageGen
        self.font = font
        self.text = textLine
        self.textSize = self.font.getsize(self.text)

        self.words = textLine.split()
        self.wordBoxes = self.generateWordBoxes()

    def generateWordBoxes(self):
        wordBoxes = []
        for word in self.words:
            wordBox = WordBox(word, font=self.font, imageGen=self.imageGen)
            wordBoxes.append(wordBox)
        return wordBoxes

    def getBBox(self, startPostion=(0, 0)):
        (marginX, marginY) = self.imageGen.getMargin(self.font)

        x, y = startPostion
        lineStartX = max(0, x - marginX + 1)
        lineStartY = max(0, y - marginY)
        lineSize = self.textSize
        lineEndX = x + lineSize[0] + marginX 
        lineEndY = y + lineSize[1] + marginY
        box = BBox2D([lineStartY,
                      lineStartX,
                      lineEndY,
                      lineEndX], mode=XYXY)


        wordBBoxes = []
        startX = x
        spaceWidth = self.imageGen.getSpaceWidth(self.font)
        constantSpaceWidth = spaceWidth
        currentText = ''

        for index, wordBox in enumerate(self.wordBoxes):
            # Code for detecting whiteSpace before character
            # Code will fail for tabs in data or for horizontal whiteSpaces other than multiple spaces
            while self.text[len(currentText)].isspace():
                currentText += self.text[len(currentText)]
                startX += constantSpaceWidth

            wordStartPostion = (startX, y)
            wordBBox = wordBox.getBBox(startPostion=wordStartPostion)
            wordBBoxes.append(wordBBox)

            if index+1 < len(self.wordBoxes):
                currentWord = wordBox.text
                currentText += currentWord + ' ' 
                nextWord = self.wordBoxes[index+1].text
                spaceWidth = self.imageGen.getSpaceWidthByWords(self.font, currentWord, nextWord)
                wordWidth = wordBox.textSize[0]
                startX = startX + wordWidth + spaceWidth
                self.text

        return (box, wordBBoxes)
        

class WordBox:
    characterBoxes = []
    def __init__(self, textWord, 
            font = None,
            imageGen = None):

        if imageGen is None:
            imageGen = ImageGenerator()

        if font is None:
            raise ValueError('font argument is not given or None.')

        self.imageGen = imageGen
        self.font = font
        self.text = textWord
        self.textSize = self.font.getsize(self.text)

    def getBBox(self, startPostion=(0,0)):
        marginX, marginY = self.imageGen.getWordMargin(self.font)
        x, y = startPostion

        wordStartX = max(0, x - marginX)
        wordStartY = max(0, y - marginY)
        wordSize = self.textSize
        wordEndX = x + wordSize[0] + marginX 
        wordEndY = y + wordSize[1] + marginY

        box = BBox2D([wordStartY,
                      wordStartX,
                      wordEndY,
                      wordEndX], mode=XYXY) 
        
        return box
