import cv2
import numpy as np

capture = cv2.VideoCapture(0) # Подключаемся к камере (0 — первая доступная)

while True:
    no_errors, frame_color = capture.read() # Считываем один кадр. no_errors - успешно ли считан кадр
    #                                                              frame_color - сам кадр

    if not no_errors:
        print('Error while read!')
        break

    # Преобразование в ч/б и размытие
    frame = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)
    frame = cv2.blur(frame, (15, 15))

    # Бинаризация. Пиксели со значением > 200 становятся белыми (250), остальные — чёрными.
    _, frame = cv2.threshold(frame, 200, 250, cv2.THRESH_BINARY)


    kernel = np.ones((5, 5), np.uint8)
    frame = cv2.dilate(frame, kernel, iterations=16)
    conts, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for i in range(0, len(conts)):
        cv2.drawContours(frame_color, conts, i, (0, 255, 0), 10)
    cv2.imshow('frame', frame_color)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
capture.release()  # Закрываем камеру
cv2.destroyAllWindows()  # Закрываем все окна OpenCV