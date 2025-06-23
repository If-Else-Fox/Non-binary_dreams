from critter import Critter
import random

signals = {
    'X': 'взаимодействуем с социумом',
    'Y': 'встречаем опасность',
    'Z': 'включаем активный режим',
    'W': 'входим в режим отдыха'
}

def main():
    critter = Critter()
    signal_keys = list(signals.keys())

    for _ in range(30):  # 30 сигналов для проверки
        signal = random.choice(signal_keys)
        value = random.randint(-2, 2)

        critter.process_signal(signal, value)
        critter.show_state(signal, value, signals[signal])

if __name__ == '__main__':
    main()
