from aiogram.filters.state import StatesGroup, State


class SetReminder(StatesGroup):
    reminder_type_input = State()
    reminder_text_input = State()
    reminder_date_input = State()
    reminder_period_input = State()
    reminder_time_after_period = State()
    reminder_time_input = State()
    setting_reminder = State()
    abort_creation = State()


class UploadFile(StatesGroup):
    file_awaiting = State()


class GetFile(StatesGroup):
    file_awaiting = State()


class DeleteReminder(StatesGroup):
    awaiting_reminder_name = State()
    reminder_deleted = State()


class SetTimezone(StatesGroup):
    timezone_input = State()