import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from dotenv import load_dotenv
import os

from handler.test_drive import test_drive_message
from state.car_massive import CarState
from state.register import RegisterState
from utils.commands import set_commands
from handler.start import get_start
from handler.register import start_register, register_name, register_surname, register_phone
from handler.setDBData import delete_account, delete_account_confirmation
from handler.car_info import send_images_from_database, select_countries, bot_help

#Получения токена подключения из .env
load_dotenv()
token = os.getenv('token')
admin_id = os.getenv('admin_id')


#Подключение по токену к апи
bot = Bot(token=token)
dp = Dispatcher()


#Регаем хендлер регистрации
dp.message.register(start_register, F.text == '🟢 Зарегистироваться 🟢')
dp.message.register(register_name, RegisterState.reg_name)
dp.message.register(register_surname, RegisterState.reg_surname)
dp.message.register(register_phone, RegisterState.reg_phone)

# dp.message.register(delete_account, Command(commands='delete_account'))
dp.message.register(delete_account_confirmation, Command(commands='delete_account'))
dp.callback_query.register(delete_account, lambda c: c.data in ["confirm_delete", "cancel_delete"])

dp.message.register(send_images_from_database, Command(commands="car_info"))
dp.callback_query.register(select_countries, CarState.select_countries)

dp.message.register(test_drive_message, Command(commands='test_drive'))
dp.message.register(bot_help, Command(commands= 'help'))

#Функция старта бота
async def start():

    # dp.startup.register(start_bot)
    dp.message.register(get_start, Command(commands='start'))

    await set_commands(bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
