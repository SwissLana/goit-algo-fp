import numpy as np
import matplotlib.pyplot as plt

# Можливі суми та аналітичні значення ймовірностей при киданні двох шестигранних кубиків 
analytic_prob = {
    2: 1/36,
    3: 2/36,
    4: 3/36,
    5: 4/36,
    6: 5/36,
    7: 6/36,
    8: 5/36,
    9: 4/36,
    10: 3/36,
    11: 2/36,
    12: 1/36
}


def monte_carlo_rolls(num_rolls=100_000):
    """Імітує кидки двох кубиків та повертає словник частот."""
    dice1 = np.random.randint(1, 7, num_rolls)
    dice2 = np.random.randint(1, 7, num_rolls)
    sums = dice1 + dice2

    # Підрахунок частоти кожної суми від 2 до 12
    unique, counts = np.unique(sums, return_counts=True)
    freq = dict(zip(unique, counts))

    # Робимо повний словник (від 2 до 12) на випадок відсутніх значень
    full_freq = {i: freq.get(i, 0) for i in range(2, 13)}
    return full_freq


# Візуалізація результатів та порівняння з аналітичними даними 
def plot_probabilities(monte_probs, analytic_probs):
    sums = list(range(2, 13))
    
    # Частоти з Монте-Карло
    monte_counts = [monte_probs[s] for s in sums]
    total = sum(monte_counts)
    
    # Ймовірності
    monte = [c / total for c in monte_counts]
    analytic = [analytic_probs[s] for s in sums]
    
    # Переводимо в %
    monte_pct = [p * 100 for p in monte]
    analytic_pct = [p * 100 for p in analytic]
    
    monte = [monte_probs[s] for s in sums]
    analytic = [analytic_probs[s] for s in sums]


    # Графік
    plt.figure(figsize=(10, 5))
    plt.plot(sums, analytic_pct, marker="o", label="Аналітичні дані")
    plt.plot(sums, monte_pct, marker="s", label="Монте-Карло")
    plt.title("Порівняння ймовірностей сум при киданні двох кубиків")
    plt.xlabel("Сума")
    plt.ylabel("Ймовірність, %")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show()

    # Вивід таблиці результатів
    print("Таблиця результатів:\n")
    print(f"{'Сума':>4} | {'Монте-Карло, %':>16} | {'Аналітична, %':>16}")
    print("-" * 46)
    for i, s in enumerate(sums):
        print(f"{s:>4} | {monte_pct[i]:>15.2f}% | {analytic_pct[i]:>15.2f}%")


if __name__ == "__main__":
    num = 100_000
    print(f"\nСимуляція Монте-Карло ({num} кидків)...\n")

    freq = monte_carlo_rolls(num)
    plot_probabilities(freq, analytic_prob)