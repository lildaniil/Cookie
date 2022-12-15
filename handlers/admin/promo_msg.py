import logging

import asyncpg
from loader import dp, db
from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext

from states import MenuSettingState
from filters import IsAdmin