#pip3 install opencv-python qrcode pyzbar numpy

#from pyzbar import pyzbar
import cv2
from pylibdmtx.pylibdmtx import decode as dm_decode
from PIL import Image

#^(?=.*01(\d{14}))(?=.*10([a-zA-Z0-9]{1,20}))(? =.*17(\d{6}))(?=.*21([a-zA-Z0-9]{1,20})).*$

'''
Функция decode() принимает изображение в виде массива numpy и использует pyzbar.decode(), 
который отвечает за декодирование всех штрих-кодов из одного изображения и возвращает 
кучу полезной информации о каждом обнаруженном штрих-коде.'''
def decode(image):
    # decodes all barcodes from an image
    decoded_objects = dm_decode(image)
    for obj in decoded_objects:
        # draw the barcode
        #print(f"Обнаружен штрих-код:\n{obj}")
        #image = draw_barcode(obj, image)
        # print barcode type & data
        ##print("Тип:", obj.type)
        #print("Данные:", obj.data)
        print()
    return image


'''
Эта функция берет декодированный объект, который мы только что видели, и само изображение, 
она рисует прямоугольник вокруг штрих-кода с помощью функции cv2.rectangle(), или  можно раскомментировать другую версию функции;
рисование многоугольника с помощью функции cv2.line().
Он возвращает изображение, содержащее нарисованные штрих-коды.
'''
def draw_barcode(decoded, image):
    # n_points = len(decoded.polygon)
    # for i in range(n_points):
    #     image = cv2.line(image, decoded.polygon[i], decoded.polygon[(i+1) % n_points], color=(0, 255, 0), thickness=5)
    # раскомментируйте выше и закомментируйте ниже, если хотите нарисовать многоугольник, а не прямоугольник
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top), 
                            (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                            color=(0, 255, 0),
                            thickness=5)
    return image

if __name__ == "__main__":
    from glob import glob
    barcodes = glob("d://dmcodes.png")

    for barcode_file in barcodes:
        # загружаем изображение в opencv
        img = Image.open(barcode_file)
        
        print(decode(img))


        #img = cv2.imread(barcode_file)
        # декодировать обнаруженные штрих-коды и получить изображение
        # нарисованный
        #img = decode(img)
        # показать изображение
        img.show()

        #cv2.imshow("img", img)
        #cv2.waitKey(0)
