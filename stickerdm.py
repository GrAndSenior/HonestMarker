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
from zebra import Zebra
class Stickerdm(Zebra):
    def __init__(self, left, top, orientation, height, quality) -> None:
        super().__init__(self)
        try:
            self.zp = Zebra('Zebra Printer')
            self.queues = self.zp.getqueues()
            self.zp.setqueue(self.queues[0])
            self.LEFT = str(left)
            self.TOP = str(top)
            self.ORIENTATION = orientation
            self.HEIGHT = str(height)
            self.zp.reset()
            if quality.find(' ')>=0:
                self.QUALITY = str(quality.split(' ')[1])
            else:
                self.QUALITY = 0
            self.text = False
            #self.label = f'^XA^CI28^FH^FO{self.LEFT},{self.TOP}^BX{self.ORIENTATION},{self.HEIGHT},{self.QUALITY},,,,\,1 ^FD\\1{code}^FS^XZ'
        except:
            print("Error with the USB connection")
            self.zp = None
    
    def add_picture(self, pic):
        self.label = pic + self.label

    def make_label(self,code):
        if self.text:
            self.label = f'^CI28^FH^FO{self.LEFT},{self.TOP}^BX{self.ORIENTATION},{self.HEIGHT},{self.QUALITY},,,,\,1^FD\\1{code}^FS'
        else: 
            self.label = f'^CI28^FH^FO{self.LEFT},{self.TOP}^BX{self.ORIENTATION},{self.HEIGHT},{self.QUALITY},,,,\,1^FD\\1{code}^FS'
        
        #self.add_picture('')
        
        return self.label

    def set_queue(self,index):
        try:
            self.zp.setqueue(self.queues[index])
            return True
        except:
            return False    

    def print_label(self):
        try:
            if not('^XA' in self.label):
                self.label = '^XA'+self.label
            if not('^XZ' in self.label):
                self.label = self.label + '^XZ'
            self.zp.output(self.label)
            return True
        except:
            return False    