from image_utils import ImageText
import os


color = (50, 50, 50)
text = 'Python is a cool programming language. You should learn it!'
font = 'Roboto-Black.ttf'
img = ImageText((800, 600), background=(255, 255, 255, 200)) # 200 = alpha

#write_text_box will split the text in many lines, based on box_width
#`place` can be 'left' (default), 'right', 'center' or 'justify'
#write_text_box will return (box_width, box_calculed_height) so you can
#know the size of the wrote text
img.write_text_box((300, 50), text, box_width=200, font_filename=font,
                   font_size=15, color=color)
# img.write_text_box((300, 125), text, box_width=200, font_filename=font,
#                    font_size=15, color=color, place='right')
# img.write_text_box((300, 200), text, box_width=200, font_filename=font,
#                    font_size=15, color=color, place='center')
# img.write_text_box((300, 275), text, box_width=200, font_filename=font,
#                    font_size=15, color=color, place='justify')

#You don't need to specify text size: can specify max_width or max_height
# and tell write_text to fill the text in this space, so it'll compute font
# size automatically
#write_text will return (width, height) of the wrote text
img.write_text((100, 350), 'test fill', font_filename=font,
               font_size='fill', max_height=150, color=color)


# fill_text_box will attempt to use up all available space in both x and 
# y dimensions, where the above example will only stick to one line
img.fill_text_box((100,100), text, box_width=600, box_height=400, 
                    font_filename=font)

img.save('sample-imagetext.png')