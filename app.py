from aiogram import executor
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import asyncio
from loader import dp
import logging

from middlewares.throttling import ThrottlingMiddleware

# from handlers.users import register_start
# from handlers.errors import register_error

# Configure logging
logging.basicConfig(level=logging.INFO)

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.sql import dbwork

async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    logging.info("func on_startup ends succesfully")


async def main():      

    await on_startup(dp)
    print("Отправил администраторам сообщения.")

    dp.middleware.setup(ThrottlingMiddleware())

    # register_start(dp)
    # register_error(dp)
    print("Все хендлеры работают.")

    # try:
        
        
    # finally:
    #     await dp.storage.close()
    #     await dp.storage.wait_closed()
    #     await dp.bot.session.close()

if __name__ == '__main__':
    logging.info(f"DP: {dp}\n Bot: {dp.bot}")
    executor.start_polling(dp, on_startup=on_startup)

@dp.message_handler(commands=['start', 'help'])
async def bot_start(message: types.Message):
    logging.info("Command start")
    await message.answer(f"Привет, {message.from_user.full_name}!")

