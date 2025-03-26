import time
import cv2


def video_processing():
    cap = cv2.VideoCapture(0)
    down_points = (640, 480)
    i = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2
        roi_size = 100  # Половина размера 200x200, то есть 100

        # Определяем границы центральной области 200x200
        x1, y1 = center_x - roi_size, center_y - roi_size
        x2, y2 = center_x + roi_size, center_y + roi_size

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        marker_detected = False
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if i % 5 == 0:
                a = x + (w // 2)
                b = y + (h // 2)
                print(a, b)

                # Проверяем, находится ли центр метки в зоне 200x200 пикселей
                if x1 <= a <= x2 and y1 <= b <= y2:
                    marker_detected = True

        # Рисуем центральный квадрат 200x200
        color = (0, 255, 0) if marker_detected else (0, 0, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)
        i += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_processing()
