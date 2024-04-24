from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#Кнопка нижней панели
register_bttn = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='🟢 Зарегистироваться 🟢'
        )
    ]

], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Для продолжения нажмитье'
                                                                      ' на кнопку')