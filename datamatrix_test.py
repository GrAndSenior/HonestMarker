'''import treepoem 
image = treepoem.generate_barcode(
    barcode_type='datamatrix',  # One of the supported codes.
    data='barcode payload', 
) 
image.convert('1').save('barcode.png')'''

'''
---- Коннектор к базе данных MySQL

import mysql.connector as connection
import pandas as pd
try:
    mydb = connection.connect(host="localhost", database = 'Marking',user="root", passwd="btsroot",use_pure=True)
    query = "Select * from Markerdetails;"
    result_dataFrame = pd.read_sql(query,mydb)
    mydb.close() #close the connection
except Exception as e:
    mydb.close()
    print(str(e))

#---- Коннектор к базе данных MySQL - !!!Конец фрагмента
'''





#'''+++++++++++++++ Кодирование текста в DataMatrix-картинку с масштабированием
TIMER = 5    # пауза между блоками этикеток
COROB = 24   # количество единиц товара в коробе
PALLET = 50  # количество коробов на палете

import treepoem 
from PIL import Image, ImageDraw, ImageFont, ImageWin
from time import sleep
import win32print
import win32ui
import pandas as pd
import mainwin


def print_sticker_corob():
    print('*'*10,'COROB FULL','*'*10)

def print_sticker_pallet():
    print('*'*10,'PALLET FULL','*'*10)

def print_sticker_code(file_name):
    #
    # Constants for GetDeviceCaps
    #
    #
    # HORZRES / VERTRES = printable area
    #
    HORZRES = 8
    VERTRES = 10
    #
    # LOGPIXELS = dots per inch
    #
    LOGPIXELSX = 88
    LOGPIXELSY = 90
    #
    # PHYSICALWIDTH/HEIGHT = total area
    #
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111
    #
    # PHYSICALOFFSETX/Y = left / top margin
    #
    PHYSICALOFFSETX = 112
    PHYSICALOFFSETY = 113

    printer_name = win32print.GetDefaultPrinter ()
    #print(printer_name)
    #file_name = "test.jpg"

    #
    # You can only write a Device-independent bitmap
    #  directly to a Windows device context; therefore
    #  we need (for ease) to use the Python Imaging
    #  Library to manipulate the image.
    #
    # Create a device context from a named printer
    #  and assess the printable size of the paper.
    #
    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC (printer_name)
    printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
    printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
    printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)

    #
    # Open the image, rotate it if it's wider than
    #  it is high, and work out how much to multiply
    #  each pixel by to get it as big as possible on
    #  the page without distorting.
    #
    bmp = Image.open (file_name)
    if bmp.size[0] > bmp.size[1]:
        bmp = bmp.rotate (90)

    ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
    scale = min (ratios)

    #
    # Start the print job, and draw the bitmap to
    #  the printer device at the scaled size.
    #
    hDC.StartDoc (file_name)
    hDC.StartPage ()

    dib = ImageWin.Dib (bmp)
    scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
    x1 = int ((printer_size[0] - scaled_width) / 2)
    y1 = int ((printer_size[1] - scaled_height) / 2)
    x2 = x1 + scaled_width
    y2 = y1 + scaled_height
    dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))

    hDC.EndPage ()
    hDC.EndDoc ()
    hDC.DeleteDC ()

'''-----------Импорт построчно только кодов
with open('code.csv','r') as codefile:
    codes = codefile.readlines()
'''

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QWidget()
#mywindow.resize(250, 150)

MainWindow.setObjectName("MainWindow")
MainWindow.resize(816, 765)
centralwidget = QtWidgets.QWidget(MainWindow)
centralwidget.setObjectName("centralwidget")
cbCols = QtWidgets.QComboBox(centralwidget)
cbCols.setGeometry(QtCore.QRect(30, 60, 341, 22))
cbCols.setObjectName("cbCols")
h1 = QtWidgets.QHBoxLayout()
h1.addWidget(cbCols)
MainWindow.setLayout(h1)






