import aiosqlite
from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import core.locale
import core.keyboards
from core.states import SetReminder, SetTimezone, GetFile, DeleteReminder
from core.config_parser import load_config
import core.utils
import datetime
import aiosqlite
import re

router = Router()

settings = load_config('config.ini')


@router.message(Command('start'))
async def start(message: types.Message):
    db = await aiosqlite.connect(settings.bot.DB_PATH)
    cur = await db.cursor()
    await cur.execute(f'INSERT OR IGNORE INTO users (id) VALUES ({message.from_user.id})')
    print('ase')
    await db.commit()
    await cur.close()
    await db.close()
    await message.answer(
        core.locale.start,
        reply_markup=core.keyboards.main_table)


@router.message(Command('cancel'))
async def cancel(message: types.Message, state: FSMContext):
    if await state.get_state():
        await state.clear()
        await message.answer(core.locale.cancel, reply_markup=core.keyboards.main_table)


@router.message(Command('menu'))
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


async def list_reminders(reminders):
    reminders_list = []
    for i in enumerate(reminders, start=1):
        n, reminder = i
        if reminder['period'] != 'none':
            reminders_list.append([
                InlineKeyboardButton(text=f'"{reminder['text']}" на {reminder['time']} ({reminder['period']})',
                                     callback_data=f'{n}')
            ])
        else:
            reminders_list.append([
                InlineKeyboardButton(text=f'"{reminder['text']}" на {reminder['time']}',
                                     callback_data=f'{n}')
            ])
    if reminders_list:
        reminders_list.append([InlineKeyboardButton(text='Закрыть ❌', callback_data='close_reminders_list')])
        reminders_list = InlineKeyboardMarkup(inline_keyboard=reminders_list)
    return reminders_list


@router.callback_query(F.data == 'close_reminders_list')
async def close_reminders_list(callback: types.CallbackQuery):
    await callback.message.edit_text(text='Закрыто', reply_markup=core.keyboards.main_table)


@router.callback_query(F.data == 'list_reminders')
async def get_list_reminders(callback: types.CallbackQuery):
    db = await aiosqlite.connect(settings.bot.DB_PATH)
    db.row_factory = aiosqlite.Row
    cur = await db.execute(f'''SELECT text, time, period FROM reminders WHERE user_id = {callback.from_user.id}''')
    data = await cur.fetchall()
    reminders_list = await list_reminders(data)
    await cur.close()
    await db.close()
    if reminders_list:
        await callback.message.edit_text(core.locale.reminders_list, reply_markup=reminders_list)
    else:
        await callback.message.edit_text(core.locale.no_reminders_found, reply_markup=core.keyboards.main_table)


@router.message(SetTimezone.timezone_input)
async def get_timezone(message: types.Message, state: FSMContext):
    pattern = re.compile(r'^UTC([+-]1[0-2]|-[0-9]|[0-9])$')
    if re.match(pattern, message.text):
        db = await aiosqlite.connect(settings.bot.DB_PATH)
        await db.execute('UPDATE users SET timezone = ? WHERE id = ?',
                         (message.text, message.from_user.id))
        await db.commit()
        await db.close()
        await state.clear()
        return await message.answer(core.locale.timezone_set)

    return await message.answer(core.locale.timezone_format_invalid)


@router.callback_query(F.data == 'delete_reminder')
async def reminder_del_choice(callback: types.CallbackQuery, state: FSMContext):
    db = await aiosqlite.connect(settings.bot.DB_PATH)
    db.row_factory = aiosqlite.Row
    cur = await db.execute(f'''SELECT text, time, period FROM reminders WHERE user_id = {callback.from_user.id}''')
    data = await cur.fetchall()
    reminders_to_del = await list_reminders(data)
    print(reminders_to_del)
    reminders = {}
    for i in enumerate(data):
        n, reminder = i
        reminders[reminders_to_del.inline_keyboard[n][0].callback_data] = dict(reminder)
    print(reminders)
    await db.close()
    print(reminders_to_del)
    await callback.message.edit_text(core.locale.delete_reminder, reply_markup=reminders_to_del)
    await state.set_state(DeleteReminder.awaiting_reminder_name)
    await state.update_data(reminders=reminders)


