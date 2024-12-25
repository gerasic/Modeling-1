import numpy as np
import matplotlib.pyplot as plt

m = 1  # масса тела (кг)
R = 5  # радиус кольца (м)
alpha = np.pi / 2 + np.pi / 6  # угловой размер дуги (рад)
mu = 0.01  # коэффициент трения
g = 9.81  # ускорение свободного падения (м/с^2)

def calculate_min_velocity(m, R, alpha, mu, g):
    """
    Расчёт минимальной скорости для прохождения дуги.
    """
    
    # Работа силы трения
    work_friction = mu * m * g * R * alpha

    # Конечная потенциальная энергия
    final_potential_energy = m * g * R * (1 - np.cos(alpha))

    # Необходимая кинетическая энергия
    required_kinetic_energy = final_potential_energy + work_friction

    # Минимальная скорость
    v_min = np.sqrt(2 * required_kinetic_energy / m)
    return v_min

def trajectory_after_detachment(v_min, R, alpha):
    """
    Построение траектории тела после отрыва от дуги.
    """
    # Начальные условия
    theta = np.linspace(0, alpha, 100)
    x_arc = R * np.sin(theta)
    y_arc = -R * (1 - np.cos(theta))

    # После отрыва
    x_detach = x_arc[-1]
    y_detach = y_arc[-1]
    vx = v_min * np.cos(alpha)
    vy = v_min * np.sin(alpha)

    # Моделирование движения
    t = np.linspace(0, 2 * vy / g, 100)
    x_free = x_detach + vx * t
    y_free = y_detach + vy * t - 0.5 * g * t**2

    return x_arc, y_arc, x_free, y_free

# Вычисления
v_min = calculate_min_velocity(m, R, alpha, mu, g)
x_arc, y_arc, x_free, y_free = trajectory_after_detachment(v_min, R, alpha)

# Визуализация
plt.figure(figsize=(10, 6))
plt.plot(x_arc, y_arc, label="Дуга кольца")
plt.plot(x_free, y_free, label="Траектория после отрыва", linestyle="--")
plt.axhline(0, color="black", linewidth=0.5, linestyle="--")
plt.title("Траектория тела в задаче 'Мёртвая петля'")
plt.xlabel("X, м")
plt.ylabel("Y, м")
plt.legend()
plt.grid()
plt.show()
