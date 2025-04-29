import aiosqlite

# Зададим имя базы данных
DB_NAME = 'quiz_bot.db'

# Функция для создания таблицы
async def create_table():
    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Выполняем SQL-запрос к базе данных
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (
            user_id INTEGER PRIMARY KEY, 
            question_index INTEGER,
            correct_answers INTEGER)''')
        # Сохраняем изменения
        await db.commit()

# Функция, которая сохраняет или обновляет номер текущего вопроса для конкретного пользователя в базе данных и правильные ответы
async def save_quiz_state(user_id, index, correct_answers):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('''INSERT OR REPLACE INTO quiz_state (user_id, question_index, correct_answers) 
                         VALUES (?, ?, ?)''', (user_id, index, correct_answers))
        # Сохраняем изменения
        await db.commit()

# Функция, которая получит текущее состояние в базе данных для заданного пользователя       
async def get_quiz_state(user_id):
    # Подключаемся к базе данных
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index, correct_answers FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0], results[1]  # возвращаем оба значения
            else:
                return 0, 0  
