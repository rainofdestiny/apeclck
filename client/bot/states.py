from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class ShortenerSG(StatesGroup):
    ENTER_NAME = State()
    ENABLE_LOGGER = State()
    TTL = State()
