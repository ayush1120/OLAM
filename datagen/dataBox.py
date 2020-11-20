import os
from PIL import Image, ImageFont
from bbox import BBox2D, XYXY
import logging

from ImageGenerator import ImageGenerator
import textUtils
from logger import log
log.setLevel(logging.DEBUG)


class TextBox:
    lineBoxes = []
    startPostion = (0, 0)
    bbox = None
    def __init__(self, text, 
            fontPath = os.path.join('font', 'Roboto-Bold.ttf'),
            fontSize = 45,
            maxWidth = None,
            imageGen = None,
            startPostion = None,
            imageSize = (736, 1104)):
        
        self.imageSize = imageSize
        self.font = ImageFont.truetype(fontPath, size=fontSize,
                                    layout_engine=ImageFont.LAYOUT_RAQM)

        if imageGen is None:
            imageGen = ImageGenerator()

        if maxWidth is None:
            raise ValueError('maxWidth argument is not given or None.')
        
        self.maxWidth = maxWidth 
        self.imageGen = imageGen
        self.marginX, self.marginY = imageGen.getMargin(self.font)
        self.lineMargin = imageGen.getLineMargin(self.font)
        
        self.text = self.processText(text=text)
        self.textLines = imageGen.textwrap(self.text, self.font, self.maxWidth)
        self.textSize = self.getTextSize()
        self.lineBoxes = self.generateLineBoxes()
        self.textWidth, self.textHeight = self.textSize
        

        if startPostion is not None:
            self.startPostion = startPostion
        else:
            self.startPostion = (0,0)
        
        self.updateBBox()

    def processText(self, text):
        # Check Words
        log.debug('''Yet to Implement Word Check, if all words are in english aur hindi.
        And words are in correct form.''')

        # Reduce text if text height is more than image size
        textHeight = self.getTextSize(text=text)[1]
        imageHeight = self.imageSize[1]
        maxTextHeight = int(0.95*imageHeight)
        while textHeight > maxTextHeight:
            text = textUtils.splitTextRandom(text=text)
            textHeight = self.getTextSize(text=text)[1]
            
        return text


    def setStartPostion(self, startPostion):
        self.startPostion = startPostion
        self.updateBBox()


    def updateBBox(self):
        marginX, marginY = (self.marginX, self.marginY)
        x,y = self.startPostion
        textWidth, textHeight = self.textSize
        textStartX = max(0, x - marginX)
        textStartY = max(0, y - marginY)
        textEndX = x + textWidth + marginX
        textEndY = y + textHeight + marginY

        box =  BBox2D([textStartX,
                       textStartY,
                       textEndX,
                       textEndY], mode=XYXY)
    
        self.bbox = box

        _, descent = self.font.getmetrics()

        prevStartY = y
        prevLineHeight = 0
        for lineBox in self.lineBoxes:
            lineStartPostion = (x, prevStartY + prevLineHeight)
            prevStartY = prevStartY + prevLineHeight
            prevLineHeight = lineBox.textSize[1] + descent + self.lineMargin
            lineBox.setStartPostion(lineStartPostion)


    def getTextSize(self, text=None):
        _, descent = self.font.getmetrics()
        lineMargin = self.lineMargin

        if text is None:
            textLines = self.textLines
        else:
            textLines = self.imageGen.textwrap(text, self.font, self.maxWidth)
        textHeight = 0
        textWidth = 0
        for line in textLines:
            lineSize = self.font.getsize(line)
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

        box =  BBox2D([textStartX,
                       textStartY,
                       textEndX,
                       textEndY], mode=XYXY)


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

    def setStartPostion(self, startPostion):
        self.startPostion = startPostion
        self.updateBBox()

    def updateBBox(self):
        (marginX, marginY) = self.imageGen.getMargin(self.font)

        x, y = self.startPostion
        lineStartX = max(0, x - marginX + 1)
        lineStartY = max(0, y - marginY)
        lineSize = self.textSize
        lineEndX = x + lineSize[0] + marginX 
        lineEndY = y + lineSize[1] + marginY
        box = BBox2D([lineStartX,
                      lineStartY,
                      lineEndX,
                      lineEndY], mode=XYXY)

        self.bbox = box

        startX = x
        spaceWidth =  self.imageGen.getSpaceWidth(self.font)
        constantSpaceWidth = spaceWidth
        currentText = ''

        for index, wordBox in enumerate(self.wordBoxes):
            # Code for detecting whiteSpace before character
            # Code will fail for tabs in data or for horizontal whiteSpaces other than multiple spaces
            while self.text[len(currentText)].isspace():
                currentText += self.text[len(currentText)]
                startX += constantSpaceWidth

            wordStartPostion = (startX, y)
            wordBox.setStartPostion(wordStartPostion)

            if index+1 < len(self.wordBoxes):
                currentWord = wordBox.text
                currentText += currentWord + ' ' 
                nextWord = self.wordBoxes[index+1].text
                spaceWidth = self.imageGen.getSpaceWidthByWords(self.font, currentWord, nextWord)
                wordWidth = wordBox.textSize[0]
                startX = startX + wordWidth + spaceWidth

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
        box = BBox2D([lineStartX,
                      lineStartY,
                      lineEndX,
                      lineEndY], mode=XYXY)


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

            wordStartPosition = (startX, y)
            wordBox.setStartPostion(wordStartPosition)
            wordBBox = wordBox.getBBox(startPostion=wordStartPosition)
            wordBBoxes.append(wordBBox)

            if index+1 < len(self.wordBoxes):
                currentWord = wordBox.text
                currentText += currentWord + ' ' 
                nextWord = self.wordBoxes[index+1].text
                spaceWidth = self.imageGen.getSpaceWidthByWords(self.font, currentWord, nextWord)
                wordWidth = wordBox.textSize[0]
                startX = startX + wordWidth + spaceWidth

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


    def setStartPostion(self, startPostion):
        self.startPostion = startPostion
        self.updateBBox()

    def updateBBox(self):
        marginX, marginY = self.imageGen.getWordMargin(self.font)
        x, y = self.startPostion

        wordStartX = max(0, x - marginX)
        wordStartY = max(0, y - marginY)
        wordSize = self.textSize
        wordEndX = x + wordSize[0] + marginX 
        wordEndY = y + wordSize[1] +  marginY

        box = BBox2D([wordStartX,
                      wordStartY,
                      wordEndX,
                      wordEndY], mode=XYXY) 
        self.bbox = box




    def getBBox(self, startPostion=(0,0)):
        marginX, marginY = self.imageGen.getWordMargin(self.font)
        x, y = startPostion

        wordStartX = max(0, x - marginX)
        wordStartY = max(0, y - marginY)
        wordSize = self.textSize
        wordEndX = x + wordSize[0] + marginX 
        wordEndY = y + wordSize[1] + marginY

        box = BBox2D([wordStartX,
                      wordStartY,
                      wordEndX,
                      wordEndY], mode=XYXY) 
        
        return box
