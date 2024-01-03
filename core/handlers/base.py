from aiogram import Bot, types


async def get_started(message: types.Message, bot: Bot):
    await message.answer(f'Hi {message.from_user.first_name}')
    # await message.reply(f'Hi {message.from_user.first_name}')


async def bot_shutdown(bot: Bot, admin_chat_id: int | str):
    await bot.send_message(admin_chat_id, text="Бот остановлен.")


async def bot_startup(bot: Bot, admin_chat_id: int | str):
    await bot.send_message(admin_chat_id, text="Бот запущен.")
