'''
import numpy as np
import cv2

image = cv2.imread("tmp.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
cv2.imwrite("tmp.png", gray)

# распознаём контуры
edged = cv2.Canny(gray, 10, 250)
cv2.imwrite("edged.jpg", edged)

# создаём и применяем закрытие
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
cv2.imwrite("closed.jpg", closed)

# находим контуры в изображении и подсчитываем число их
cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
total = 0

# выполняем цикл по контурам
for c in cnts:
    # сглаживаем контур
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # если у контура есть четыре вершины, это, скорее всего, код
    if len(approx) == 4:
        cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
        total += 1


# покажем результирующее изображение
print("Я нашёл {0} кодов на этой картинке".format(total))
cv2.imwrite("output.jpg", image)
'''




import sys
import numpy as np
import cv2 as cv

hsv_min = np.array((0, 54, 5), np.uint8)
hsv_max = np.array((187, 255, 253), np.uint8)

if __name__ == '__main__':
    fn = 'tmp.png' # имя файла, который будем анализировать
    img = cv.imread(fn)

    hsv = cv.cvtColor( img, cv.COLOR_BGR2HSV ) # меняем цветовую модель с BGR на HSV
    thresh = cv.inRange( hsv, hsv_min, hsv_max ) # применяем цветовой фильтр
    contours0, hierarchy = cv.findContours( thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    # перебираем все найденные контуры в цикле
    for cnt in contours0:
        rect = cv.minAreaRect(cnt) # пытаемся вписать прямоугольник
        box = cv.boxPoints(rect) # поиск четырех вершин прямоугольника
        box = np.int0(box) # округление координат
        cv.drawContours(img,[box],0,(255,0,0),2) # рисуем прямоугольник

    cv.imshow('contours', img) # вывод обработанного кадра в окно

    cv.waitKey()
    cv.destroyAllWindows()