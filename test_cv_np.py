from time import time
import numpy as np
import os
import fitz
import cv2
import matplotlib.pyplot as plt
from pylibdmtx.pylibdmtx import decode
import itertools
from PIL import Image


def dm_decode(image, point, size):
    try:
        code_img = image[point[0]-5:point[0]+size[1]+5, point[1]-5: point[1]+size[0]+5].copy()
        return bytes.decode(decode(code_img)[0].data)
    except: 
        return False

def prescan(pdf_filename):
    pdfIn = fitz.open(pdf_filename)
    #for page_number, page in enumerate(pdfIn):
    page = pdfIn[0]

    for zoom in range(1,9):
        # Получить PixMap из страницы PDF файла и преобразовать в NumPy Array без промежуточного сохранения
        img = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        img = np.array(Image.frombytes("RGB", [img.width, img.height], img.samples))

        # Повысить контрастность полученного изображения
        clahe = cv2.createCLAHE(clipLimit=5., tileGridSize=(8,8))          # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        #lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
        lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)  # convert from BGR to LAB color space
        l, a, b = cv2.split(lab)  # split on 3 different channels
        l2 = clahe.apply(l)  # apply CLAHE to the L-channel
        lab = cv2.merge((l2,a,b))  # merge channels
        img = cv2.cvtColor(cv2.cvtColor(lab, cv2.COLOR_LAB2BGR), cv2.COLOR_BGR2GRAY)  # convert from LAB to BGR, а затем в GRAY

        # Получаем номера столбцов и строк, в которых есть полезная информация
        bool_arr = ( img != 255)
        cols, rows = np.sum(bool_arr, axis=(0)), np.sum(bool_arr, axis=(1))
        cols, rows = np.where(cols > 0, 1, 0),  np.where(rows > 0, 1, 0)

        # Получаем размер кода в пикселях
        maxima_so_far = {}
        for t, group in itertools.groupby(cols):
            group_length = sum(1 for _ in group)
            if group_length > maxima_so_far.get(t, 0):
                maxima_so_far[t] = group_length
        size = (maxima_so_far[1],  maxima_so_far[1])

        # Определяем координаты углов изображения кода
        cols, rows = cols.nonzero()[0], rows.nonzero()[0]
        x, y = [cols[0]], [rows[0]]
        # Получаем два вектора: номера столбцов и строк с полезной информацией
        for i in range(1, len(cols)-1):
            if cols[i] - cols[i-1] > 1:
                x.append(cols[i])

        for i in range(1, len(cols)-1):
            if rows[i] - rows[i-1] > 1:
                y.append(rows[i])
        matrix = (len(x), len(y))   # Размерность таблицы кодов на странице
        
        # Получаем список координат левого верхнего угла всех кодов на странице
        img_codes = []
        for row in y:
            for col in x:
                img_codes.append((row, col))

    
        # Пытаемся распознать код
        try:
            # Выбираем первый код для предварительного просмотра и проверки распознавания 
            if dm_decode(img, img_codes[0], size): break
        except:
            # При неудачной попытке увеличиваем масштаб
            continue

    return (zoom, zoom), matrix, size

if __name__ == "__main__":
    filename = 'd:/dm/103336_gtin_08410660053902_quantity_23760.pdf'
    start = time()
    zoom, matrix, size = prescan(filename)

    print(zoom, matrix, size)
    print(time()-start)    
    #zoom = (1, 1)
    #matrix = (13, 13)  # Размерность таблицы кодов на странице (строк-стоблцов)
    #size = (168, 247)  #
