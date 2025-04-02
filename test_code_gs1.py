import barcode
#from cairosvg import svg2png
GS1_FNC1_CHAR = u'\xf1'
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PyQt5.QtSvg import *
from time import time

code = u'0105411858000138215!"Qk6!93cQ3y'

start = time()
code_128_creator = barcode.get_barcode_class("Gs1_128")
gs1_128_code = code_128_creator(GS1_FNC1_CHAR + code)
code = gs1_128_code.render()
print(time()-start)
print(code.replase('\r\n',''))
#svg2png(bytestring=code,write_to='output.png')

