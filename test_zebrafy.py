from zebrafy import ZebrafyImage, ZebrafyZPL, ZebrafyPDF
from PIL import Image
from zebra import Zebra

pil_image = Image.new(mode="RGB", size=(1770, 1180))
#zpl_string = ZebrafyImage(pil_image).to_zpl()

z = Zebra()
z.setqueue(z.getqueues()[0])
with open("sample.png", "rb") as image:
    zpl_string = ZebrafyImage(
        image.read(),
        format="Z64",
        invert=True,
        dither=False,
        threshold=128,
        width=0,
        height=0,
        pos_x=0,
        pos_y=0,
        rotation=270,
        complete_zpl=True,
    ).to_zpl()
b_code = '''^FO1310,830^BXN,10,200,26,26,,`,1^FD`10103263280117616215Y&XfIxWkYyIL93Gb4M^FS^XZ'''
zpl_string = zpl_string.replace('^XZ', b_code)

#z.output(zpl_string)

ZebrafyZPL(zpl_string).to_images()[0].save('test.png', 'PNG')


with open("sample.zpl", "w") as zpl:
    
    zpl.write(zpl_string)
    pil_images = ZebrafyZPL(zpl_string).to_images()
    for count, pil_image in enumerate(pil_images):

        pil_image.save(f"output_{count}.png", "PNG")