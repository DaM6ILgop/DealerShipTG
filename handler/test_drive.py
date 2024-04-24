from aiogram.types import Message
from aiogram import Bot
from handler.setDBData import user_is_register


async def test_drive_message(message: Message, bot:Bot):
    if not await user_is_register(message.from_user.id):
        await bot.send_message(message.from_user.id, 'Пожалуйста, зарегистрируйтесь для использования этой функции.')
        return
    await message.answer(
        "🚗 Для заказа автомобиля на тест-драйв необходимо выполнить следующие шаги:\n\n"
        "1️⃣ Выберите интересующий вас автомобиль. Запомните ID модели.\n"
        "2️⃣ Выберите удобный для вас способ связи с менеджером. Это может быть номер телефона или почта:\n"
        "   - 📞 Телефон: +7 (949) 352 12-32\n"
        "   - 📧 Email: DealerShip@gmail.com\n"
        "3️⃣ Сообщите менеджеру, что вы хотите протестировать автомобиль. 🚘"
    )