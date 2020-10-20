import os
import cv2.cv2 as cv2
import numpy as np
import logging
import json

from PIL import Image, ImageDraw, ImageFont
from bbox import BBox2D, XYXY
from utils import get_colors
import textwrap


from logger import log

log.setLevel(logging.DEBUG)


class ImageGenerator:
    
    def __init__(self):
        pass

    def createBackgroundImage(self, size=(200, 400), color=(255, 255, 255)):
        height, width = size
        backgroundImage = np.zeros((height,width,3), np.uint8)
        backgroundImage[:, :] = color
        return backgroundImage


    def getTextSize(self, text = "Helo helo",
            fontPath = os.path.join('font', 'Roboto-Bold.ttf'),
            fontSize = 45):
        
        font = ImageFont.truetype(fontPath , size=fontSize, layout_engine=ImageFont.LAYOUT_RAQM)
        return font.getsize(text)  # (Width, Height)

    


    def textwrap(self, text, font, maxWidth):
        lines = []
        if font.getsize(text)[0] <= maxWidth:
            lines.append(text)
        else:
            # split the line by spaces to get words
            words = text.split(' ')  
            i = 0
            # append every word to a line while its width is shorter than image width
            while i < len(words):
                line = ''        
                while i < len(words) and font.getsize(line + words[i])[0] <= maxWidth:                
                    line = line + words[i] + " "
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
                # when the line gets longer than the max width do not append the word,
                # add the line to the lines array
                lines.append(line)    
        return lines


    def addText(self, img,
            text = "Helo helo",
            startPostion = (50, 50),
            color = (0, 0, 0),
            fontPath = os.path.join('font', 'Roboto-Bold.ttf'),
            fontSize = 45,
            lineMargin = 1,
            maxWidth = None):
            
        # openCV to PIL
        img = Image.fromarray(img)
        font = ImageFont.truetype(fontPath , size=fontSize, layout_engine=ImageFont.LAYOUT_RAQM)

        # starting postion 
        x,y = startPostion 
        color = 'rgb' + str(color)

        # maxWidth
        if maxWidth is None:
            maxWidth = int(0.75*img.size[0])
        
        # textwrap
        lines = self.textwrap(text, font, maxWidth)

        _, descent = font.getmetrics()


        #draw the message on the backgroundImage
        draw = ImageDraw.Draw(img)
        for line in lines:
            lineHeight = font.getsize(line)[1] + descent + lineMargin
            draw.text((x,y), line, fill=color, font=font)        
            y = y + lineHeight
            

        # PIL to openCV
        img = np.asarray(img)
        return img


    def getBoundingBoxes(self, textLines,
            startPostion = (50, 50),
            fontPath = os.path.join('font', 'Roboto-Bold.ttf'),
            fontSize = 45,
            lineMargin = 1):
        
        bboxes = {
            "text" : [],
            "lines" : []
        } 

        font = ImageFont.truetype(fontPath , size=fontSize, layout_engine=ImageFont.LAYOUT_RAQM)

        marginX = 2
        marginY = 2

        startX = max(0, startPostion[0] - marginX) 
        startY = max(0, startPostion[1] - marginY)

        y = startY
        lineStart = (startPostion[0], startPostion[1])
        (x,y) = (startPostion[0], startPostion[1])
        ascent, descent = font.getmetrics()

        endX = 0
        endY = 0
        log.debug(len(textLines))

        for i , line in enumerate(textLines):
            lineStartX = max(0, x - marginX)
            lineStartY = max(0, y - marginY)
            
            lineSize = font.getsize(line)

            lineEndX = x + lineSize[0] + marginX
            lineEndY = y + lineSize[1] + descent + lineMargin + marginY

            lineHeight = font.getsize(line)[1] + descent + lineMargin   
            

            endX = max(lineEndX, endX)
            endY = max(lineEndY, endY)

            y = y + lineHeight
            
            box = BBox2D([lineStartY,
                      lineStartX,
                      lineEndY,
                      lineEndX], mode=XYXY) 
            
            details = {
                'line_num' : i+1,
                'bounding_box' : box
            }

            bboxes['lines'].append(details)
            

        box = BBox2D([startY,
                      startX,
                      endY,
                      endX], mode=XYXY)
        bboxes["text"].append(box)

        return bboxes        

        



    def drawBoundingBox(self, img, box, color=(25, 121, 67), thickness=2,
            label=None,
            fontFace = cv2.FONT_HERSHEY_PLAIN,
            fontScale = 0.9):
        point1 = (int(box.y1), int(box.x1))
        point2 = (int(box.y2), int(box.x2))
        img = cv2.rectangle(img, point1, point2, color, thickness=thickness)
        if label is not None:
            label_x = point1[0]
            label_y = max(point1[1]-2, 0)
            cv2.putText(img, label, (label_x, label_y), fontFace, fontScale, color)
        return img

    def drawBoundingBoxes(self, img, boxes, thickness = 2,
            labels = None,
            fontFace = cv2.FONT_HERSHEY_PLAIN,
            fontScale = 0.8):
        
        n = len(boxes)
        colors = get_colors(n)
        for i, box in enumerate(boxes):
            label = None
            if labels is not None:
                label = labels[i]
            img = self.drawBoundingBox(img, box, color=colors[i],
                     thickness=thickness,
                     label=label,
                     fontFace=fontFace,
                     fontScale=fontScale)

        return img

    def showImage(self, img, windowName='Image'):
        height, width = img.shape[:2]
        cv2.namedWindow(windowName, cv2.WINDOW_GUI_EXPANDED)
        cv2.resizeWindow(windowName, width, height)
        cv2.imshow(windowName, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
