import matplotlib.pyplot as plt
import numpy as np

# Инициализация параметров
m = 2          # Масса тела, кг
R = 4          # Радиус дуги, м
theta_total = np.pi/100  # Общий угол дуги
mu = 0.02      # Коэффициент трения
g = 9.81       # Ускорение свободного падения, м/с^2
dt = 0.001     # Шаг времени для дуги, с
dt_flight = 0.0001  # Шаг времени для свободного падения, с
difference = 0.0001  # Точность для бинарного поиска
MAX_SPEED = 100  # Максимальная скорость (порог для проверки)
MIN_SPEED = 1e-5  # Минимальная скорость для остановки

# Функция для обновления состояния тела на дуге
def update_arc(v, theta, s_path):
    normal_force = (m * v ** 2 / R) + m * g * np.cos(theta)
    friction_force = mu * normal_force
    tangential_acc = -friction_force / m - g * np.sin(theta)
    v_new = max(v + tangential_acc * dt, 0)
    s_path_new = s_path + v * dt
    theta_new = min(s_path_new / R, theta_total)
    x_new = R * np.sin(theta_new)
    y_new = R * (1 - np.cos(theta_new))
    return v_new, theta_new, s_path_new, x_new, y_new

# Функция для проверки, может ли тело пройти весь путь по дуге с заданной начальной скоростью
def can_complete_arc(v0):
    theta = 0
    s_path = 0
    v = v0
    while theta < theta_total:
        if v < MIN_SPEED:
            return False
        v, theta, s_path, _, _ = update_arc(v, theta, s_path)
    return True

# Бинарный поиск минимальной скорости, при которой тело может пройти всю дугу
v_low = 0
v_high = MAX_SPEED
while v_high - v_low > difference:
    v_mid = (v_low + v_high) / 2
    if can_complete_arc(v_mid):
        v_high = v_mid
    else:
        v_low = v_mid

v0 = (v_low + v_high) / 2

if round(v0, 2) == MAX_SPEED:
    print("Тело не может пройти участок")
else:
    theta = 0
    s_path = 0
    v = v0
    x, y = 0, 0
    flag = True
    detach_point = None
    detach_theta = None
    vx, vy = 0, 0

    arc_coords = []
    flight_coords = []

    while flag or y > 0:
        if flag:
            if v < MIN_SPEED or theta >= theta_total:
                flag = False
                detach_point = (x, y)
                detach_theta = theta
                vx = v * np.cos(theta)
                vy = v * np.sin(theta)
            else:
                v, theta, s_path, x, y = update_arc(v, theta, s_path)
                arc_coords.append((x, y))
        else:
            vy -= g * dt_flight
            x += vx * dt_flight
            y = max(0, y + vy * dt_flight)
            if y > 0 or len(flight_coords) < 10:  # Добавляем хотя бы 10 точек
                flight_coords.append((x, y))

    arc_x, arc_y = zip(*arc_coords)
    flight_x, flight_y = zip(*flight_coords) if flight_coords else ([], [])

    print(f"Минимальная начальная скорость: v0 = {v0:.2f} м/с")
    if detach_point:
        print(f"Точка отрыва: x = {detach_point[0]:.2f} м, y = {detach_point[1]:.2f} м")
        print(f"Горизонтальная скорость при отрыве (vx): {vx:.4f} м/с")
        print(f"Вертикальная скорость при отрыве (vy): {vy:.4f} м/с")
        print(f"Угол отрыва (theta): {np.degrees(detach_theta):.4f}°")

    plt.figure(figsize=(10, 6))
    plt.plot(arc_x, arc_y, color="blue", label="Движение по дуге")
    if flight_coords:
        plt.plot(flight_x, flight_y, color="red", label="Свободное падение")
    if detach_point:
        plt.scatter(*detach_point, color="green", label="Точка отрыва", zorder=5)
    plt.title("Движение тела по дуге и свободное падение")
    plt.xlabel("X, м")
    plt.ylabel("Y, м")
    plt.grid()
    plt.legend()
    plt.show()
