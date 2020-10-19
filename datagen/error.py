from PIL import ImageFont
font = ImageFont.truetype("Roboto-Black.ttf", layout_engine=ImageFont.LAYOUT_RAQM)
print(font.getsize("Hello World"))