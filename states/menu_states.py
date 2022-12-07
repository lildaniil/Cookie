from aiogram.dispatcher.filters.state import StatesGroup, State

class MenuSettingState(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()