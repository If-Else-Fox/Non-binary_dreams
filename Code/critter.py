class Critter:
    """Класс, описывающий состояние зверька"""
    def __init__(self):
        # Инициализация начальных состояний
        self.energy = 0.0
        self.anxiety = 0.0
        self.happiness = 0.0
        self.fatigue = 0.0
        self.stress = 0.0
        self.acceptance = 0.1
        self.resilience = 5

    def apply_effects(self, d_energy=0, d_anxiety=0, d_happiness=0,
                      d_fatigue=0, d_stress=0, d_acceptance=0, d_resilience=0):
        """Изменение состояния зверька"""
        self.energy += d_energy
        self.anxiety += d_anxiety
        self.happiness += d_happiness
        self.fatigue += d_fatigue
        self.stress += d_stress
        self.acceptance += d_acceptance
        self.resilience += d_resilience

    def process_signal(self, signal, value):
        """Обрабатываем приходящий сигнал и изменяем состояние в зависимости от его типа и значения"""
        if signal == 'X':  # Взаимодействуем с социумом
            self.apply_effects(
                d_energy=0.1 * value,
                d_anxiety=0.1 * value,
                d_happiness=0.3 * value,
                d_fatigue=0.1 * value,
                d_stress=0.2 * value,
                d_acceptance=0.01 * value
            )
        elif signal == 'Y':  # Встречаем опасность
            self.apply_effects(
                d_energy=-0.1 * value,
                d_anxiety=0.3 * value,
                d_happiness=-0.2 * value,
                d_fatigue=0.2 * value,
                d_stress=0.5 * value,
                d_acceptance=-0.01 * value
            )
        elif signal == 'Z':  # Активный режим
            self.apply_effects(
                d_energy=0.3 * value,
                d_anxiety=0.2 * value,
                d_happiness=0.1 * value,
                d_fatigue=0.3 * value,
                d_stress=0.4 * value,
                d_acceptance=0.0 * value
            )
        elif signal == 'W':  # Режим отдыха
            self.apply_effects(
                d_energy=0.5 * value,
                d_anxiety=-0.3 * value,
                d_happiness=0.2 * value,
                d_fatigue=-0.4 * value,
                d_stress=-0.3 * value,
                d_acceptance=0.0 * value
            )
        else:
            # Для неизвестных сигналов — никаких изменений
            pass

    def status(self):
        """Текущие показатели в удобочитаемом формате"""
        return {
            "energy": round(self.energy, 2),
            "anxiety": round(self.anxiety, 2),
            "happiness": round(self.happiness, 2),
            "fatigue": round(self.fatigue, 2),
            "stress": round(self.stress, 2),
            "acceptance": round(self.acceptance, 2),
            "resilience": round(self.resilience, 2),
        }

    def show_state(self, signal, value, description):
        """Отображение результата обработки сигнала"""
        status = self.status()
        status_str = " | ".join([f"{k.capitalize()}: {v}" for k, v in status.items()])
        print(f"⚡️ Сигнал: {signal} ({description}) v = {value}")
        print(status_str)
        print()

