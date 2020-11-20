import numpy as np
import os
import random
import colorsys
import math

def get_colors(num_colors):
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        color = colorsys.hls_to_rgb(hue, lightness, saturation)
        color = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
        colors.append(color)
    return colors

def getDistanceBetweenColors(color1, color2):
    d = (color1[0] - color2[0])**2
    d += (color1[1] - color2[1])**2
    d += (color1[2] - color2[2])**2
    return int(math.sqrt(d))


def getGrayDistance(color1, color2):
    gray1 = (0.3 * color1[0]) + (0.59 * color1[1]) + (0.11 * color1[2])
    gray2 = (0.3 * color1[0]) + (0.59 * color1[1]) + (0.11 * color1[2])
    return abs(gray1 - gray2)



def getDistinctColors(color1=None, minDistance=30):
    if color1 is None:
        color1 = getRandomColor()
    color2 = getRandomColor()

    grayMin = max(minDistance/2, 120)
    grayDistance = getGrayDistance(color1, color2)
    d = getDistanceBetweenColors(color1, color2)
    while d<minDistance and grayDistance<grayMin:
        color2 = getRandomColor()
        d = getDistanceBetweenColors(color1, color2)
        grayDistance = getGrayDistance(color1, color2)
    return (color1, color2)


def getRandomFont(fontFolder):
    fonts = os.listdir(fontFolder)
    length = len(fonts)
    num = random.randint(1, length)
    fontPath = os.path.join(fontFolder, fonts[num-1])
    return fontPath


def getRandomColor():
    r = random.randint(1, 255)
    g = random.randint(1, 255)
    b = random.randint(1, 255)
    return (r, g, b)

def getRandomStartingPostion(textSize, imageSize):
    imageWidth, imageHeight = imageSize
    textWidth, textHeight = textSize

    xMin = max(int(0.05*imageWidth), 1)
    xMax = imageWidth - textWidth - max(int(0.05*imageWidth), 1)
    xMax = max(xMin, xMax)
    x = random.randint(xMin, xMax)

    yMin = max(int(0.03*imageHeight), 1)
    yMax = imageHeight - textHeight - max(int(0.03*imageWidth), 1)
    yMax = max(yMax, yMin)
    y = random.randint(yMin, yMax)

    return (x, y)