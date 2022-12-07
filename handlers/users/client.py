from aiogram import types
from loader import dp, bot

@dp.message_handler(commands=['start', 'help'])
async def command_start(msg : types.Message):
    await bot.send_message(msg.from_user.id, 'Хало')
            # await
        # except:
        #     await

