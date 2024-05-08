from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
from pystrich.datamatrix import DataMatrixEncoder


import treepoem 
from PIL import Image, ImageDraw, ImageFont, ImageWin
from time import sleep
import win32print
import win32ui
import pandas as pd


#with open('code.csv','r') as codefile:
#    codes = codefile.readlines()
codes = ['01052001206901972157BwYbgB*Lfp(938WrH',
'0105200120690197215*j"fJGg(%pN&93qnEs',
'0105200120690197215a=iJmoAhcPrd931BQM',
'0105200120690197215G:dnzbI<dNL&930EHZ',
'0105200120690197215-&bPN2Ap?G_g93PIqa',
'0105200120690197215WGJ,nJ>9/9W993Qq9e',
'0105200120690197215kqj5!ohmepVw932b/8',
'0105200120690197215jD_Ezo0iiMRD93gRBC',
'0105200120690197215i"j/Uhht7Nra93xYrn',
'01052001206901972159-_pMxT<PBRW93PLbJ']
n = 0    





corob=''
count = 0    
font1 = ImageFont.truetype('sources/fonts/Roboto-Bold.ttf', size=20)
font2 = ImageFont.truetype('sources/fonts/arialbd.ttf', size=14)    
back = Image.open('1015.png')


image = treepoem.generate_barcode(barcode_type='datamatrix',data=codes[0],scale=1,) 
image.convert('1').save('tmp.png')
imcode = Image.open('tmp.png')
back.paste(imcode, (80, 50))

image = treepoem.generate_barcode(barcode_type='datamatrix',data=codes[1],scale=2,) 
image.convert('1').save('tmp.png')
imcode = Image.open('tmp.png')
back.paste(imcode, (150, 50))

image = treepoem.generate_barcode(barcode_type='datamatrix',data=codes[2],scale=3,) 
image.convert('1').save('tmp.png')
imcode = Image.open('tmp.png')
back.paste(imcode, (270, 50))

image = treepoem.generate_barcode(barcode_type='datamatrix',data=codes[3],scale=4,) 
image.convert('1').save('tmp.png')
imcode = Image.open('tmp.png')
back.paste(imcode, (430, 50))

image = treepoem.generate_barcode(barcode_type='datamatrix',data=codes[4],scale=5,) 
image.convert('1').save('tmp.png')
imcode = Image.open('tmp.png')
back.paste(imcode, (650, 50))

image = treepoem.generate_barcode(barcode_type='datamatrix',data=codes[5],scale=6,) 
image.convert('1').save('tmp.png')
imcode = Image.open('tmp.png')
back.paste(imcode, (900, 50))

image = treepoem.generate_barcode(barcode_type='datamatrix',data=codes[6],scale=7,) 
image.convert('1').save('tmp.png')
imcode = Image.open('tmp.png')
back.paste(imcode, (1200, 50))

image = treepoem.generate_barcode(barcode_type='datamatrix',data=codes[7],scale=8,) 
image.convert('1').save('tmp.png')
imcode = Image.open('tmp.png')
back.paste(imcode, (100, 550))

image = treepoem.generate_barcode(barcode_type='datamatrix',data=codes[8],scale=9,) 
image.convert('1').save('tmp.png')
imcode = Image.open('tmp.png')
back.paste(imcode, (550, 550))

image = treepoem.generate_barcode(barcode_type='datamatrix',data=codes[9],scale=10,) 
image.convert('1').save('tmp.png')
imcode = Image.open('tmp.png')
back.paste(imcode, (1050, 550))





back.save('code/'+str(count).zfill(len(str(len(codes))))+'.png', quality=100)
# Zoom  1 - 40x40
#       2 - 79x79
#       3 - 119x119  
#       4 - 159x159
#       5 - 199x199
#       6 - 238x238
