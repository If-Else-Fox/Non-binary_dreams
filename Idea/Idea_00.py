import random

# Инициализация состояния
def clamp(x):
    return max(-2, min(2, x))

# Весовые коэффициенты для каждого флага
weights = {
    'A': {'b': 1.0, 'c': 0.5, 'd': 0.25},
    'B': {'a': 1.0, 'c': 0.5, 'd': 0.25},
    'C': {'a': 1.0, 'b': 0.5, 'd': 0.25},
    'D': {'a': 1.0, 'b': 0.5, 'c': 0.25},
    'Z': {'a': 1.0, 'b': 0.8, 'c': 0.5, 'd': 0.3}
}

results = set()
clamped_count = 0
iterations = 1000000

for _ in range(iterations):
    state = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    v = random.randint(-2, 2)
    f = random.choice(list(weights.keys()))

    for key, weight in weights[f].items():
        state[key] = clamp(state[key] + v * weight)
        if state[key] in [-2, 2]:
            clamped_count += 1

    results.add(tuple(state.values()))

# Итоговая статистика
print(f"Всего запусков: {iterations}")
print(f"Уникальных комбинаций: {len(results)}")
print(f"Число случаев, когда хотя бы одна из переменных уперлась в предел: {clamped_count}")
print(f"Доля уникальных комбинаций: {len(results)/iterations*100:.2f}%")

