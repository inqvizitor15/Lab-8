import time
import cv2


def video_processing():
    cap = cv2.VideoCapture(0)
    down_points = (640, 480)
    i = 0

    # Определяем центральный квадрат 200x200
    square_size = 200
    center_square = {
        'x1': down_points[0] // 2 - square_size // 2,
        'y1': down_points[1] // 2 - square_size // 2,
        'x2': down_points[0] // 2 + square_size // 2,
        'y2': down_points[1] // 2 + square_size // 2
    }

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)

        # Рисуем центральный квадрат
        cv2.rectangle(frame,
                      (center_square['x1'], center_square['y1']),
                      (center_square['x2'], center_square['y2']),
                      (255, 0, 0), 2)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

        contours, hierarchy = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Вычисляем центр прямоугольника
            center_x = x + w // 2
            center_y = y + h // 2

            # Рисуем центр прямоугольника
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            # Проверяем попадание в центральный квадрат
            if (center_square['x1'] <= center_x <= center_square['x2'] and
                    center_square['y1'] <= center_y <= center_square['y2']):
                cv2.putText(frame, "HIT!", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if i % 5 == 0:
                print(f"Center coordinates: {center_x}, {center_y}")

        cv2.imshow('Crash Test Target Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)
        i += 1

    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_processing()