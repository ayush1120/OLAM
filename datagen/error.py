from PIL import ImageFont
import os
import random

from textGenerator import TextGenerator
from ImageGenerator import ImageGenerator
import pandas as pd

# textGenerator = TextGenerator()
# text = textGenerator.getRandomText()

# data = pd.read_csv('lol.csv')
# size =  len(data.text)
# text = data.loc[random.randint(0, size-1), 'text']

text = 'सूत्रों के मुताबिक दाऊद को दिल के दो दौरे पड़ चुके हैं, जिसके चलते उसने अपनी गतिविधियां सीमित कर दी हैं। कराची में उसके डॉक्टरों ने उसे ज्यादा चलने-फिरने से मना किया है। दवाइयों के सहारे जी रहे 56 वर्षीय दाऊद को लगता है उसका दम किसी भी वक्त निकल सकता है।'

# print(f'text : {text}')


fontPath = os.path.join(os.getcwd(), 'hindiFonts', 'NotoSans-Regular.ttf')
fontSize = 1
font = ImageFont.truetype(fontPath , size=fontSize, layout_engine=ImageFont.LAYOUT_RAQM)

imgSize = (1080, 720)
maxWidth = 0.75*imgSize[1]

imageGen = ImageGenerator()

lines = imageGen.textwrap(text=text, font=font, maxWidth=maxWidth)

# text = 'उधर, ईरान ने परमाणु बम बनाने से इंकार किया है और कहा है कि उसका परमाणु कार्यक्रम शातिपूर्ण उद्देश्य के लिए है।'

# print(lines)

a = font.getmask(lines[0]).getbbox()
b = font.getsize(lines[0])
ascent, descent = font.getmetrics()
margin = 2

print(f'a : {a}')
print(f'b : {b}')
# print(f'c : {c}')