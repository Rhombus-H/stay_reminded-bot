import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from core.middleware import settings
from core.handlers import router
# from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def start():
    logging.basicConfig(
        level=logging.INFO,
        filename='bot.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    bot = Bot(token=settings.TOKEN_API_KEY)

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    # scheduler = AsyncIOScheduler()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
