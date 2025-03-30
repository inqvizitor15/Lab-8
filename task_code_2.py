import cv2
import numpy as np

capture = cv2.VideoCapture(0)  # Подключаемся к камере (0 — первая доступная)

down_points = (640, 480)

# Определяем квадрат 200x200
square_size = 200
center_square = {
    'x1': down_points[0] // 2 - square_size // 2,
    'y1': down_points[1] // 2 - square_size // 2,
    'x2': down_points[0] // 2 + square_size // 2,
    'y2': down_points[1] // 2 + square_size // 2
}

while True:
    no_errors, frame_color = capture.read()  # Считываем один кадр. no_errors - успешно ли считан кадр
    #  frame_color - сам кадр
    frame_color = cv2.flip(frame_color, 1)  # Зеркальное отображение изображения
    frame_color = cv2.resize(frame_color, down_points, interpolation=cv2.INTER_LINEAR)

    if not no_errors:
        print('Error while read!')
        break

    # Преобразование в ч/б
    frame = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)  # Размытие. (5, 5) - размер матрицы,
    # которая будет "скользить" по изображению и накладывать размытие

    # Бинаризация. Пиксели со значением > 200 становятся белыми (250), остальные — чёрными.
    _, frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY + +cv2.THRESH_OTSU)

    # Морфологическое расширение
    kernel = np.ones((3, 3), np.uint8)
    frame = cv2.dilate(frame, kernel, iterations=5)

    # Используем метод для поиска круга
    circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, dp=1.2,
                               minDist=100, param1=80, param2=40,
                               minRadius=30, maxRadius=250)

    # Определяем цвет центрального прямоугольника.
    square_color = (255, 0, 0)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        x_c, y_c, r = circles[0, 0]
        # print(f"Координаты центра: ({x_c}, {y_c})") Отладка
        if (center_square['x1'] <= x_c <= center_square['x2']) and \
                (center_square['y1'] <= y_c <= center_square['y2']):
            square_color = (0, 255, 0)

    # Рисуем центральный квадрат
    cv2.rectangle(frame_color,
                  (center_square['x1'], center_square['y1']),
                  (center_square['x2'], center_square['y2']),
                  square_color, 2)

    # cv2.imshow('frame', frame)
    cv2.imshow('frame_color', frame_color)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

capture.release()  # Закрываем камеру
cv2.destroyAllWindows()  # Закрываем все окна OpenCV
