import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from core.handlers import router
from core.config_parser import load_config
from core.commands import set_commands
# from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def start():
    logging.basicConfig(
        level=logging.INFO,
        filename='bot.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    settings = load_config('config.ini')
    bot = Bot(token=settings.bot.TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await set_commands(bot)
    # scheduler = AsyncIOScheduler()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
