from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Старт'
        ),
        BotCommand(
            command='cancel',
            description='Отмена операции'
        ),
        BotCommand(
            command='menu',
            description='Вызов меню'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
