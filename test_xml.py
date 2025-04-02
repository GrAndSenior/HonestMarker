from xml.etree import ElementTree 
from datetime import datetime


pallets = [f'pallet{_}' for _ in range(3)]
boxnumbers = [f'box{str(_).zfill(2)}' for _ in range(30)]
amcs = [f'item{str(_).zfill(3)}' for _ in range(180)]

class XmlReport():
    def __init__(self):
        self.root = ElementTree.Element('Documents')
        self.document = ElementTree.Element('Document', xmlxsi="http://www.w3.org/2001/XMLSchema-instance", Version="1")
        self.invoice_aggregation = ElementTree.Element('Invoice_aggregation')
        self.header = ElementTree.Element('Header')
        self.version = ElementTree.Element('Version')
        self.invioceNumber = ElementTree.Element('InvoiceNumber')
        self.invoiceDate = ElementTree.Element('InvoiceDate')
        self.content = ElementTree.Element('Content')
        self.palettequantity = ElementTree.Element('PaletteQuantity')
        self.boxquantity = ElementTree.Element('BoxQuantity')
        self.unitquantity = ElementTree.Element('UnitQuantity')
        self.weight = ElementTree.Element('Weight')
        self.sku = ElementTree.Element('SKU')
        self.position = ElementTree.Element('Position')
        self.identity = ElementTree.Element('Identity')
        self.fullname = ElementTree.Element('FullName')
        self.ean = ElementTree.Element('EAN')
        self.boxcapacity = ElementTree.Element('BoxCapacity')
        self.quantity = ElementTree.Element('Quantity')
        self.markinfo = ElementTree.Element('MarkInfo')

    def indent(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

   
    def make_report(self, pallets=[], boxnumbers=[], amcs=[]):

        self.version.text = "1"
        now = datetime.now() # current date and time
        self.invoiceDate.text = now.strftime("%Y-%d-%m")
        self.header.append(self.version)
        self.header.append(self.invioceNumber)
        self.header.append(self.invoiceDate)

        self.palettequantity.text = str(1)
        self.boxquantity.text = str(10)
        self.unitquantity.text = str(60)
        self.weight.text = str(0)
        self.sku.text = str(1)


        self.identity.text = str(1)
        self.fullname.text = ""
        self.ean.text = str(0)
        self.boxcapacity.text = str(6)
        self.quantity.text = str(len(amcs))

        self.position.append(self.identity)
        self.position.append(self.fullname)
        self.position.append(self.ean)
        self.position.append(self.boxcapacity)
        self.position.append(self.quantity)



        for p in range(len(pallets)):
            palletpos = ElementTree.Element('PalletPos')
            palletnum = ElementTree.Element('PalletNum')
            bottlingdate = ElementTree.Element('BottlingDate')
            boxpos = ElementTree.Element('BoxPos')
            palletnum.text = pallets[p]
            bottlingdate.text = now.strftime("%Y-%d-%m")
            palletpos.append(palletnum)
            palletpos.append(bottlingdate)
            for b in range(10):
                boxnumber = ElementTree.Element('boxnumber')
                boxnumber.text = boxnumbers[p*10+b]
                boxpos.append(boxnumber)
                amclist = ElementTree.Element('amclist')
                for i in range(6):
                    amc = ElementTree.Element('amc')
                    amc.text = amcs[p*10*6 + b*6 + i]
                    amclist.append(amc)
                boxpos.append(amclist)    

            palletpos.append(boxpos)
            self.markinfo.append(palletpos)

        self.position.append(self.markinfo)

        self.content.append(self.palettequantity)
        self.content.append(self.boxquantity)
        self.content.append(self.unitquantity)
        self.content.append(self.weight)
        self.content.append(self.sku)
        self.content.append(self.position)


        self.invoice_aggregation.append(self.header)
        self.invoice_aggregation.append(self.content)

        self.document.append(self.invoice_aggregation)
        self.root.append(self.document)


        self.indent(self.root)
        etree = ElementTree.ElementTree(self.root)
        myfile = open("sample1.xml" , "wb")
        etree.write(myfile, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    XmlReport().make_report(pallets, boxnumbers, amcs)