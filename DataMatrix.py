from treepoem import generate_barcode
from PyQt5.QtGui import QPixmap
from PIL import Image
#from PIL.ImageQt import ImageQt # для перевода графики из Pillow в Qt
GS = ''
FNC1 = b'\x1d'

class Datamatrix():
    def __init__(self,code):#,goods):
        #self.image = None
        self.control = 'Ok'
        self.gs1dm = code
        #self.validate(goods)
        self.Kcode = ''
        self.Pcode = '' 
        
    def validate(self,goods):
        self.gtin = self.gs1dm[2:16]
        if goods == 18:
            if self.gs1dm[16:18] == '21':
                self.serial_number = self.gs1dm[18:31]
            else:
                self.control = 'Ошибка!!!'
            if self.gs1dm[31] != GS:
                self.insert_gs(31)
                self.control = 'Исправлен'
            self.expiry_date = ''
            self.batch_number = ''
            if self.gs1dm[-6:-4] == '93' and len(self.gs1dm)>32:
                self.control_code = self.gs1dm[-4:]
            else:
                self.control_code = ''
                self.control = 'Нет ключа проверки!!!'
        
    def insert_gs(self,pos):
        if not(GS in self.gs1dm):
            self.gs1dm = self.gs1dm[:pos]+GS+self.gs1dm[pos:]
        print(self.gs1dm)
'''
    def generate(self):
        # Generate datamatrix
        datamatrix = generate_barcode(
            barcode_type='gs1datamatrix',
            #data=f"(01){gtin}(21){serial_number}(17){expiry_date}(10){batch_number}",
            data=f"(01){self.gtin}(21){self.serial_number}(93){self.control_code}",
            options={"parsefnc": True, "format": "square", "version": "26x26"})
        
        #print(datamatrix.size)
        # Resize datamatrix to desired size
        #dm_size_px = (120, 120)
        #datamatrix = datamatrix.resize((120, 120), Image.NEAREST)
        
        # Create white picture
        picture_size_px = (120, 120)
        picture = Image.new('L', picture_size_px, color='white')
        
        # Position the datamatrix
        barcode_position_px = ((picture_size_px[0]-datamatrix.size[0])//2, (picture_size_px[1]-datamatrix.size[1])//2)
        picture.paste(datamatrix, barcode_position_px)
        picture.save('tmp.png')
        picture = QPixmap('tmp.png')
        #picture.show()
        #self.image = picture
        return picture
'''

label = Datamatrix('0100000075013769215sGfqg893Gtjk')
label.insert_gs(25)