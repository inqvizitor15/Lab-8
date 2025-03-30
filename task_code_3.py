import numpy as np
import cv2

cap = cv2.VideoCapture(0)

fly_image = cv2.imread("fly64.png", cv2.IMREAD_UNCHANGED)
fly_height, fly_width = fly_image.shape[:2]

while True:
    no_errors, frame = cap.read()
    if not no_errors:
        break

    height, width = frame.shape[:2]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 0)

    # Используем метод для поиска круга
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2,
                               minDist=100, param1=80, param2=40,
                               minRadius=30, maxRadius=250)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        x, y, r = circles[0, 0].astype(int)  # Преобразуем в int

        # Границы мухи с защитой от выхода за пределы кадра
        x1_fl = max(0, x - fly_width // 2)
        x2_fl = min(width, x1_fl + fly_width)
        y1_fl = max(0, y - fly_height // 2)
        y2_fl = min(height, y1_fl + fly_height)

        if x1_fl < x2_fl and y1_fl < y2_fl:  # Проверка на валидность области
            fly_region = frame[y1_fl:y2_fl, x1_fl:x2_fl]

            # Обработка картинки
            if fly_image.shape[2] == 4:  # Проверка наличия альфа-канала
                alpha_ch = fly_image[:, :, 3] / 255.0
                for ch in range(3):
                    fly_region[:, :, ch] = (1 - alpha_ch) * fly_region[:, :, ch] + alpha_ch * fly_image[:, :,
                                                                                              ch]
            else:
                frame[y1_fl:y2_fl, x1_fl:x2_fl] = fly_image

    cv2.imshow('Hindrance', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
