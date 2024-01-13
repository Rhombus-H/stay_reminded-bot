from aiogram.filters.state import StatesGroup, State


class SetReminder(StatesGroup):
    reminder_text_input = State()
    reminder_time_input = State()
