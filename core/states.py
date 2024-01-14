from aiogram.filters.state import StatesGroup, State


class SetReminder(StatesGroup):
    reminder_type_input = State()
    reminder_text_input = State()
    reminder_period_input = State()
    reminder_time_after_period = State()
    reminder_time_input = State()
    setting_reminder = State()
