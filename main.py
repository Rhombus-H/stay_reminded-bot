import asyncio
from aiogram import Bot, Dispatcher
from core.handlers.base import get_started, bot_shutdown, bot_startup
from core.handlers.reminder import remind_command, reminder_checker
from core.middleware.database_connect import init_reminder_dic
import logging
from core.middleware import settings


async def start():
    logging.basicConfig(
        level=logging.INFO,
        filename='bot_log.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    reminders_dic = init_reminder_dic()

    bot = Bot(token=settings.TOKEN_API_KEY)

    dp = Dispatcher()

    dp.startup.register(bot_startup(bot, admin_chat_id=settings.ADMIN_ID))
    dp.shutdown.register(bot_shutdown(bot, admin_chat_id=settings.ADMIN_ID))

    dp.register_message_handler(remind_command, commands=['remind'], state='*')
    await asyncio.create_task(reminder_checker(bot))
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
