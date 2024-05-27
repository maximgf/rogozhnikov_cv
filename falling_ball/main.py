import cv2 as cv
import numpy as np
from skimage.morphology import closing, disk
from time import sleep
# Загрузка изображения
img = cv.imread("video1.jpg")

# Преобразование изображения в оттенки серого
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
 
 
_, img_bin = cv.threshold(img, 70, 255, cv.THRESH_BINARY)


contours, _ = cv.findContours(img_bin, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

largest_contour = max(contours, key=cv.contourArea)

x, y, w, h = cv.boundingRect(largest_contour)

img = img[y+65:y+h-40, x+20:x+w-30]
img = cv.GaussianBlur(img,(9,9),0)
_, img_bin = cv.threshold(img, 139, 255, cv.THRESH_BINARY)
 

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
    height, width = img.shape

    # Начальные координаты круга
    y = 0
    x = int(width * 0.4)
    radius = 5  
    temp = 8
     
    while y < height:
        sleep(0.5)
         
        y+=temp
        trigger_bool = False

        # Поиск контуров
        contours, _ = cv.findContours(img_bin, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Создание копии изображения
        img_copy = img.copy()

        # Рисование круга

        # Проверка пересечения круга с контурами
        for contour in contours:
            epsilon = 0.02 * cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, epsilon, True)
                # Создание маски контура
            mask_contour = np.zeros_like(img_bin)
            cv.drawContours(mask_contour, [contour], -1, 255, -1)

            # Создание маски круга
            mask_circle = np.zeros_like(img_bin)
            cv.circle(mask_circle, (x, y), radius, 255, -1)

            # Проверка пересечения масок
            intersection = cv.bitwise_and(mask_contour, mask_circle)


            if np.sum(intersection > 0) > 0 and len(approx) < 10:
                print(len(approx))
                points_intersection = (cv.findNonZero(intersection))[0][0]
                start_x,start_y = points_intersection[0],points_intersection[1]
                end_y = max(contour, key=lambda point: point[0][1])[0][1]
                end_x = [point[0][0] for point in contour if point[0][1] == end_y][0]
                
                k,b = line_equation((start_x,start_y),(end_x,end_y))
                 
                points = contour[:, 0, :]
                print(len(approx))
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


