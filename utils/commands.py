from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

#Команды бота
async def set_commands(bot:Bot):
    commands = [
        BotCommand(
            command='start',
            description='Запуск бота'
        ),
        BotCommand(
            command='car_info',
            description='Показывает информацию по имеющимся автомобилям'
        ),
        BotCommand(
            command='test_drive',
            description='Заказать тест драйв'
        ),
        BotCommand(
            command='delete_account',
            description='Удалить аккаунт'
        ),
        BotCommand(
            command='help',
            description='Тех.поодержка'
        )

    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())