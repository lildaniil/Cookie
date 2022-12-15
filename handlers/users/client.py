from aiogram import types
import asyncpg.exceptions
from loader import dp, db, bot
from utils.db_api import postgresql 

from data import config

@dp.message_handler(commands=['start', 'help'])
async def command_start(msg : types.Message):
    await bot.send_message(msg.from_user.id, 'Хало')

    is_admin = False
    if str(msg.from_user.id) in config.ADMINS:
        is_admin = True

    print(
        f'''
        from user:{msg.from_user.full_name}
        user id:{msg.from_user.id}
        username:{msg.from_user.username}
        bot:{msg.from_user.is_bot}
        premium:{msg.from_user.is_premium}
        lang:{msg.from_user.language_code}
        {config.ADMINS}
        Is admin: {is_admin}           
        '''
        )

    try:
        user = await db.add_user(
            id=msg.from_user.id,
            first_name=msg.from_user.first_name,
            last_name=msg.from_user.last_name,
            username=msg.from_user.username,
            language_code=msg.from_user.language_code,
            is_premium=msg.from_user.is_premium,
            is_bot=msg.from_user.is_bot,
            supports_inline_queries=msg.from_user.supports_inline_queries
            )
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(id=msg.from_user.id)

    await bot.send_message(msg.from_user.id, 'Хало!')

    count_users = await db.count_user()
    print (count_users)
        
