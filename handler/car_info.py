import math

from aiogram import Bot, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand, BotCommandScopeDefault, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
import pyodbc
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handler.setDBData import user_is_register
from state.car_massive import CarState

conn_str = ( f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER=AzurLine;'
    f'DATABASE=TG_CarDealer2;'
    f'Trusted_Connection=yes;')

connection = pyodbc.connect(conn_str)
cursor = connection.cursor()


def kb_build(current_page, total_pages, car_list):
    keyboard = InlineKeyboardBuilder()
    cars_per_page = 4  # Limit to 4 cars per page
    start_index = current_page * cars_per_page
    end_index = min(start_index + cars_per_page, len(car_list))

    # Add buttons for cars on the current page
    for i, car in enumerate(car_list[start_index:end_index]):
        button = InlineKeyboardButton(text=str(car[3]), callback_data=str(start_index + i))  # Use index in the list as callback_data
        keyboard.add(button)

    keyboard.adjust(2)

    # Add navigation buttons
    navigation_buttons = []
    if current_page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"prev_{current_page}"))
    else:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️", callback_data="ignore"))
    navigation_buttons.append(InlineKeyboardButton(text=f"{current_page+1}/{total_pages}", callback_data="ignore"))
    if current_page < total_pages - 1:
        navigation_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"next_{current_page}"))
    else:
        navigation_buttons.append(InlineKeyboardButton(text="➡️", callback_data="ignore"))
    keyboard.row(*navigation_buttons)

    return keyboard.as_markup()


async def send_images_from_database(message: Message,state: FSMContext, bot: Bot):
    # Проверка наличия пользователя в базе данных
    if not await user_is_register(message.from_user.id):
        await bot.send_message(message.from_user.id, 'Пожалуйста, зарегистрируйтесь для использования этой функции.')
        return

    conn = pyodbc.connect(conn_str)

    # Создание курсора
    cursor = conn.cursor()

    # Выполнение запроса для выбора изображения и информации об автомобиле
    cursor.execute("""
                   SELECT Images.ImageURL, CarDealer.Developers_name, CarDealer.Developers_country, CarModels.Model_name, CarModels.ID_vehicle_model,
                   Cars.Year_of_vehicle, Cars.Car_color, Cars.Engine_type, Cars.Car_price
                   FROM Images
                   JOIN Cars ON Images.CarID = Cars.VIN_vehicle_number
                   JOIN CarModels ON Cars.ID_vehicle_model = CarModels.ID_vehicle_model
                   JOIN CarDealer ON CarModels.ID_developer = CarDealer.ID_developer
               """)

    # Получение результатов запроса
    rows = cursor.fetchall()
    CarState.car_list = rows
    total_pages = math.ceil(len(CarState.car_list) / 4)  # Рассчитываем общее количество страниц
    await bot.send_message(message.from_user.id, 'Приветствуем вас в нашем виртуальном автосалоне! 🚗\n'
'Мы рады представить вам **список автомобилей**, с которыми можно ознакомиться прямо сейчас.\n'
'Если вам приглянулся автомобиль, не стесняйтесь обратиться в наш автосалон. Мы всегда готовы помочь вам с выбором! 🤝\n'
'Кнопка запроса контактов салона удобно расположена в "Меню".📞\n'
                           , reply_markup=kb_build(0, total_pages, CarState.car_list))
    await state.set_state(CarState.select_countries)


async def select_countries(call: CallbackQuery, state: FSMContext, bot:Bot):
    if call.data.isdigit():
        index = int(call.data)
        selected_car = CarState.car_list[index]
        image_url = selected_car[0]
        car_info = f"Название производителя: {selected_car[1]}\n\n" \
                   f"Страна производитель: {selected_car[2]}\n\n" \
                   f"Название модели: {selected_car[3]}\n\n" \
                   f"ID модели автомобиля: {selected_car[4]}\n\n" \
                   f"Дата выпуска: {selected_car[5]}\n\n" \
                   f"Цвет автомобиля: {selected_car[6]}\n\n" \
                   f"Тип двигателя: {selected_car[7]}\n\n" \
                   f"Цена автомобиля в рублях: {selected_car[8]}"
        try:
            await bot.send_photo(chat_id=call.message.chat.id, photo=image_url, caption=car_info)
        except Exception:
            await bot.send_message(chat_id=call.message.chat.id, text=car_info)
    else:
        # Обрабатываем нажатия на кнопки навигации
        if call.data == "ignore":
            return
        if call.data.startswith("prev_"):
            page = int(call.data.split("_")[1]) - 1
        elif call.data.startswith("next_"):
            page = int(call.data.split("_")[1]) + 1
        else:
            return
        total_pages = math.ceil(len(CarState.car_list) / 4)
        await call.message.edit_reply_markup(reply_markup=kb_build(page, total_pages, CarState.car_list))


async def bot_help(message: Message, bot: Bot):
    if not await user_is_register(message.from_user.id):
        await bot.send_message(message.from_user.id, 'Вы не зарегистрированный пользователь.')
    else:
        await bot.send_message(message.from_user.id,
                               'Здравствуйте! Если у вас возникли какие-либо вопросы, обращайтесь по почте\n'
                               'MailL: dealerShip@gmail.com.')
    return






