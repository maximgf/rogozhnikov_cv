import cv2
import numpy as np

# Инициализация видеопотока с камеры
cap = cv2.VideoCapture(0)

while True:
    # Чтение кадра из видеопотока
    img = cap.read()[1]
    orig = img.copy()

    # Преобразование изображения в оттенки серого
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Применение гауссова размытия для уменьшения шума
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Применение пороговой обработки для бинаризации изображения
    _, thres = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)

    # Поиск контуров на бинаризованном изображении
    cts, _ = cv2.findContours(thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Выбор самого большого контура
    contour = max(cts, key=cv2.contourArea)

    # Приближение контура с помощью алгоритма Дуке
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    if len(approx) == 4:
        # Изменение формы контура для удобства работы
        pts = approx.reshape(4, 2)

        # Инициализация массива для хранения вершин прямоугольника
        rect = np.zeros((4, 2), dtype="float32")
        # Определение вершин прямоугольника
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        # Вычисление ширины и высоты прямоугольника
        (tl, tr, br, bl) = rect
        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)
        maxHeight = max(int(heightA), int(heightB))

        # Определение массива для трансформации
        dst = np.array(
            [
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1],
            ],
            dtype="float32",
        )

        # Вычисление матрицы преобразования перспективы
        M = cv2.getPerspectiveTransform(rect, dst)
        # Применение преобразования перспективы
        warped = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))

        # Добавление текста на трансформированное изображение
        cv2.putText(
            warped,
            "Hello world",
            (0, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 0),
            2,
        )

        # Вычисление обратной матрицы преобразования
        M_inv = cv2.getPerspectiveTransform(dst, rect)
        # Применение обратной трансформации
        warped_back = cv2.warpPerspective(warped, M_inv, (orig.shape[1], orig.shape[0]))

        # Создание маски для выделения контура
        mask = np.zeros_like(gray)
        cv2.fillConvexPoly(mask, approx, 255)

        # Применение маски к исходному изображению
        masked = cv2.bitwise_and(orig, orig, mask=cv2.bitwise_not(mask))
        # Сложение маскированного изображения с трансформированным
        final = cv2.add(masked, warped_back)

        # Отображение результата
        cv2.imshow("img", final)
        cv2.waitKey(1)
    else:
        # Отображение исходного изображения, если контур не прямоугольник
        cv2.imshow("img", orig)
        cv2.waitKey(1)