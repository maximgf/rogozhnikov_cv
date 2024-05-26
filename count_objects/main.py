import cv2
import zmq
import numpy as np

# Создание окон для отображения изображений
cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)

# Инициализация ZeroMQ контекста и сокета
context = zmq.Context()
socket = context.socket(zmq.SUB)
# Настройка сокета на подписку на все темы
socket.setsockopt(zmq.SUBSCRIBE, b"")
# Установка порта для подключения
port = 5055
socket.connect(f"tcp://192.168.0.113:{port}")

# Счетчик для отслеживания количества полученных изображений
n = 0

# Бесконечный цикл для обработки изображений
while True:
    # Получение данных из сокета
    bts = socket.recv()
    n += 1
    # Преобразование полученных данных в массив numpy
    arr = np.frombuffer(bts, np.uint8)
    # Декодирование массива в изображение
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    # Преобразование изображения в HSV цветовое пространство
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Применение порогового значения для создания маски
    _, thresh = cv2.threshold(hsv[:, :, 1], 70, 255, cv2.THRESH_BINARY)
    # Вычисление карты расстояний
    distance_map = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    # Применение порогового значения к карте расстояний
    ret, dist_tresh = cv2.threshold(
        distance_map, 0.6 * np.max(distance_map), 255, cv2.THRESH_BINARY
    )

    # Вычитание двух масок для получения путаницы
    confuse = cv2.subtract(thresh, dist_tresh.astype("uint8"))
    # Определение связанных компонентов в маске
    ret, markers = cv2.connectedComponents(dist_tresh.astype("uint8"))
    markers += 1
    # Обнуление маркеров в областях путаницы
    markers[confuse == 255] = 0

    # Применение алгоритма watershed для сегментации изображения
    segments = cv2.watershed(image, markers)
    # Поиск контуров на изображении
    cnts, hierrachy = cv2.findContours(
        segments, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )

    # Счетчики для кругов и прямоугольников
    n_circ = 0
    n_rect = 0
    # Обработка каждого контура
    for i in range(len(cnts)):
        if hierrachy[0][i][3] == -1:
            rect = cv2.minAreaRect(cnts[i])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            width, height = rect[1]
            # Подсчет кругов и прямоугольников
            if abs(width - height) < 10:
                n_circ += 1
            else:
                n_rect += 1
            # Рисование контура на изображении
            cv2.drawContours(image, [box], 0, (0, 255, 0), 10)

    # Вывод количества кругов и прямоугольников на изображение
    cv2.putText(
        image,
        f"Circles: {n_circ}",
        (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 255),
        2,
    )
    cv2.putText(
        image,
        f"Rects: {n_rect}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 255),
        2,
    )

    # Ожидание нажатия клавиши
    key = cv2.waitKey(10)
    if key == ord("q"):
        break

    # Отображение изображений в окнах
    cv2.imshow("Image", image)
    cv2.imshow("Mask", confuse)

# Закрытие всех окон
cv2.destroyAllWindows()