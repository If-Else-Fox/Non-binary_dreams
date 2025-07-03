import random

def clamp(x):
    return max(-2, min(2, x))

# Генератор сбалансированных весов
def generate_balanced_weights():
    flags = ['A', 'B', 'C', 'D', 'Z']
    variables = ['a', 'b', 'c', 'd']
    weights = {flag: {} for flag in flags}

    # Каждый флаг затрагивает 2–4 переменные
    for flag in flags:
        count = random.randint(2, 4)
        chosen_vars = random.sample(variables, count)
        for var in chosen_vars:
            weights[flag][var] = round(random.uniform(0.3, 0.9), 2)

    # Убедимся, что каждая переменная участвует хотя бы в 2 флагах
    variable_coverage = {var: 0 for var in variables}
    for flag_map in weights.values():
        for var in flag_map:
            variable_coverage[var] += 1

    for var, count in variable_coverage.items():
        if count < 2:
            needed = 2 - count
            possible_flags = [f for f in flags if var not in weights[f]]
            chosen_flags = random.sample(possible_flags, min(needed, len(possible_flags)))
            for flag in chosen_flags:
                weights[flag][var] = round(random.uniform(0.3, 0.9), 2)

    return weights

# Один запуск с антизалипанием и глобальным сбросом
def run_sequence(steps, weights, noise_level=0.1, max_stick=15):
    state = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    stick_count = {'a': 0, 'b': 0, 'c': 0, 'd': 0}

    for _ in range(steps):
        v = random.randint(-2, 2)
        f = random.choice(list(weights.keys()))

        # Немного шумим веса (динамика)
        dynamic_weights = {
            key: w + random.uniform(-w * noise_level, w * noise_level)
            for key, w in weights[f].items()
        }

        all_stuck = all(abs(state[k]) == 2 for k in state)

        for key, weight in dynamic_weights.items():
            # Проверка залипания
            if abs(state[key]) == 2:
                stick_count[key] += 1
            else:
                stick_count[key] = 0

            # Самоосвобождение
            if stick_count[key] >= max_stick:
                if state[key] > 0:
                    state[key] -= 0.5
                elif state[key] < 0:
                    state[key] += 0.5
                state[key] = clamp(state[key])
                continue

            # 🌬 Глобальный сброс, если всё залипло
            if all_stuck:
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

# Запуск эксперимента
def experiment(runs=1_000_000, steps=100):
    weights = generate_balanced_weights()
    print("Случайно сгенерированные сбалансированные веса:")
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
