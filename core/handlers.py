import aiosqlite
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import core.locale
import core.keyboards
from core.states import SetReminder, SetTimezone
from core.config_parser import load_config
import datetime
import aiosqlite
import re

router = Router()

settings = load_config('config.ini')


@router.message(Command('start'))
async def start(message: types.Message):
    db = await aiosqlite.connect(settings.bot.DB_PATH)
    cur = await db.cursor()
    await cur.execute(f'INSERT OR IGNORE INTO users (user_id) VALUES ({message.from_user.id})')
    print('ase')
    await db.commit()
    await cur.close()
    await db.close()
    await message.answer(
        core.locale.start,
        reply_markup=core.keyboards.main_table)


@router.message(Command('cancel'))
async def cancel(message: types.Message, state: FSMContext):
    if state.get_state():
        await state.clear()
        await message.answer(core.locale.cancel)


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
        core.locale.bot_help,
        reply_markup=core.keyboards.iclose_keyboard
    )


@router.callback_query(F.data == 'set_timezone' or SetTimezone.timezone_input)
async def set_timezone(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SetTimezone.timezone_input)
    await callback.message.edit_text(core.locale.set_timezone)


@router.message(SetTimezone.timezone_input)
async def get_timezone(message: types.Message, state: FSMContext):
    pattern = re.compile(r'^UTC([+-]1[0-2]|-[0-9]|[0-9])$')
    if re.match(pattern, message.text):
        db = await aiosqlite.connect(settings.bot.DB_PATH)
        cur = await db.cursor()
        await cur.execute('UPDATE users SET timezone = (?, )', (message.text, ))
        await db.commit()
        await cur.close()
        await db.close()
        await state.clear()
        return await message.answer()

    else:
        return await message.answer(core.locale.time_zone_invalid)



@router.callback_query(F.data == 'delete_reminder')
async def delete_reminder(callback: types.CallbackQuery):
    pass  # todo: вызов списка напоминалок как клавиатуры и последующие действия с каждым


@router.callback_query(F.data == 'set_reminder')
async def option_set_reminder(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SetReminder.reminder_type_input)
    await callback.message.edit_text(core.locale.reminder_type)


@router.message(SetReminder.reminder_type_input)
async def get_reminder_type(message: types.Message, state: FSMContext):
    await message.answer(core.locale.reminder_time)
    await state.set_state(SetReminder.reminder_time_input)
    await state.update_data(reminder_type=message.text)


@router.message(SetReminder.reminder_time_input)
async def get_reminder_time(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(reminder_time=message.text)
    if data['reminder_type'] == core.locale.periodic:
        print('ы')
        await state.set_state(SetReminder.reminder_period_input)
        await message.answer(core.locale.reminder_period)
    else:
        print('s')
        await state.set_state(SetReminder.reminder_text_input)
        await message.answer(core.locale.reminder_text)


@router.message(SetReminder.reminder_period_input)
async def get_reminder_period(message: types.Message, state: FSMContext):
    await state.set_state(SetReminder.reminder_text_input)
    await state.update_data(reminder_period=message.text)
    await message.answer(core.locale.reminder_text)


@router.message(SetReminder.reminder_text_input)
async def get_reminder_text(message: types.Message, state: FSMContext):
    await state.set_state(SetReminder.setting_reminder)
    await state.update_data(reminder_text=message.text, user_id=message.from_user.id)
    await message.answer(core.locale.confirm)


@router.message(SetReminder.setting_reminder)
async def set_reminder(message: types.Message, state: FSMContext):
    # if message.text == core.locale.yes:
    print('test')
    data = await state.get_data()
    print(data)
    user_id, period, time, text = data['user_id'], '0', data['reminder_time'], data['reminder_text']
    if data['reminder_type'] == core.locale.periodic:
        period = ','.join(data['reminder_period'].split()).lower()
        query = '''INSERT INTO reminders (text, time, user_id, period) VALUES (?, ?, ?, ?);'''
    else:
        query = '''INSERT INTO reminders (text, time, user_id) VALUES (?, ?, ?);'''
        print('1')
    db = await aiosqlite.connect(settings.bot.DB_PATH)
    cur = await db.cursor()
    await cur.execute(query, (text, time, user_id, period))
    print('sdsd')
    await db.commit()
    await cur.close()
    await db.close()
    await message.answer(core.locale.reminder_set)
    await state.clear()

# pass


@router.callback_query(F.data == 'add_file')
async def file_options_choice(callback: types.CallbackQuery):
    await callback.message.edit_text(
        core.locale.file_awaiting,
        reply_markup=core.keyboards.close_keyboard())
