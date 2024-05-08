from treepoem import generate_barcode
from PIL import Image, ImageDraw, ImageFont
from random import randint
from time import time
import re

import pandas as pd
from pathlib import Path

class Gs1datamatix():
    def __init__(self, code, textinclude=False):
        self.gs1dm = code
        self.version = '26x26'
        self.textinclude = textinclude
        self.image = self.generate()
        
    def save(self, fileName):
        folder = Path('d:\\Grand\\Py\\DataMatrix\\test\\')
        if folder.is_dir():
            folder_count = len([1 for file in folder.iterdir()])
        self.image.save( f"test\{folder_count}.png")        
        self.image.save(fileName)

    def show(self):
        self.image.show()

    def generate(self):
        # Generate datamatrix
        datamatrix = generate_barcode(
            barcode_type='datamatrix',
            data=f"^FNC1{self.gs1dm}",
            options={"parsefnc": True, "parse": True, "format": "square", "version": self.version, "includetext": self.textinclude})
        
        # Resize datamatrix to desired size
        dm_size_px = (196, 196)
        datamatrix = datamatrix.resize(dm_size_px, Image.NEAREST)

        # Create white picture  
        picture_size_px = (200, 200)
        picture = Image.new('L', picture_size_px, color='white')

        # Position the datamatrix
        barcode_position_px = (2, 2)
        picture.paste(datamatrix, barcode_position_px)

        # Draw picture for placing texts on it
        draw = ImageDraw.Draw(picture)

        # Store font for the texts
        ocrb_font = ImageFont.truetype("sources/fonts/arialnb.ttf", 12)
        self.image = picture
        # Draw texts on the Picture
        #datamatrix_text_position_px = (10,15)
        #draw.text(datamatrix_text_position_px, "This is a GS1 DataMatrix", fill='black', font=ocrb_font)
        #welcome_text_position_px = (35,180)
        #draw.text(welcome_text_position_px, gs1dm[:gs1dm.find('93')], fill='black', font=ocrb_font)

        # Save the image
        #picture.save("datamatrix.png")
        #picture.show()
        return picture
    def validate(self, tg):
        #    '^[0][1][0-9]{14}[2][1][^]{7}[9][3]\S{4}$',self.gs1dm) - пример валидатора

        if tg == 0 or tg == 10:  #Альтернативная табачная продукция
            return (re.match('\S{29}$',self.gs1dm) is not None) or (re.match('^[0][1][0-9]{14}[2][1][^]{7}[8][0][0][5][^]{6}[9][3]\S{4}$',self.gs1dm) is not None) or (re.match('^[0][1][0-9]{14}[2][1][^]{7}[9][3]\S{4}$',self.gs1dm) is not None)
        elif tg == 1:  #Антисептики и дезинфицирующие средства
            pass
        elif tg == 2:  #Безалкогольное пиво
            pass
        elif tg == 3:  #Биологически активные добавки к пище
            pass
        elif tg == 4:  #Велосипеды и велосипедные рамы
            pass
        elif tg == 5:  #Духи и туалетная вода
            pass
        elif tg == 6:  #Лекарственные препараты для медицинского применения
            pass
        elif tg == 7:  #Медицинские изделия
            pass
        elif tg == 8:  #Молочная продукция
            pass
        elif tg == 9:  #Морепродукты
            pass
        elif tg == 10:  #Никотиносодержащая продукция
            pass
        elif tg == 11:  #Обувные товары
            pass
        elif tg == 12:  #Пиво, напитки, изготавливаемые на основе пива, слабоалкогольные напитки
            return (re.match('^[0][1][0-9]{14}[2][1][^]{7}[9][3]\S{4}$',self.gs1dm) is not None) or (re.match('^[0][1][0-9]{14}[2][1][^]{7}[9][3]\S{4}\S{10}$',self.gs1dm) is not None) or (re.match('^[0][1][0-9]{14}[2][1][^]{13}[9][3]\S{4}$',self.gs1dm) is not None) #- пример валидатора
        elif tg == 13:  #Предметы одежды, бельё постельное, столовое, туалетное и кухонное
            pass
        elif tg == 14:  #Соковая продукция и безалкогольные напитки
            pass
        elif tg == 15:  #Табачная продукция
            pass
        elif tg == 16:  #Товары из натурального меха
            pass
        elif tg == 17:  #Упакованная вода
            pass
        elif tg == 18:  #Фотокамеры (кроме кинокамер), фотовспышки и лампы-вспышки
            pass
        elif tg == 19:  #Шины и покрышки пневматические резиновые новые
            pass
        elif tg == 20:
            pass
        return False

def make_code(code):
    #print(code)
    start = time()
    dm = Gs1datamatix(str(code))
    print(round(time()-start,2))
    #print(dm.image)
    #dm.generate()
    return True

df = pd.DataFrame()
df = pd.read_csv('testdf.csv', sep='\t', encoding='utf-8', names=['gs1dm'])
#gf = df['gs1dm'].apply(make_code) - работает 
dm = Gs1datamatix('010460043993125621JgXJ5.T800511200093Mdlr')
'0100681131699891215mvmtWv93dGVz3351000323'
print(dm.validate(12))
#print(df['gs1dm'])
