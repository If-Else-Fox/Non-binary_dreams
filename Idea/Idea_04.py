import random

def clamp(x):
    return max(-2, min(2, x))

# Базовые веса (как в оригинале)
base_weights = {
    'A': {'b': 1.0, 'c': 0.5, 'd': 0.25},
    'B': {'a': 1.0, 'c': 0.5, 'd': 0.25},
    'C': {'a': 1.0, 'b': 0.5, 'd': 0.25},
    'D': {'a': 1.0, 'b': 0.5, 'c': 0.25},
    'Z': {'a': 1.0, 'b': 0.8, 'c': 0.5, 'd': 0.3}
}

# Шум в пределах ±10%
def noisy_weight(base, noise_level=0.1):
    variation = base * noise_level
    return base + random.uniform(-variation, variation)

def run_sequence(steps, noise_level=0.1):
    state = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    stick_count = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    
    for _ in range(steps):
        v = random.randint(-2, 2)
        f = random.choice(list(base_weights.keys()))

        # Создаём рандомизированные веса
        dynamic_weights = {
            key: noisy_weight(weight, noise_level)
            for key, weight in base_weights[f].items()
        }

        # Оцениваем залипания
        total_stickiness = 0.0
        for key in dynamic_weights:
            if state[key] in [-2, 2]:
                stick_count[key] += 1
                total_stickiness += stick_count[key] * 0.1
            else:
                stick_count[key] = 0

        # Инвертируем сигнал, если нужно
        if random.random() < min(total_stickiness, 1.0):
            v = -v

        # Применяем сигнал с весами
        for key, weight in dynamic_weights.items():
            new_value = state[key] + v * weight
            state[key] = clamp(new_value)

    return tuple(state.values())

# Тестируем
results = set()
steps_count = 100
iterations = 1_000_000
clamped_count = 0

for _ in range(iterations):
    result = run_sequence(steps_count, noise_level=0.1)
    results.add(result)
    if any(value in [-2, 2] for value in result):
        clamped_count += 1

print(f"Всего запусков цепочек: {iterations}")
print(f"Шагов в каждой цепочке: {steps_count}")
print(f"Уникальных комбинаций: {len(results)}")
print(f"Число случаев, упершихся в предел [-2,2]: {clamped_count}")
print(f"Доля уникальных комбинаций: {len(results)/iterations*100:.2f}%")

