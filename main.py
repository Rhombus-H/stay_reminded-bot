import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import aiosqlite
import logging
from core.handlers import router
from core.config_parser import load_config
from core.commands import set_commands
from core.utils import translate
from apscheduler.schedulers.asyncio import AsyncIOScheduler

settings = load_config('config.ini')

apsched = AsyncIOScheduler()


async def reminder_task(bot: Bot, chat_id, message):
    await bot.send_message(chat_id=chat_id, text=message)


async def schedule_reminders(bot: Bot):
    async with aiosqlite.connect(settings.bot.DB_PATH) as db:
        data = await db.execute_fetchall(f'''SELECT * FROM reminders WHERE scheduled = 0''')
        await db.execute(f'''UPDATE reminders SET scheduled = 1 WHERE scheduled = 0''')
        await db.commit()
    for i in data:
        text, time, user_id, repeat, period = i[:5]
        hours = time.split(':')[0]
        minutes = time.split(':')[1]
        seconds = time.split(':')[2]
        apsched.add_job(
            reminder_task(bot=bot, chat_id=user_id, message=text),
            trigger='cron',
            day=translate(period),
            hour=hours,
            minute=minutes,
            second=seconds,
        )


async def start():
    logging.basicConfig(
        level=logging.INFO,
        filename='bot.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    bot = Bot(token=settings.bot.TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    apsched.add_job(schedule_reminders, args=[bot], trigger='interval', minutes=1)
    await set_commands(bot)
    # scheduler = AsyncIOScheduler()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
