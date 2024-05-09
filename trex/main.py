import cv2 as cv
from mss import mss
import numpy as np
from time import sleep, time
import pyautogui as inp
from skimage.morphology import closing,disk

dino_img = cv.imread("t-rex.png")
dino_img = cv.cvtColor(dino_img, cv.COLOR_RGB2GRAY)


monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
frame_rate = 120
frame_duration = 1.0 / frame_rate
with mss() as sct:
    inp.press("space")
    sleep(2)
    # Захват изображения
    img = np.array(sct.grab(monitor))
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    # Поиск шаблона
    _, thrash, t_min_loc, t_max_loc = cv.minMaxLoc(
        cv.matchTemplate(img, dino_img, cv.TM_SQDIFF_NORMED)
    )
    monitor = {
    "top": t_min_loc[1] - 94,
    "left": t_min_loc[0] - 4,
    "width": 300,
    "height": 150,
    }
    img = np.array(sct.grab(monitor))
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    _, thrash, t_min_loc, t_max_loc = cv.minMaxLoc(
    cv.matchTemplate(img, dino_img, cv.TM_SQDIFF_NORMED))
    

    # Вычисление координат для области, в которой будет нарисован прямоугольник
    #top_left = (t_min_loc[0], t_min_loc[1])
    #bottom_right = (t_min_loc[0] + dino_img.shape[1], t_min_loc[1] + dino_img.shape[0])
    temp = 0
    temp_time = time()
    temp_v = 0
    start = time()

    while True:
        frame_start_time = time()
        img = np.array(sct.grab(monitor))
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        _, img = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
        #cv.rectangle(img, top_left, bottom_right, (255, 0,0), 2)
        enemy = img[:,int(img.shape[1] *0.3):]
        enemy = enemy[:int(enemy.shape[0] * 0.855),:]
        enemy = closing(enemy,disk(3))
        contours, _ = cv.findContours(enemy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        #cv.drawContours(enemy, contours, -1, (255, 0, 0), 2)
        for contour in contours:
        #Получить коорд ограничивающего прямоугольника для текущего контура
            x, y, w, h = cv.boundingRect(contour)
            #t = time() - temp_time
            #s = (temp - x)
            #v = s/(t+0.001)


            #agr = w * 0.7+ h*0.85
            # Нарисуйте прямоугольник на изображении
                #cv.rectangle(enemy, (x, y), (x + w, y + h), (255, 0, 0), 2)
            #if time() - start < 34:
                #agr = 35

            if x <= 24:
                if y + h - t_min_loc[1] - 20 > 0:
                    sleeper = (w) * 20 / (1000 + (round(time() - start,3) * 40))
                    if y - t_min_loc[1] >= -10:
                        sleeper += 0.1
                        #print("high")
                    #if sleeper < 0:
                        #print("xx")
                        #sleeper = 0.2
                    #print(time() - start)
                    inp.press("up")
                    sleep(sleeper/4)
                    inp.keyDown("down")
                    sleep(0.02)
                    inp.keyUp("down")
                else:
                    inp.keyDown("down")
                    sleep(abs(sleeper))
                    inp.keyUp("down")
            #temp = x
            #temp_time = time()
            #temp_v = v

        frame_end_time = time()
        elapsed_time = frame_end_time - frame_start_time
        if elapsed_time < frame_duration:
            sleep(frame_duration - elapsed_time)

        if cv.waitKey(1) == ord ==("q"):
            break
        cv.imshow('Image', enemy)
cv.destroyAllWindows() 



