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


@router.callback_query(F.data == 'bot_help')
async def get_help(callback: types.CallbackQuery):
    await callback.message.edit_text(
        core.locale.help,
        reply_markup=core.keyboards.iclose_keyboard
    )


@router.callback_query(F.data == 'set_timezone')
async def get_timezone(callback: types.CallbackQuery):
    await callback.message.edit_text(
        core.locale.set_timezone,
        reply_markup=core.keyboards.close_keyboard()
    )


@router.callback_query(F.data == 'set_reminder')
async def option_set_reminder(callback: types.CallbackQuery, state=FSMContext):
    await state.set_state(SetReminder.reminder_type_input)
    await callback.message.answer(core.locale.reminder_type)


@router.message(SetReminder.reminder_type_input)
async def get_reminder_type(message: types.Message, state: FSMContext):
    if message.text == core.locale.periodic:
        await state.set_state(SetReminder.reminder_period_input)
        await message.answer(core.locale.reminder_period)
    else:
        await state.set_state(SetReminder.reminder_time_input)
        await message.answer(core.locale.reminder_time)
    await state.update_data(reminder_type=message)


@router.message(SetReminder.reminder_period_input)
async def get_reminder_period(message: types.Message, state: FSMContext):
    await state.set_state(SetReminder.reminder_text_input)
    await state.update_data(reminder_period=message)
    await message.answer(core.locale.reminder_text)


@router.message(SetReminder.reminder_time_input)
async def get_reminder_time(message: types.Message, state: FSMContext):
    await state.set_state(SetReminder.reminder_text_input)
    await state.update_data(reminder_time=message)
    await message.answer(core.locale.reminder_text)


@router.message(SetReminder.reminder_text_input)
async def get_reminder_text(message: types.Message, state: FSMContext):
    await state.set_state(SetReminder.setting_reminder)
    await state.update_data(reminder_text=message, user_id=message.from_user.id)
    await message.answer(core.locale.confirm)


@router.message(SetReminder.setting_reminder)
async def set_reminder(message: types.Message, state: FSMContext):
    # if message.text == core.locale.yes:
    print('gay')
    data = await state.get_data()
    print(data)
    user_id, repeat, period, text = data['user_id'], False, '0', data['reminder_text']
    if data['reminder_type'] == core.locale.periodic:
        repeat, period = True, ''.join(data['reminder_period'].split())
    time = data['reminder_time']
    print(user_id, repeat, period, text, time)
    async with aiosqlite.connect(settings.bot.DB_PATH) as db:
        print('gay')
        await db.execute(f'''UPDATE reminders
            SET text, time, user_id, repeat, period = {text}, {time}, {user_id}, {repeat}, {period}''')
        print('as')
    await message.answer(core.locale.reminder_set)
    await state.clear()

# pass


@router.callback_query(F.data == 'add_file')
async def file_options_choice(callback: types.CallbackQuery):
    await callback.message.edit_text(
        core.locale.file_awaiting,
        reply_markup=core.keyboards.close_keyboard())
