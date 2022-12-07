from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command

from states import OrderState

@dp.message_handler(Command("Order"))
async def order_mh(message: types.Message):
    await message.answer("Вы запустили форму заказа")

    await OrderState.O1.set()