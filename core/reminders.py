from aiogram import Bot, types
import aiosqlite
from core.config_parser import load_config


config = load_config('config.ini')

async def send_reminding_message(bot: Bot, message):
    async with aiosqlite.connect(config.bot.DB_PATH) as db:
        data = db.execute_fetchall(f'''SELECT from reminders WHERE''')