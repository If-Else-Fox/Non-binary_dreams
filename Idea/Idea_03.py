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
    stick_count = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    
    for _ in range(steps):
        v = random.randint(-2, 2)
        f = random.choice(list(weights.keys()))

        # === Новый порядок: сначала решаем, надо ли перевернуть v ===
        total_stickiness = 0.0
        for key in weights[f]:
            if state[key] in [-2, 2]:
                stick_count[key] += 1
                total_stickiness += stick_count[key] * 0.1
            else:
                stick_count[key] = 0

        if random.random() < min(total_stickiness, 1.0):
            v = -v  # теперь это делается ДО применения v

        # === Применяем одно и то же v ко всем ручкам ===
        for key, weight in weights[f].items():
            new_value = state[key] + v * weight
            state[key] = clamp(new_value)
    
    return tuple(state.values())

# Тестируем
results = set()
steps_count = 100
iterations = 1000000
clamped_count = 0

for _ in range(iterations):
    result = run_sequence(steps_count)
    results.add(result)
    if any(value in [-2, 2] for value in result):
        clamped_count += 1

print(f"Всего запусков цепочек: {iterations}")
print(f"Шагов в каждой цепочке: {steps_count}")
print(f"Уникальных комбинаций: {len(results)}")
print(f"Число случаев, упершихся в предел [-2,2]: {clamped_count}")
print(f"Доля уникальных комбинаций: {len(results)/iterations*100:.2f}%")
