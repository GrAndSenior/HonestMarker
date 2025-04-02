# Необходимо наличие устанвленного poppler

import cv2
import numpy as np
from pdf2image import convert_from_path


pages = convert_from_path('d:/dm/103336_gtin_08410660053902_quantity_23760.pdf')
image_of_pdf = np.concatenate(tuple(convert_from_path('d:/dm/103336_gtin_08410660053902_quantity_23760.pdf')), axis=0)

cv2.imshow("Image of PDF", image_of_pdf)
cv2.waitKey(0)