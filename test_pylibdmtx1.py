from pylibdmtx.pylibdmtx import encode, decode, dmtxEncodeDataMatrix
from pystrich.datamatrix import DataMatrixEncoder
from PIL import Image
#FNC1 = chr(29)
#FNC1 = FNC1.encode("acsii")
#FNC1 = bytes.fromhex("d2")

'''
for i in range(1):
    #FNC1 = chr(i)
    #FNC1 = bytes.fromhex("E8")
    encoded = encode('^FNC1105411858000138215!"Qk6!93cQ3y',size='22x22')
    #print( encode('0105411858000138215!"Qk6!93cQ3y')._fields[3].title())
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    img.show()
#print(decode(Image.open('dmtx.png')))
#[Decoded(data=b'hello world', rect=Rect(left=9, top=10, width=80, height=79))]

'''
import treepoem
from time import time
start = time()
GS1 = ''
image = treepoem.generate_barcode(
    barcode_type="gs1datamatrix",  # One of the BWIPP supported codes.
    data='(01)05411858000138(21)5!"Qk6!{GS}(93)cQ3y', 
    options={"parse": True, "format": "square", "version": "22x22", "includetext": False}
)
image.convert("1").save("barcode.png")
print(round(time()-start,2))
image.show()
