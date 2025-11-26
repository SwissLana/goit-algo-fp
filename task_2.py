import matplotlib.pyplot as plt
import numpy as np


def draw_tree(x, y, length, angle, depth):
    """
    Рекурсивна функція для побудови дерева Піфагора.
    x, y  – координати початку гілки
    length – довжина гілки
    angle – кут нахилу (в градусах)
    depth – рівень рекурсії
    """
    if depth == 0:
        return

    # Обчислюємо кінець гілки
    x2 = x + length * np.cos(np.radians(angle))
    y2 = y + length * np.sin(np.radians(angle))

    # Малюємо гілку
    plt.plot([x, x2], [y, y2], color='brown', linewidth=1.5)

    # Рекурсивно малюємо 2 нові гілки
    new_length = length * 0.7

    # Ліва гілка: кут +45°
    draw_tree(x2, y2, new_length, angle + 45, depth - 1)

    # Права гілка: кут -45°
    draw_tree(x2, y2, new_length, angle - 45, depth - 1)



# Запитуємо глибину у користувача
try:
    depth = int(input("Введіть рівень рекурсії (рекомендовано 6–10): "))
except ValueError:
    print("Некоректний ввід. Використано значення depth = 8")
    depth = 8

plt.figure(figsize=(8, 8))
plt.axis('off')

# Початкові координати стовбура
start_x = 0
start_y = -1

# Малюємо дерево
draw_tree(start_x, start_y, length=1, angle=90, depth=depth)

plt.show()