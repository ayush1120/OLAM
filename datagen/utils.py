import numpy as np
import colorsys

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