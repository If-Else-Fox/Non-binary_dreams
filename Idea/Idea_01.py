import random

def clamp(x):
    return max(-2, min(2, x))

weights = {
    'A': {'b': 1.0, 'c': 0.5, 'd': 0.25},
    'B': {'a': 1.0, 'c': 0.5, 'd': 0.25},
    'C': {'a': 1.0, 'b': 0.5, 'd': 0.25},
    'D': {'a': 1.0, 'b': 0.5, 'c': 0.25},
    'Z': {'a': 1.0, 'b': 0.8, 'c': 0.5, 'd': 0.3}
}

def run_sequence(steps):
    state = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    for _ in range(steps):
        v = random.randint(-2, 2)
        f = random.choice(list(weights.keys()))
        for key, weight in weights[f].items():
            state[key] = clamp(state[key] + v * weight)
    return tuple(state.values())

results = set()
steps_count = 10  # Кол-во шагов в цепочке
iterations = 100000
clamped_count = 0

for _ in range(iterations):
    result = run_sequence(steps_count)
    results.add(result)
    if any(value in [-2, 2] for value in result):
        clamped_count += 1

print(f"Всего запусков цепочек: {iterations}")
print(f"Шагов в каждой цепочке: {steps_count}")
print(f"Уникальных комбинаций: {len(results)}")
print(f"Число случаев, когда хотя бы одна из переменных уперлась в предел: {clamped_count}")
print(f"Доля уникальных комбинаций: {len(results)/iterations*100:.2f}%")

