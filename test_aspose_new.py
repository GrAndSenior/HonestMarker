#!!!!!!!!!!!!!  Платный продукт. В бесплатной версии возвращает только информацию вида (01)04810268050169(21)2mzgp***********
'''
#pip install aspose-barcode-for-python-via-net


from aspose.barcode import barcoderecognition

reader = barcoderecognition.BarCodeReader('d://datamatrix.png')
recognized_results = reader.read_bar_codes()
for barcode in recognized_results:
    print(barcode.code_text)
'''    