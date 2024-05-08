
import aspose.barcode as barcode

# Инициализировать объект класса BarcodeGenerator
generator = barcode.generation.BarcodeGenerator(barcode.generation.EncodeTypes.DATA_MATRIX, "Aspose")

# Сгенерировать штрих-код Datamatrix
generator.save("datamatrix-barcode.png")

#To encode a FNC1 , FNC2 or FNC 3 you can send a F1, F2 or F3  in the data stream of your EPL programming using the "B" command .
#In order to specify subset A, B, or C encode a 1A,  1B, or a 1C in the barcode field as stated in the EPL Programming Manual. 
#https://support.zebra.com/cpws/docs/eltron/epl2/B_Code128_Command.pdf

#Example:

#Subset A using FNC1
#B100,200,0,1A,3,3,144,B,"ABCD"F1"4567"

'''
Global Trade Item Number (GTIN) 	Products and services 	Can of soup, chocolate bar, music album
Global Location Number (GLN) 	Parties and locations 	Companies, warehouses, factories, stores
Serial Shipping Container Code (SSCC) 	Logistics units 	Unit loads on pallets, roll cages, parcels
Global Returnable Asset Identifier (GRAI) 	Returnable assets 	Pallet cases, crates, totes
Global Individual Asset Identifier (GIAI) 	Assets 	Medical, manufacturing, transport and IT equipment
Global Service Relation Number (GSRN) 	Service provider and recipient relationships 	Loyalty scheme members, doctors at a hospital, library members
Global Document Type Identifier (GDTI) 	Documents 	Tax demands, shipment forms, driving licences
Global Identification Number for Consignment (GINC) 	Consignments 	Logistics units transported together in an ocean container
Global Shipment Identification Number (GSIN) 	Shipments 	Logistics units delivered to a customer together
Global Coupon Number (GCN) 	Coupons 	Digital coupons
Component/Part Identifier (CPID) 	Components and parts 	Automobile parts
Global Model Number (GMN) 	product model 	Medical devices
'''

from treepoem import generate_barcode
from PIL import Image

class Dmgs1_parcer():
    def __init__(self,code) -> None:
        import re
        self.gtin = code[2:17]
        self.serial_number = code[19:27]#'2mzgp6C5'
        self.expiry_date = ''#"250731"
        self.batch_number = "DATAMATRIXTEST"
        self.control_code = code[:-4]#'L&V1'


def generate_and_print(gtin, serial_number, expiry_date, batch_number, control_code):
    # Generate datamatrix
    datamatrix = generate_barcode(
        barcode_type='gs1datamatrix',
        #data=f"(01){gtin}(21){serial_number}(17){expiry_date}(10){batch_number}",
        data=f"(01){gtin}(21){serial_number}(93){control_code}",
        options={"parsefnc": True, "format": "square", "version": "26x26"})
    
    # Resize datamatrix to desired size
    dm_size_px = (120, 120)
    datamatrix = datamatrix.resize(dm_size_px, Image.NEAREST)

    # Create white picture
    picture_size_px = (140, 140)
    picture = Image.new('L', picture_size_px, color='white')

    # Position the datamatrix
    barcode_position_px = (10, 10)
    picture.paste(datamatrix, barcode_position_px)

    # Save the image
    picture.save("d://datamatrix.png")
    #picture.show()


gtin = "04810268050169"
serial_number = '2mzgp6C5'
expiry_date = "250731"
batch_number = "DATAMATRIXTEST"
control_code = '1234'

generate_and_print(gtin, serial_number, expiry_date, batch_number,control_code)
import csv


FNC1 = ''
#FNC1 = b'\x1D'
LEFT = '20'
TOP = '20'
ORIENTATION = ''
HEIGHT = '6'
QUALITY = '200'
GS = ''
#DM = '0105200120690210215mk.3UOWO%knt93VgDi'
#DM = '0104810268050169212mzgp6C593L&V1'
DM_GS = '0104810268050169212mzgp6C593L&V1'
DM = '0105411858000077215"?m3sa932GuU'

#DM = '0104607974050152215uAPW&v93EI3H'
if not '' in DM:
    tmp_str = list(DM)
    tmp_str.insert(26, '')
    DM = ''.join(tmp_str)
    #print(DM)


#l1 =f'^XA^CI28^FH^FO{LEFT},{TOP}^BXN,{HEIGHT},{QUALITY},,,,{FNC1},1 ^FD{FNC1}{DM[:31]}{GS}{DM[31:]}^FS^XZ'
#l1 =f'^XA^CI28^FH^FO{LEFT},{TOP}^BXN,{HEIGHT},{QUALITY},,,,\,1 ^FD{FNC1}{DM[:26]}{GS}{DM[26:]}^FS^XZ'
#l1 =f'^XA^CI28^FH^FO{LEFT},{TOP}^BXN,{HEIGHT},{QUALITY},,,,\,1 ^FD{DM[:26]}{GS}{DM[26:]}^FS^XZ'

