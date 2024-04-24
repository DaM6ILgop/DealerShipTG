from aiogram import Bot
from aiogram.types import Message

from keyboards.register_kb import register_bttn

#Главная функция старта.
async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'👋 Здравствуйте! Рад видеть вас! 🎉 \n'
                                                 f' 🚗 Бот поможет вам выбрать автомобиль для покупки. 🚙💨\n', reply_markup=register_bttn)