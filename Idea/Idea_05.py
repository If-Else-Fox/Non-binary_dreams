
import random

def clamp(x):
    return max(-2, min(2, x))

# Генерация случайных весов для флагов
def generate_random_weights():
    weights = {}
    for flag in ['A', 'B', 'C', 'D', 'Z']:
        affected_keys = random.sample(['a', 'b', 'c', 'd'], k=random.randint(1, 4))
        weights[flag] = {k: round(random.uniform(0.1, 1.0), 2) for k in affected_keys}
    return weights

# Модель одного запуска
def run_sequence(steps, weights, noise_level=0.1):
    state = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    stick_count = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    
    for _ in range(steps):
        v = random.randint(-2, 2)
        f = random.choice(list(weights.keys()))

        # Динамические веса с шумом
        dynamic_weights = {
            key: w + random.uniform(-w * noise_level, w * noise_level)
            for key, w in weights[f].items()
        }

        total_stickiness = 0
        for key in dynamic_weights:
            if state[key] in [-2, 2]:
                stick_count[key] += 1
                total_stickiness += stick_count[key] * 0.1
            else:
                stick_count[key] = 0

        if random.random() < min(total_stickiness, 1.0):
            v = -v

        for key, weight in dynamic_weights.items():
            new_value = state[key] + v * weight
            state[key] = clamp(new_value)

    return tuple(state.values())

# Запуск эксперимента
def experiment(runs=1_000_000, steps=100):
    weights = generate_random_weights()
    print("Случайно сгенерированные веса:")
    for flag, mapping in weights.items():
        print(f"  {flag}: {mapping}")

    results = set()
    clamped_count = 0

    for _ in range(runs):
        result = run_sequence(steps, weights)
        results.add(result)
        if any(value in [-2, 2] for value in result):
            clamped_count += 1

    print("\nРЕЗУЛЬТАТ ЭКСПЕРИМЕНТА")
    print(f"Всего запусков цепочек: {runs}")
    print(f"Шагов в каждой цепочке: {steps}")
    print(f"Уникальных комбинаций: {len(results)}")
    print(f"Число случаев, упершихся в предел [-2,2]: {clamped_count}")
    print(f"Доля уникальных комбинаций: {len(results)/runs*100:.2f}%")


if __name__ == "__main__":
    experiment()
