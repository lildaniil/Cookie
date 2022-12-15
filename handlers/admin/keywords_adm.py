import logging

import asyncpg
from loader import dp, db
from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext

from states import MenuSettingState
from filters import IsAdmin


@dp.message_handler(IsAdmin(), text = "secret")
async def menu_setting_start_secret(message : types.Message):
    print("________________________secret______________________")
    # logging("Admin - secret word")
    await message.answer("ты в админ панеле")




# Quit from states using key word 
@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def menu_cancel(message : types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Отмена")