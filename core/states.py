from aiogram.filters.state import StatesGroup, State


class UploadFile(StatesGroup):
    type_choice = State()
    file_await = State()
