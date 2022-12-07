import logging
from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from states import MenuSettingState


@dp.message_handler(text = "secret")
async def menu_setting_start(message : types.Message):
    logging( "Admin - secret word")
    await message.answer("ты в админпанеле")


#start point and requesting photo
@dp.message_handler(text = "Add_to_menu")
async def menu_setting_start(message : types.Message):
    await MenuSettingState.photo.set()
    await message.answer("Загрузи фото прикольдеса")


#next state - adding photo and requesting product name
@dp.message_handler(content_types=['photo'], state=MenuSettingState.photo)
async def menu_setting_ser_photo(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    
    await MenuSettingState.next()
    await message.answer("Как назовешь ета чуда?")


#get second answer
@dp.message_handler(state=MenuSettingState.name)
async def menu_setting_set_name(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    
    await FSMContext.next()
    await message.answer("Опиши канфету")


#set description 
@dp.message_handler(state=MenuSettingState.name)
async def menu_setting_set_desc(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    
    await FSMContext.next()
    await message.answer("Сколько мелеардов за эту усладу?")

    
#set price 
@dp.message_handler(state=MenuSettingState.name)
async def menu_setting_set_price(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    
    await message.answer("Готова")
    await state.finish()
    
    