#l1 = f'^XA^CI28^FH^FO{LEFT},{TOP}^BXN,{HEIGHT},{QUALITY},,,,{GS},1 ^FD\\1{DM[:26]}{GS}{DM[26:]}^FS^XZ'
l1 = f'^XA^CI28^FH^FO{LEFT},{TOP}^BXN,{HEIGHT},{QUALITY},,,,\,1 ^FD\\1{DM_GS}^FS^XZ'
#Ok l2 =f'^XA^CI28^FH^FO{LEFT},{TOP}^BXN,{HEIGHT},{QUALITY},,,,,1 ^FD{DM[:26]}{GS}{DM[26:]}^FS^XZ'
l2 = f'^XA^CI28^FH^FO{LEFT},{TOP}^BXN,{HEIGHT},{QUALITY},,,,\,1 ^FD\\1{DM}^FS^XZ'

l2_1 =f'^XA^CI28^FH^FO{LEFT},{TOP}^BXN,{HEIGHT},{QUALITY},,,,\\,1 ^FD\\1{DM[:31]}{DM[31:]}^FS^XZ'
label = '''^XA^CI28^FH^CFT,5,10^FO90,180^FD037^FS^FO60,60^BXN,5,200,,,,,1^0105200120690135215!;Ofnp-,A=RP^FS^XZ''' 
label = label+chr(29)+f'''DM[31:]^FS^XZ'''


#--Вывод на печать DataMarix на Zebra
#^BX orientation, height, quality, columns, rows, format, escape, ratio
#Configures the current field as a Data Matrix bar code.
#Parameters:

#    orientation: The bar code orientation to use. Valid values are N (no rotation), R (rotate 90° clockwise), I (rotate 180° clockwise), and B (rotate 270° clockwise). The default value is the orientation configured via the ^FW command, which itself defaults to N (no rotation).
#    height: The bar code element height, in dots. The individual elements are square, so the element height and width will be the same. Any number between 1 and the label width may be used. The default value is the element height necessary for the total bar code height to match the bar code height configured via the ^BY command.
#    quality: The level of error correction to apply. Valid values are 0 (ECC 0), 50 (ECC 50), 80 (ECC 80), 100 (ECC 100), 140 (ECC 140) and 200 (ECC 200). The default value is 0 (scan errors are detected but not corrected). Always use quality level 200 (ECC 200).
#    columns: The number of columns to encode. For ECC 200 bar codes, even numbers between 1 and 144 may be used. This parameter can be used to control the bar code width. The default value depends on the amount of data encoded.
#    rows: The number of rows to encode. For ECC 200 bar codes, even numbers between 1 and 144 may be used. This parameter can be used to control the bar code height. The default value depends on the amount of data encoded.
#    format: The type of data that needs to be encoded. Valid values are 1, 2, 3, 4, 5 and 6. The default value is 6. This parameter is ignored for ECC 200 bar codes (the recommended quality level).
#    escape: The escape character used to escape control sequences in the field data. The default value is "~" (tilde).
#    ratio: The desired aspect ratio, if any. Valid values are 1 (square) and 2 (rectangular).

#Example (common usage): ^BX,5,200
#Example (full usage): ^BXN,5,200,22,22,,~,1

import socket              
mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         
host = "10.144.3.106" 
port = 9100   
'''
try:           
	mysocket.connect((host, port)) #connecting to host
	mysocket.send(b"^XA^A0N,50,50^FO50,50^FDSocket Test^FS^XZ")#using bytes
	mysocket.close () #closing connection
except:
	print("Error with the network connection")
'''
from zebra import Zebra

try:
    zp = Zebra('Zebra Printer')
    #print(zp.getqueues())

    queue = zp.getqueues()[0]
    zp.setqueue(queue)
except:
	print("Error with the USB connection")
#for i in range(10):
#zp.output(label)
#zp.output(l1)
zp.output(l2)

#z.print_config_label()
#z.output(label)


worklabel='''
^XA 
^CI28
^FH
^CFP,5,10 ^FO560,310 ^FH^FD04630162491475^FS
^CFP,5,10 ^FO560,330 ^FH^FD5aWoWlascYnb8^FS
^FO 45,270 ^BY4 ^BEN,60,Y,N  ^FD2000016664232^FS 
			
^FO10,10 ^BXN,4,200,,,,\,1 
^FD01046201432695992153S*_aNUvldo=^FS
^XZ
'''