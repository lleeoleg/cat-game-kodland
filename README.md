# 🐱 Cat Game

Мультиплеерная игра с котиками, где игроки управляют своими персонажами через Telegram-бота.  
Задача — собирать монетки на игровом поле.  

## 🎮 Возможности
- Управление котиком через Telegram кнопки (⬆️ ⬇️ ⬅️ ➡️)  
- Анимация ходьбы котика (спрайты с плавным движением)  
- Система монеток на карте  
- Лидерборд с результатами игроков  
- Flask-сервер для хранения состояния игры  

## 🛠️ Технологии
- [Python](https://www.python.org/)  
- [Flask](https://flask.palletsprojects.com/) — сервер для игры  
- [PyGame Zero](https://pygame-zero.readthedocs.io/) — визуализация поля и котиков  
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) — бот для Telegram  
- Git + GitHub  

## 🚀 Запуск

1. Клонируй репозиторий:
bash
git clone https://github.com/lleeoleg/cat-game-kodland.git
cd cat-game-kodland

2. Создай виртуальное окружение и установи зависимости:
python3 -m venv venv
source venv/bin/activate   # для Mac/Linux
venv\Scripts\activate      # для Windows

pip install -r requirements.txt


3.Запусти Flask-сервер:
python server.py

4.Запусти игру с визуализацией:
python game.py

5.Запусти Telegram-бота:
python bot.py

📸 Скриншоты
<img width="640" height="493" alt="image" src="https://github.com/user-attachments/assets/581cc745-8ebc-4204-8663-c330e801a5db" />
<img width="371" height="513" alt="image" src="https://github.com/user-attachments/assets/70211ff6-8915-4962-8be2-b00324bd5d38" />
<img width="902" height="222" alt="image" src="https://github.com/user-attachments/assets/8bb1f36c-6211-4600-90cf-7cf9e6edf9c7" />
<img width="362" height="512" alt="image" src="https://github.com/user-attachments/assets/23283a64-69b2-405b-88c8-1c15f2c5c65c" />



🏆 Лидерборд

Игра сохраняет статистику игроков: имя, количество монет и длительность игры.




