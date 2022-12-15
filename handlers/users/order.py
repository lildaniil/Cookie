from loader import dp, db
from aiogram import types
from aiogram.dispatcher.filters import Command

from states import OrderState

@dp.message_handler(Command("Order"))
async def order_mh(message: types.Message):
    await message.answer("Вы запустили форму заказа")
    users = await db.select_all_users()
    # await OrderState.O1.set()

@dp.message_handler(Command("Menu"))
async def show_menu(message: types.Message):
    await message.answer("Вы запустили демонстрацию меню")
    menu_items = await db.select_all_menu_items()

    
    for item in menu_items:
        print("------")
        print(item[0])
        a = f"""Photo: {item[1]}"""
        print(a)
        print(type(a))
        await dp.bot.send_photo(
        chat_id=message.from_user.id,
        photo=item[1],
        caption=
            f'<b>{item[2]}</b>\n\n'
            f'<i>{item[3]}</i>\n\n'
            f'Цена: {item[4]} рублей'           
        )