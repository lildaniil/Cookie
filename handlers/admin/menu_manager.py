import logging

import asyncpg
from loader import dp, db
from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext

from states import MenuSettingState
from filters import IsAdmin

#adding to db
async def add_to_database(state, data):
    async with state.proxy() as data:
        print(type(data))

        try:
            menu_item = await db.add_menu_item(
                picture=data['photo'],
                product_name=data['name'],
                description=data['desc'],
                price=data['price']
            )

            logging.info("Item has been added to menu table")
        except asyncpg.exceptions.UniqueViolationError:
            print("Exeption !!")


#start point and requesting photo
@dp.message_handler(IsAdmin(), Command("addtomenu"), )
async def menu_setting_start(message : types.Message):
    print("________________________ADD______________________")
    await MenuSettingState.photo.set()
    await message.answer("Загрузи фото прикольдеса")


#next state - adding photo and requesting product name
@dp.message_handler(content_types=['photo'], state=MenuSettingState.photo)
async def menu_setting_ser_photo(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    
        await message.answer("Как назовешь ета чуда?")
        await MenuSettingState.next()


#get second answer
@dp.message_handler(state=MenuSettingState.name)
async def menu_setting_set_name(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    
    await message.answer("Опиши канфету")
    await MenuSettingState.next()


#set description 
@dp.message_handler(state=MenuSettingState.description)
async def menu_setting_set_desc(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    
    await message.answer("Сколько мелеардов за эту усладу?")
    await MenuSettingState.next()

    
#set price and add to DB
@dp.message_handler(state=MenuSettingState.price)
async def menu_setting_set_price(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)

    # todo add to db
    await add_to_database(state=state,data=data)
    
    await state.finish()
    await message.answer("Готова")
    

# # Quit from states using key word 
# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
# async def menu_cancel(message : types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.finish()
#     await message.answer("Отмена")
