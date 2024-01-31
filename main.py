import asyncio
from datetime import datetime

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
    db = await aiosqlite.connect(settings.bot.DB_PATH)
    cursor = await db.execute(f'''SELECT * FROM reminders WHERE scheduled = 0''')
    data = await cursor.fetchall()
    # await db.execute(f'''UPDATE reminders SET scheduled = 1''')
    # await db.commit()
    await cursor.close()
    await db.close()
    print(apsched.get_jobs())
    for i in data:
        text, time, user_id, period, timezone = list(i)[1:6]
        hours = time.split(':')[0]
        minutes = time.split(':')[1]
        if period != 'none':
            apsched.add_job(
                reminder_task(bot=bot, chat_id=user_id, message=text),
                trigger='cron',
                start_date=datetime.now(),
                day_of_week=translate(period),
                hour=hours,
                minute=minutes,
                timezone=timezone + ':00'
            )
        else:
            apsched.add_job(
                reminder_task(bot=bot, chat_id=user_id, message=text),
                trigger='date'
            )
        apsched.start()


async def start():
    logging.basicConfig(
        level=logging.INFO,
        filename='bot.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    bot = Bot(token=settings.bot.TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    await set_commands(bot)
    # scheduler = AsyncIOScheduler()
    # apsched.add_job(schedule_reminders, trigger='interval', seconds=2, kwargs={'bot': bot})
    # apsched.start()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
