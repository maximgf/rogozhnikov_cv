import cv2 as cv
import numpy as np
from skimage.morphology import closing, disk
from time import sleep
# Загрузка изображения
img = cv.imread("video.png")

image = cv.imread('video1.jpg')

# Преобразование в оттенки серого
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

# Применение гауссового размытия для уменьшения шума
blurred = cv.GaussianBlur(gray, (5, 5), 0)

# Детекция границ с использованием метода Canny
edges = cv.Canny(blurred, 50, 150)

# Нахождение контуров
contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Фильтрация контуров по площади, чтобы найти контуры проекторного экрана и двух прямоугольников
min_area = 5000
max_area = 100000

filtered_contours = [contour for contour in contours if min_area < cv.contourArea(contour) < max_area]

# Создание маски для экрана проектора и двух прямоугольников
mask = np.zeros_like(image)

# Заполнение маски найденными контурами
for contour in filtered_contours:
    cv.drawContours(mask, [contour], -1, (255, 255, 255), thickness=cv.FILLED)

# Наложение маски на исходное изображение
result = cv.bitwise_and(image, mask)


cv.imshow("Image",result)
cv.waitKey()


def line_equation(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2:
        return f"x = {x1}"

    k = (y1 - y2) / (x2 - x1)
    b = y1 - k * x1

    return (k,b)

def line(x,k,b):
    
    y = int(k*x + b)

    return y






# Проверка, успешно ли загружено изображение
if img is not None:
    # Размеры изображения
    height, width, _ = img.shape

    # Начальные координаты круга
    y = 0
    x = int(width * 0.65)
    radius = 5  
    temp = 8

    while y < height:
        y+=temp
        trigger_bool = False
        # Преобразование изображения в оттенки серого
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Бинаризация изображения
        _, img_bin = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY_INV)

        # Применение морфологической операции закрытия
        img_closed = closing(img_bin, disk(3))

        # Поиск контуров
        contours, _ = cv.findContours(img_closed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Создание копии изображения
        img_copy = img.copy()

        # Рисование круга

        # Проверка пересечения круга с контурами
        for contour in contours:
                # Создание маски контура
            mask_contour = np.zeros_like(img_bin)
            cv.drawContours(mask_contour, [contour], -1, 255, -1)

            # Создание маски круга
            mask_circle = np.zeros_like(img_bin)
            cv.circle(mask_circle, (x, y), radius, 255, -1)

            # Проверка пересечения масок
            intersection = cv.bitwise_and(mask_contour, mask_circle)


            if np.sum(intersection > 0) > 0:

                points_intersection = (cv.findNonZero(intersection))[0][0]
                start_x,start_y = points_intersection[0],points_intersection[1]
                end_y = max(contour, key=lambda point: point[0][1])[0][1]
                end_x = [point[0][0] for point in contour if point[0][1] == end_y][0]
                
                k,b = line_equation((start_x,start_y),(end_x,end_y))
                print(start_x,start_y)
                points = contour[:, 0, :]
                
                if k > 0:
                    x += 100
                    end_x -= radius*2
                    for point in points:
                        border = x
                        if point[0] < start_x and point[0] > end_x - radius*2:
                            x = point[0]
                            y = point[1] - 15
                            img_copy = img.copy()
                            cv.circle(img_copy, (point[0], point[1] - 10), radius, (0, 255, 0), -1)
                            
                            cv.imshow('Image', img_copy)

                            cv.waitKey(1)
                            if x > border:
                                break


                    x = end_x
                    y = end_y 
                else:
                    end_x += radius*2
                    x -= 100
                    for point in points:
                        border = x
                        if point[0] > start_x  and end_x + radius*2>= point[0]:
                            x = point[0]
                            y = point[1] - 15
                            img_copy = img.copy()
                            cv.circle(img_copy, (point[0], point[1] - 10), radius, (0, 255, 0), -1)
                            cv.imshow('Image', img_copy)

                            cv.waitKey(1)
                            if x < border:
                                break

                    x = end_x
                    y = end_y

                

            else:

                img_copy = img.copy()
                cv.circle(img_copy, (x, y), radius, (0, 255, 0), -1)
                cv.imshow('Image', img_copy)
                cv.waitKey(1)
  


                




    # Закрытие всех окон после завершения цикла
    cv.destroyAllWindows()
else:
    print("Ошибка при загрузке изображения")


