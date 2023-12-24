from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_API_KEY = os.getenv(
    'TOKEN_API_KEY',
    '123123123123123123',  # placeholder for a key
)

bot = Bot(TOKEN_API_KEY)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text=message.text)


if __name__ == '__main__':
    executor.start_polling()
