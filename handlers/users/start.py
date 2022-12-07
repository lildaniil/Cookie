from aiogram import types
import logging

from loader import dp


@dp.message_handler(commands=['start', 'help'])
async def bot_start(message: types.Message):
    logging.info("Command start")
    await message.answer(f"Привет, {message.from_user.full_name}!")

