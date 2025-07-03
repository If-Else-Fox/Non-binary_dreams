import random

def clamp(x):
    return max(-2, min(2, x))

# Генерация случайных весов
def generate_random_weights():
    weights = {}
    for flag in ['A', 'B', 'C', 'D', 'Z']:
        affected = random.sample(['a', 'b', 'c', 'd'], k=random.randint(1, 4))
        weights[flag] = {k: round(random.uniform(0.1, 1.0), 2) for k in affected}
    return weights

# Один цикл с антизалипанием
def run_sequence(steps, weights, noise_level=0.1, max_stick=15):
    state = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    stick_count = {'a': 0, 'b': 0, 'c': 0, 'd': 0}

    for _ in range(steps):
        v = random.randint(-2, 2)
        f = random.choice(list(weights.keys()))

        # Варьируем веса
        dynamic_weights = {
            key: w + random.uniform(-w * noise_level, w * noise_level)
            for key, w in weights[f].items()
        }

        # Проверка общего "залипания" всей системы
        all_stuck = all(abs(state[k]) == 2 for k in state)

        for key, weight in dynamic_weights.items():
            # Проверка залипания
            if abs(state[key]) == 2:
                stick_count[key] += 1
            else:
                stick_count[key] = 0

            # Реакция на локальное залипание
            if stick_count[key] >= max_stick:
                # Постепенно возвращаем к 0
                if state[key] > 0:
                    state[key] -= 0.5
                elif state[key] < 0:
                    state[key] += 0.5
                state[key] = clamp(state[key])
                continue

            # Глобальный сброс
            if all_stuck:
                # "вдох" — мягко уходим к центру
                if state[key] > 0:
                    state[key] -= 0.2
                elif state[key] < 0:
                    state[key] += 0.2
                state[key] = clamp(state[key])
                continue

            # Обычное обновление
            new_value = state[key] + v * weight
            state[key] = clamp(new_value)

    return tuple(round(v, 2) for v in state.values())

# Эксперимент
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
        if any(abs(v) >= 2 for v in result):
            clamped_count += 1

    print("\nРЕЗУЛЬТАТ ЭКСПЕРИМЕНТА")
    print(f"Всего запусков цепочек: {runs}")
    print(f"Шагов в каждой цепочке: {steps}")
    print(f"Уникальных комбинаций: {len(results)}")
    print(f"Число случаев, упершихся в предел [-2,2]: {clamped_count}")
    print(f"Доля уникальных комбинаций: {len(results)/runs*100:.2f}%")

# Старт
if __name__ == "__main__":
    experiment()
