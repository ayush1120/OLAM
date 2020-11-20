import os
import random

from ImageGenerator import ImageGenerator

def splitTextRandom(text):
    length = len(text)
    split = 0.6 + random.random()*0.32
    endChar = int(split*length)
    for i in range(endChar, 0, -1):
        if text[i].isspace():
            endChar = i
            break

    text = text[:endChar]
    return text


if __name__ == '__main__':
    text = '''मनुष्य अपने स्वार्थ सिद्धि और तरक्की  के कारण पर्यावरण को बेहद नुकसान पहुंचा रहा है। पर्यावरण का संतुलन बिगड़ रहा है। इसके कारण कई प्राकृतिक  आपदाओं को इसने जन्म दिया है।  भूकंप एक भयंकर प्राकृतिक आपदा है। यह एक भीषण संकट है।  भूकंप जैसे ही आता है , यह जीव जंतु , मनुष्य सभी की जान ले लेता है। पेड़ पौधे नष्ट हो जाते है।  बड़ी बड़ी इमारतें कुछ ही मिनटों में ताश के पत्तों की तरह ढह जाती है।  भूमि पर दरार पड़ जाती है। अचानक धरती पर तीव्र गति से कम्पन होती है कि एक ही झटके में सब कुछ नष्ट हो जाता है।  कई परिवार भूकंप की इस भयावह आपदा के शिकार हो जाते है।  हर तरफ  त्र्याही त्र्याही मच जाती है। भूकंप दो  अक्षरों -भू + कम्प से बना है।  भू मतलब धरती और कम्प का अर्थ है कम्पन। इस प्रकार भूमि  यानी  धरती पर अचानक आये कम्पन को भूकंप कहते है।'''

    print(f'textLength : {len(text)}')
    text = splitTextRandom(text)
    print(f'textLength : {len(text)}')
    print(text)

    