#df = pd.read_csv('tmp.csv', delimiter=',', names = ["requestedCis","gtin","tnVedEaes","tnVedEaesGroup","maxRetailPrice","parent","producerInn","ownerInn","prVetDocument","productName","brand","ownerName","producerName","introducedDate","receiptDate","status","statusEx","emissionType","withdrawReason","packageType","productGroup","applicationDate","emissionDate","expirationDate","child","setGtin","setDescription","productionDate","aggregationType"])
df = pd.read_csv('tmp.csv', delimiter=',')
df.fillna('',inplace=True)

#cbCols.addItems(['1','2'])
#MainWindow.show()
print(pd.pivot_table(df,index=['gtin'],columns='receiptDate',aggfunc=len))
'''+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
codes = list(df['requestedCis'])[1:]
corob=''
count = 0    
font1 = ImageFont.truetype('sources/fonts/Roboto-Bold.ttf', size=20)
font2 = ImageFont.truetype('sources/fonts/arialbd.ttf', size=14)    
for code in codes:
    #print('code/'+str(count).zfill(len(str(len(codes))))+'.png', code[:-1])
    print(code[:-1])      # если считывали только коды построчно
    corob = corob+'\n'+code
    if count % COROB == 0 and count > 0:
        print_sticker_corob()
        sleep(TIMER)
    
    if count % PALLET*COROB == 0 and count > 0:
        print_sticker_pallet()
        sleep(2*TIMER)

    image = treepoem.generate_barcode(
            barcode_type='datamatrix',  # One of the supported codes.
            data=code,
            scale=3,                    # Zoom  1 - 40x40
                                        #       2 - 79x79
                                        #       3 - 119x119  
                                        #       4 - 159x159
                                        #       5 - 199x199
                                        #       6 - 238x238
            ) 
    
    image.convert('1').save('tmp.png')
    imcode = Image.open('tmp.png')
    #imcode = Image.open('tmp.png').resize((150, 150))

    back = Image.open('small.png')
    #draw_text = ImageDraw.Draw(back)

    #draw_text.text((605,250),code[:19],fill='black',font=font2)
    #draw_text.text((635,270),code[20:],fill='black',font=font2)
    
    #draw_text.text((145,333),'12 мес.',fill='black',font=font1)
    #draw_text.text((365,333),'05.09.2023',fill='black',font=font1)
    #draw_text.text((625,333),'04.09.2024',fill='black',font=font1)
    
    back.paste(imcode, (30, 30))
    #back.show()             #для отладки...
    back.save('code/'+str(count).zfill(len(str(len(codes))))+'.png', quality=100)
    #print(f'Изображение {count} из {len(codes)}')
    
    # Печать стикера (на принтер по умолчанию)
    #print_sticker_code('code/'+str(count).zfill(len(str(len(codes))))+'.png')
    
    
    count += 1    

'''

#sys.exit(app.exec_())


'''+++++++++++++++ Кодирование текста в DataMatrix-картинку
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
from pystrich.datamatrix import DataMatrixEncoder
with open('code.csv','r') as codefile:
    codes = codefile.readlines()
n = 0    


for code in codes:
    back = Image.open('back.png')
    encoder = DataMatrixEncoder(code)
    encoder.save('tmp.png')
    imcode = Image.open('tmp.png').resize((150, 150))

    back.paste(imcode, (620, 50))
    back.save('code/'+str(n)+'.png', quality=100)
    n += 1    
'''


'''+++++++++++++++ Декодирование из DataMatrix-картинки в текст 
import numpy as np
import cv2
from pylibdmtx import pylibdmtx

image = cv2.imread('0.png', cv2.IMREAD_UNCHANGED);
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
msg = pylibdmtx.decode(thresh)
print(msg)
'''




#encoder = DataMatrixEncoder("This is a DataMatrix.")
#encoder.save( "datamatrix_test.png" )
#print(encoder.get_ascii())