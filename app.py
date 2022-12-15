from aiogram import executor
from aiogram import types
import logging

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):


    #Connecting to database and creating a table
    logging.info("Database connecting...")
    await db.create()
    logging.info("Database connected!")
    logging.info("Creating a tables...")
    await db.create_table_users()
    logging.info("Table Users - ok!")
    await db.create_table_menu()
    logging.info("Table Menu - ok!")

    logging.info("Database is ready")



    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

