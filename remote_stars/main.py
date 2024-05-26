import numpy as np
import socket

# Функция для приема пакетов данных через сокет
def packet(sock, n):
    # Создание пустого байтового массива для хранения данных
    data = bytearray()
    # Пока длина данных меньше заданного размера n
    while len(data) < n:
        # Получение данных из сокета
        pack = sock.recv(n - len(data))
        # Добавление полученных данных в массив
        data.extend(pack)
    # Возвращение собранных данных
    return data

# Функция для вычисления площади вокруг точки (x, y) в матрице b
def area(b, y, x):
    # Возвращает плоский массив данных из матрицы b, ограниченной областью вокруг точки (x, y)
    return b[y-1:y+2, x-1:x+2].flatten()

# Функция для поиска двух позиций в матрице с максимальным расстоянием между ними
def maxLen(data):
    # Инициализация переменных для хранения позиций
    onePos, secondPos = None, None
    # Обход матрицы
    for y in range(1, data.shape[0] - 1):
        for x in range(1, data.shape[1] - 1):
            # Получение значения в текущей позиции
            v = data[y, x]
            # Пропуск, если значение меньше 3
            if v < 3: continue
            # Пропуск, если есть соседние элементы больше текущего
            if any([n > v for n in area(data, y, x)]): continue
            # Если первая позиция не установлена, устанавливаем ее
            if onePos is None: onePos = (x, y)
            # Если вторая позиция не установлена и первая уже установлена, устанавливаем вторую
            elif secondPos is None: secondPos = (x, y)
            # Если обе позиции установлены, прекращаем поиск
            else: break
    # Возвращаем найденные позиции
    return onePos, secondPos

# Инициализация сокета
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Подключение к серверу
    sock.connect(("84.237.21.36", 5152))
    # Цикл для повторения действий 10 раз
    for i in range(10):
        # Отправка запроса на получение данных
        sock.send(b"get")
        # Получение данных
        rc = packet(sock, 40002)
        # Преобразование данных в матрицу изображения
        img = np.frombuffer(rc[2:40002], dtype="uint8").reshape(200, 200)
        # Поиск двух позиций с максимальным расстоянием
        onePos, secondPos = maxLen(img)
        # Вычисление расстояния между найденными точками
        res = np.sqrt((onePos[0] - secondPos[0]) ** 2 + (onePos[1] - secondPos[1]) ** 2)
        # Вывод расстояния
        print(res)

