items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(items: dict, budget: int):
    """
    Жадібний алгоритм:
    - сортуємо страви за співвідношенням калорій/вартість (від найбільшого до найменшого)
    - доки є бюджет, додаємо наступну найвигіднішу страву, якщо вона "влазить"
    Повертає: обрана_їжа, загальна_вартість, загальна_калорійність.
    """
    # Формуємо список (назва, cost, calories, ratio)
    enriched = []
    for name, data in items.items():
        cost = data["cost"]
        calories = data["calories"]
        ratio = calories / cost
        enriched.append((name, cost, calories, ratio))

    # Сортуємо за ratio від більшого до меншого
    enriched.sort(key=lambda x: x[3], reverse=True)

    chosen = []
    total_cost = 0
    total_calories = 0

    for name, cost, calories, ratio in enriched:
        if total_cost + cost <= budget:
            chosen.append(name)
            total_cost += cost
            total_calories += calories

    return chosen, total_cost, total_calories


def dynamic_programming(items: dict, budget: int):
    """
    Алгоритм динамічного програмування:
    Кожну страву можна взяти або 0 або 1 раз.
    Будуємо таблицю dp[i][w] — максимум калорій, який можна отримати,
    використовуючи перші i страв і бюджет w.
    Повертає: обрана_їжа, загальна_вартість, загальна_калорійність.
    """
    # Перетворимо словник у списки для зручності
    names = list(items.keys())
    costs = [items[name]["cost"] for name in names]
    calories = [items[name]["calories"] for name in names]
    n = len(names)

    # dp[i][w] – максимум калорій, використовуючи перші i предметів при бюджеті w
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    # Заповнюємо таблицю
    for i in range(1, n + 1):
        cost_i = costs[i - 1]
        cal_i = calories[i - 1]
        for w in range(budget + 1):
            # Не беремо i-ту страву 
            dp[i][w] = dp[i - 1][w]
            # Пробуємо взяти, якщо вистачає бюджету
            if cost_i <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - cost_i] + cal_i)

    # Максимальна калорійність при повному бюджеті
    max_calories = dp[n][budget]

    # Відновлюємо вибір страв (йдемо назад по таблиці)
    chosen = []
    w = budget
    total_cost = 0

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            # Це означає, що i-та страва була взята
            name = names[i - 1]
            chosen.append(name)
            total_cost += costs[i - 1]
            w -= costs[i - 1]

    chosen.reverse()  # щоб порядок відповідав початковому

    return chosen, total_cost, max_calories


if __name__ == "__main__":
    try:
        budget = int(input("\nВведіть ваш бюджет (наприклад, 100): "))
    except ValueError:
        print("Некоректне значення бюджету. Використано 100 за замовчуванням.")
        budget = 100

    print(f"\nБюджет: {budget}\n")

    # Жадібний алгоритм
    greedy_chosen, greedy_cost, greedy_calories = greedy_algorithm(items, budget)
    print("Жадібний алгоритм:")
    print("  Обрані страви:", greedy_chosen)
    print("  Загальна вартість:", greedy_cost)
    print("  Загальна калорійність:", greedy_calories)

    # Динамічне програмування
    dp_chosen, dp_cost, dp_calories = dynamic_programming(items, budget)
    print("\nАлгоритм динамічного програмування:")
    print("  Обрані страви:", dp_chosen)
    print("  Загальна вартість:", dp_cost)
    print("  Загальна калорійність:", dp_calories)

    # Порівняння
    print("\nПорівняння результатів:")
    print(f"  Жадібний: калорій = {greedy_calories}, вартість = {greedy_cost}")
    print(f"  Динамічне програмування: калорій = {dp_calories}, вартість = {dp_cost}")
    print()