@router.message(DeleteReminder.awaiting_reminder_name)
async def delete_reminder(callback: types.CallbackQuery, state: FSMContext):
    reminders_to_del = await state.get_data()
    reminders_to_del = reminders_to_del['reminders']
    db = await aiosqlite.connect(settings.DB_PATH)
    cur = await db.execute(f'''DELETE FROM reminders WHERE user_id, text, time = (?, ?, ?)''',
                           (reminders_to_del[callback.data]['user_id'],
                            reminders_to_del[callback.data]['text'],
                            reminders_to_del[callback.data]['time']))
    await db.commit()
    await cur.close()
    await db.close()
    await callback.message.edit_text(core.locale.reminder_deleted.format(
        f'"{reminders_to_del[callback.data]['text']}" на {reminders_to_del[callback.data]['time']}'),
        reply_markup=core.keyboards.main_table)


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
    if re.match(re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'), message.text):
        await state.update_data(reminder_time=message.text)
        if data['reminder_type'] == core.locale.periodic:
            print('ы')
            await state.set_state(SetReminder.reminder_period_input)
            await message.answer(core.locale.reminder_period)
        else:
            print('s')
            await state.set_state(SetReminder.reminder_date_input)
            print('((')
            await message.answer(core.locale.reminder_date)
    else:
        await message.answer(core.locale.time_format_invalid)


@router.message(SetReminder.reminder_date_input)
async def get_reminder_date(message: types.Message, state: FSMContext):
    today = datetime.date.today().strftime('%d.%m')
    if datetime.datetime.strptime(today, '%d.%m') <= datetime.datetime.strptime(message.text, '%d.%m'):
        data = await state.get_data()
        time = datetime.datetime.strptime(data['reminder_time'], '%H:%M').time()
        date = message.text
        print(time)
        print(datetime.datetime.now().hour, datetime.datetime.now().minute)
        print('.'.join(datetime.datetime.now().date().strftime('%Y-%m-%d').split('-')[1:][::-1]))
        print(date)
        if datetime.datetime.strptime(today, '%d.%m') <= datetime.datetime.strptime(date, '%d.%m') and \
                time > datetime.datetime.now().time():
            print('dsd')
            await state.update_data(date=date)
            await state.set_state(SetReminder.reminder_text_input)
            await message.answer(core.locale.reminder_text)
        else:
            await message.answer(core.locale.time_selected_invalid)
    else:
        await message.answer(core.locale.time_format_invalid)


@router.message(SetReminder.reminder_period_input)
async def get_reminder_period(message: types.Message, state: FSMContext):
    weekdays = set(core.utils.WEEKDAYS.keys())
    if not set(message.text.lower().split()) & weekdays:
        await message.answer(core.locale.period_format_invalid)
    else:
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
    if message.text.lower() == core.locale.yes:
        print('test')
        data = await state.get_data()
        print(data)
        user_id, period, time, text = data['user_id'], '0', data['reminder_time'], data['reminder_text']
        db = await aiosqlite.connect(settings.bot.DB_PATH)
        cur = await db.execute('SELECT timezone FROM users WHERE id = ?', (user_id,))
        print('sir')
        timezone = await cur.fetchone()
        timezone = timezone[0]
        if data['reminder_type'] == core.locale.periodic:
            period = ', '.join(data['reminder_period'].split()).lower()
            print(text, time, user_id, period, timezone)
            query = '''INSERT INTO reminders (text, time, user_id, period, timezone) VALUES (?, ?, ?, ?, ?)'''
            cur = await db.execute(query, (text, time, user_id, period, timezone))
            print('2')
        else:
            date = data['reminder_time']
            time = date + ' ' + data['date']
            query = '''INSERT INTO reminders (text, time, user_id, timezone) VALUES (?, ?, ?, ?);'''
            cur = await db.execute(query, (text, time, user_id, timezone))
            print('1')
        await db.commit()
        await cur.close()
        await db.close()
        print('sdsd')
        await message.answer(core.locale.reminder_set, reply_markup=core.keyboards.main_table)
        await state.clear()
    else:
        await message.answer(text=core.locale.abort_notifier_creation)
        await state.set_state(SetReminder.abort_creation)


@router.message(SetReminder.abort_creation)
async def cancel_notifier_creation(message: types, state: FSMContext):
    if message.text.lower() == core.locale.yes:
        await message.answer(core.locale.cancel, reply_markup=core.keyboards.main_table)
        await state.clear()


@router.callback_query(F.data == 'add_file')
async def file_option_choice(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(GetFile.file_awaiting)
    await callback.message.edit_text(
        core.locale.file_awaiting)


@router.message(GetFile.file_awaiting)
async def add_file(message: types.Message, state: FSMContext):
    if message.content_type != types.ContentType.DOCUMENT:
        await message.answer(core.locale.file_invalid)
    else:
        db = await aiosqlite.connect(settings.bot.DB_PATH)
        print('sugoma')
        query = '''INSERT INTO files (file_id, name, user_id) VALUES (?, ?, ?);'''
        await db.execute(query, (message.document.file_id, message.document.file_name, message.from_user.id))
        print('adasdsadas')
        await db.commit()
        await db.close()
        await state.clear()
        await message.answer(core.locale.file_success, reply_markup=core.keyboards.main_table)


@router.callback_query(F.data == 'list_files')
async def list_files(callback: types.CallbackQuery, state: FSMContext):
    db = await aiosqlite.connect(settings.bot.DB_PATH)
    cursor = await db.execute(f'''SELECT file_id, name FROM files''')
    data = await cursor.fetchall()
    await state.clear()
    if data:
        await callback.message.edit_text(core.locale.file_list, reply_markup=core.keyboards.files_list(data))
    else:
        await callback.message.edit_text(core.locale.file_list_empty, reply_markup=core.keyboards.main_table)
