# telegram_bot_quiz

*Задача:

Создание Telegram-бота-квиза с использованием aiogram v3 и BotFather. Бот предлагает пользователю пройти серию вопросов с вариантами ответов, хранит прогресс в SQLite-базе и отображает результаты в конце.

*Ссылка на Telegram-бота: 

[@funny_quiz_game_bot](https://t.me/funny_quiz_game_bot)

*Структура проекта:
- main.py                 # Точка входа. Запуск бота.
- handle_button.py        # Обработка команд и логика квиза.
- asynchronous_db.py      # Работа с базой данных (SQLite).
- questions_answers.py    # Список вопросов и ответов.
- README.md               # Документация.

*Как запустить:

1. Установите зависимости:
- pip install aiogram
- pip install aiosqlite
2. Убедитесь, что в main.py указан корректный токен бота от BotFather: API_TOKEN = 'ВАШ_ТОКЕН'
3. Запустите бота: python main.py

*Команды бота и их описания:
- /start - Приветственное сообщение и кнопка "Начать игру".
- /quiz или Начать игру -	Запуск новой игры. Бот начинает задавать вопросы.
- Пройти заново -	Начинает квиз заново после завершения.
- Варианты ответов - Выбираются нажатием на кнопки под вопросом. Бот сообщает, верен ли ответ, и переходит к следующему.

*Хранение данных:
- Используется база данных quiz_bot.db на основе aiosqlite.
- Для каждого пользователя сохраняются текущий индекс вопроса и количество правильных ответов.
