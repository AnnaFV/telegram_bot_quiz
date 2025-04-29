from aiogram.filters.command import Command
from aiogram import types, Dispatcher, F
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from questions_answers import quiz_data
from asynchronous_db import save_quiz_state, get_quiz_state

# Создаем диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем клавиатуру с кнопкой "Начать игру"
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer(
        "Добро пожаловать в квиз! Для начала игры нажми на кнопку 'Начать игру' или отправь команду /quiz",
        reply_markup=builder.as_markup(resize_keyboard=True))


# Хэндлер на команды /quiz и кнопки "Начать игру" и "Пройти заново"
@dp.message(F.text.in_(["Начать игру", "Пройти заново"]))
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Получаем ID пользователя, чтобы сохранить состояние квиза
    user_id = message.from_user.id
    # Сброс состояния: начинаем с первого вопроса и нуля правильных ответов
    await save_quiz_state(user_id, 0, 0)
    # Убираем клавиатуру, чтобы не было кнопок во время игры
    await message.answer("Давайте начнем квиз!", reply_markup=types.ReplyKeyboardRemove())
    # Запускаем квиз
    await new_quiz(message)


# Начало нового квиза
async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    # Сохраняем начальное состояние с нулём правильных ответов
    await save_quiz_state(user_id, current_question_index, 0)
    # Показываем первый вопрос
    await get_question(message, user_id)


# Получение текущего вопроса и отправка его пользователю
async def get_question(message, user_id):
    # Получаем индекс текущего вопроса из базы данных
    current_question_index, _ = await get_quiz_state(user_id)
    question = quiz_data[current_question_index]
    correct_index = question['correct_option']
    options = question['options']
    # Генерируем клавиатуру с вариантами ответов
    kb = generate_options_keyboard(options, options[correct_index])
    # Отправляем текст вопроса с кнопками
    await message.answer(question['question'], reply_markup=kb)


# Генерация клавиатуры с вариантами ответов
def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer"
        ))
    builder.adjust(1)
    return builder.as_markup()


# Обработка ответа пользователя
async def handle_answer(callback, is_correct):
    # Удаляем старую клавиатуру с кнопками
    await callback.bot.edit_message_reply_markup(chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None)
    # Получаем текущий индекс вопроса и количество правильных ответов
    current_question_index, correct_answers = await get_quiz_state(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    correct_text = quiz_data[current_question_index]['options'][correct_option]
    # Отправляем сообщение в зависимости от ответа
    if is_correct:
        await callback.message.answer(f"✅ Правильно! Ваш ответ: {correct_text}")
        correct_answers += 1  # Увеличиваем счетчик
    else:
        await callback.message.answer(f"❌ Неправильно. Правильный ответ: {correct_text}")
    # Сохраняем новое состояние с увеличенным индексом вопроса
    await save_quiz_state(callback.from_user.id, current_question_index + 1, correct_answers)
    # Переходим к следующему вопросу или завершаем квиз
    await proceed_to_next_question(callback.message, callback.from_user.id, current_question_index + 1, correct_answers)
    
    
# Переход к следующему вопросу или завершение квиза
async def proceed_to_next_question(message, user_id, current_question_index, correct_answers):
    if current_question_index < len(quiz_data):
        await get_question(message, user_id)
    else:
        await finish_quiz(message, correct_answers)


# Завершение квиза и вывод результатов
async def finish_quiz(message, correct_answers):
    # Сообщение с результатами
    await message.answer(
        f"Это был последний вопрос.\n"
        f"Вы набрали {correct_answers} из {len(quiz_data)} правильных ответов!"
    )
    # Кнопка "Пройти заново"
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Пройти заново"))
    # Возвращаем клавиатуру после завершения игры
    await message.answer("Хотите попробовать еще раз? Нажмите на кнопку 'Пройти заново'.", reply_markup=builder.as_markup(resize_keyboard=True))


# Обработка правильного ответа
@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await handle_answer(callback, is_correct=True)


# Обработка неправильного ответа
@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await handle_answer(callback, is_correct=False)
