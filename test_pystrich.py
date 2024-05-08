from pystrich.datamatrix import DataMatrixEncoder
from pylibdmtx.pylibdmtx import encode
from ppf.datamatrix import DataMatrix
from PIL import Image
import barcode
FNC1 = "\xf1"
GS1_FNC1_CHAR = u'\xf1'
#FNC1 = "\xe8"
dm = barcode.Gs1_128(GS1_FNC1_CHAR+'0103068320103631215:eIbEKP=s"&P93DK2a')
dm = barcode.Gs1_128('0103068320103631215:eIbEKP=s"&P93DK2a')
dm1 = barcode.Gs1_128('0103068320103631215:eIbEKP=s"&P93DK2a')
#dm.code = f'{GS1_FNC1_CHAR}0103068320103631215:eIbEKP=s"&P93DK2a'
encoder = DataMatrixEncoder(dm.code)
encoder.save("test_pystrich.png" )

encoded = encode(f'{GS1_FNC1_CHAR}0103068320103631215:eIbEKP=s"&P93DK2a')
img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
img.save('test_pylibdmtx_fnc_char.png')

encoded = encode(f'0103068320103631215:eIbEKP=s"&P93DK2a')
img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
img.save('test_pylibdmtx_nofnc.png')


matrix = DataMatrix(dm.code)
#matrix.svg(fg='#FFF',bg='000')
#matrix.save()

