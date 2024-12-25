import matplotlib.pyplot as plt
import numpy as np

# Инициализация параметров
m = 2          # Масса тела, кг
R = 4          # Радиус дуги, м
theta_total = np.pi # Общий угол дуги (5/6 от pi, т.е. 150 градусов)
mu = 0.02      # Коэффициент трения
g = 9.81       # Ускорение свободного падения, м/с^2
dt = 0.01      # Шаг времени, с
difference = 0.0001  # Точность для бинарного поиска
MAX_SPEED = 100  # Максимальная скорость (порог для проверки)

# Функция для обновления состояния тела на дуге
def update_arc(v, theta, s_path):
    # Вычисление силы нормального давления
    normal_force = (m * v ** 2 / R) + m * g * np.cos(theta)
    # Вычисление силы трения
    friction_force = mu * normal_force
    # Вычисление тангенциального ускорения с учетом силы трения и силы тяжести
    tangential_acc = -friction_force / m - g * np.sin(theta)
    # Обновление скорости с учетом ускорения
    v_new = max(v + tangential_acc * dt, 0)  # Ограничиваем скорость от отрицательных значений
    # Обновление пути вдоль дуги
    s_path_new = s_path + v * dt
    # Вычисление нового угла на дуге
    theta_new = s_path_new / R
    # Преобразование угла в координаты (x, y)
    x_new = R * np.sin(theta_new)
    y_new = R * (1 - np.cos(theta_new))
    return v_new, theta_new, s_path_new, x_new, y_new

# Функция для проверки, может ли тело пройти весь путь по дуге с заданной начальной скоростью
def can_complete_arc(v0):
    theta = 0
    s_path = 0
    v = v0
    
    # Проверка, пока не пройден весь угол дуги
    while theta < theta_total:
        # Вычисление силы нормального давления
        normal_force = (m * v ** 2 / R) + m * g * np.cos(theta)
        # Если сила нормального давления меньше или равна нулю, то тело не может пройти дугу
        if normal_force <= 0 or v <= 0:
            return False
        # Обновление состояния тела на дуге
        v, theta, s_path, _, _ = update_arc(v, theta, s_path)
    return True

# Бинарный поиск минимальной скорости, при которой тело может пройти всю дугу
v_low = 0
v_high = 100
while v_high - v_low > difference:
    v_mid = (v_low + v_high) / 2
    # Проверка, может ли тело пройти дугу с текущей скоростью
    if can_complete_arc(v_mid):
        v_high = v_mid  # Если может, уменьшаем верхнюю границу поиска
    else:
        v_low = v_mid  # Если не может, увеличиваем нижнюю границу поиска

# Среднее значение скоростей в низкой и высокой границе является минимальной начальной скоростью
v0 = (v_low + v_high) / 2

# Проверка, не превышает ли минимальная начальная скорость максимальное значение
if round(v0, 2) == MAX_SPEED:
    print("Тело не может пройти участок")
else:
    theta = 0
    s_path = 0
    v = v0
    x, y = 0, 0
    flag = True
    detach_point = None  # Точка отрыва
    detach_theta = None  # Угол отрыва
    vx, vy = 0, 0  # Горизонтальная и вертикальная компоненты скорости при отрыве

    arc_coords = []  # Список координат тела на дуге
    flight_coords = []  # Список координат тела после отрыва

    # Моделируем движение тела по дуге и после отрыва
    while flag or y > 0:
        if flag:
            # Вычисление силы нормального давления для проверки, можно ли продолжить движение по дуге
            normal_force = (m * v ** 2 / R) + (m * g * np.cos(theta))
            # Если сила нормального давления отрицательна или достигнут конец дуги, отрываем тело
            if normal_force <= 0 or theta >= theta_total:
                flag = False  # Смена флага, начинаем моделировать свободное падение
                detach_point = (x, y)  # Сохраняем точку отрыва
                detach_theta = theta  # Сохраняем угол отрыва
                vx = v * np.cos(theta)  # Горизонтальная скорость при отрыве
                vy = v * np.sin(theta)  # Вертикальная скорость при отрыве
            else:
                # Обновляем скорость, угол и координаты тела на дуге
                v, theta, s_path, x, y = update_arc(v, theta, s_path)
                arc_coords.append((x, y))  # Добавляем координаты на дуге
        else:
            # Моделируем свободное падение тела после отрыва
            vy -= g * dt  # Учёт ускорения свободного падения
            x += vx * dt  # Обновление координаты X
            y = max(0, y + vy * dt)  # Обновление координаты Y (ограничиваем падение на землю)
            flight_coords.append((x, y))  # Добавляем координаты в список

    # Разделение координат на X и Y для дуги и падения
    arc_x, arc_y = zip(*arc_coords)
    flight_x, flight_y = zip(*flight_coords)

    # Вывод минимальной начальной скорости и информации о точке отрыва
    print(f"Минимальная начальная скорость: v0 = {v0:.2f} м/с")
    if detach_point:
        print(f"Точка отрыва: x = {detach_point[0]:.2f} м, y = {detach_point[1]:.2f} м")
        print(f"Горизонтальная скорость при отрыве (vx): {vx:.2f} м/с")
        print(f"Вертикальная скорость при отрыве (vy): {vy:.2f} м/с")
        print(f"Угол отрыва (theta): {np.degrees(detach_theta):.2f}°")

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(arc_x, arc_y, color="blue", label="Движение по дуге")  # Дуга
    plt.plot(flight_x, flight_y, color="red", label="Свободное падение")  # Падение

    if detach_point:
        plt.scatter(*detach_point, color="green", label="Точка отрыва", zorder=5)

    plt.title("Движение тела по дуге и свободное падение")
    plt.xlabel("X, м")
    plt.ylabel("Y, м")
    plt.grid()
    plt.legend()
    plt.show()
