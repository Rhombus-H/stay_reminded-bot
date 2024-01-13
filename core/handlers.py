import aiosqlite
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import core.locale
import core.keyboards
from core.states import SetReminder
from core.config_parser import load_config
import datetime
import aiosqlite

router = Router()

settings = load_config('config.ini')


@router.message(Command('start'))
async def start(message: types.Message):
    async with aiosqlite.connect(settings.bot.DB_PATH) as db:
        await db.execute(f'UPDATE users SET user_id = ?', (message.from_user.id,))
    await message.answer(
        core.locale.start,
        reply_markup=core.keyboards.main_table)


@router.message(Command('cancel'))
async def cancel(message: types.Message):
    await message.answer(
        core.locale.cancel,
        reply_markup=core.keyboards.main_table)


@router.message(F.text == 'Меню')
@router.message(F.text == 'В меню')
@router.message(F.text == 'В главное меню')
async def menu(message: types.Message):
    await message.answer(
        core.locale.in_the_menu,
        reply_markup=core.keyboards.main_table)


@router.callback_query(F.data == 'set_timezone')
async def get_timezone(callback: types.CallbackQuery):
    await callback.message.edit_text(
        core.locale.set_timezone,
        reply_markup=core.keyboards.close_keyboard()
    )


@router.callback_query(F.data == 'set_reminder')
async def get_reminder_text(callback: types.CallbackQuery, state=FSMContext):
    await state.set_state(SetReminder.reminder_text_input)
    await callback.message.answer(core.locale.reminder_text)


@router.message(SetReminder.reminder_text_input)
async def get_reminder_time(message: types.Message, state: FSMContext):
    await state.set_state(SetReminder.reminder_time_input)
    await state.update_data(reminder_text=message)
    await message.reply(core.locale.reminder_text)


@router.message(SetReminder.reminder_time_input)
async def set_reminder(message: types.Message, state: FSMContext):
    reminder_data = state.get_data()


@router.callback_query(F.data == 'add_file')
async def file_options_choice(callback: types.CallbackQuery):
    await callback.message.edit_text(
        core.locale.file_awaiting,
        reply_markup=core.keyboards.close_keyboard())
