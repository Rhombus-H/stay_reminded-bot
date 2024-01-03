import asyncio
from aiogram import types
import datetime
import dateparser


reminders = {}  # placeholder


# todo: add reminders_dic init here, not in the db_conn.py
async def set_reminder(chat_id, remind_time, message):
    # This function sets the reminder
    reminders[remind_time] = (chat_id, message)


async def reminder_checker(bot):
    # This function checks for due reminders
    while True:
        now = datetime.datetime.now()
        for remind_time in list(reminders.keys()):
            if now >= remind_time:
                chat_id, message = reminders[remind_time]
                await bot.send_message(chat_id, f'Напоминание: {message}')
                del reminders[remind_time]
        await asyncio.sleep(60)  # check every minute


async def remind_command(message: types.Message):
    # This handler will receive the remind command
    try:
        args = message.get_args().split(',')
        date_str, text = args[0], args[1]
        remind_date = dateparser.parse(date_str.strip())
        if remind_date:
            await set_reminder(message.chat.id, remind_date, text.strip())
            await message.reply(f'Reminder set for {remind_date}')
        else:
            await message.reply('Invalid date format. Please use YYYY-MM-DD HH:MM')
    except Exception as e:
        await message.reply(f'Error: {e}')
