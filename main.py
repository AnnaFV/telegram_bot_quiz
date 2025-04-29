import asyncio
import logging
from aiogram import Bot, F
from handle_button import dp
from asynchronous_db import create_table

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Токен, который был получен от BotFather при создании бота
API_TOKEN = '7241589154:AAF8AdCDmMMFl8Gcbsoan7sTmJbWFYZP0us'

# Объект бота
bot = Bot(token=API_TOKEN)

# Связываем объект бота с диспетчером
dp.bot = bot

# Запуск процесса поллинга новых апдейтов
async def main():
    # Запускаем создание таблицы базы данных
    await create_table()
    # Запускаем процесс опроса (polling) для обработки входящих сообщений
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
