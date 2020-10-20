from PIL import ImageFont
import os

fontPath = os.path.join(os.getcwd(), 'hindiFonts', 'NotoSans-Regular.ttf')
fontSize = 5
font = ImageFont.truetype(fontPath , size=fontSize, layout_engine=ImageFont.LAYOUT_RAQM)
print(font.getsize("Hello World"))