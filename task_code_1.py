import cv2
from matplotlib import pyplot

# Так как OpenCV изначально считывает картинку в формате BRG,
#     то сначала я конвертирую её в RGB, а затем в HSV, как того требует задание

img = cv2.imread('variant-3.jpeg')  # , cv2.IMREAD_GRAYSCALE)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Конвертируем в RGB
img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)  # Конвертируем в HSV

img_res = cv2.resize(img, (200, 200))
pyplot.imshow(img_hsv)
pyplot.show()
