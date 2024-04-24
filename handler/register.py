from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.register import RegisterState
import re

from handler.setDBData import handle_user_data
from handler.setDBData import user_is_register

#Запуск регистрации при нажатии на кнопку регистрации.
# Используется магический фильтр в главном файле
async def start_register(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if await user_is_register(user_id):
        await message.answer("❤️|Вы уже зарегистрированы|❤️")
    else:
        await message.answer(f'📝 Пожалуйста, укажите ваше имя.')
        await state.set_state(RegisterState.reg_name)



async def register_name(message: Message, state: FSMContext):
    await message.answer(f'Приятно познакомится. {message.text}. \n'
                         f'Теперь укажите вашу фамилию')
    await state.update_data(regname=message.text)
    await state.set_state(RegisterState.reg_surname)



async def register_surname(message: Message, state: FSMContext):
    await state.update_data(regsurname=message.text)

    await message.answer(f'Укажите ваш номер телефона. ☎️\n'
                         f'⚠️Внимание, проверяйте вводимый номер⚠️\n'
                         f'Пример формата номера телефона: +79493333333')
    await state.set_state(RegisterState.reg_phone)



async def register_phone(message: Message, state: FSMContext):
    if(re.findall('^\+?[7][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$',message.text)):
        await state.update_data(regphone=message.text)
        try:
            reg_data = await state.get_data()
            reg_data['tg_user_id'] = message.from_user.id  # Добавляем tg_user_id в данные пользователя
            success = await handle_user_data(reg_data)
            if success:
                reg_name = reg_data.get('regname')
                reg_surname = reg_data.get('regsurname')
                reg_phone = reg_data.get('regphone')
                reg_data['tg_user_id'] = message.from_user.id  # Добавляем tg_user_id в данные пользователя
                msg = f'ℹ️Ваши данныеℹ️\n\n Имя: {reg_name} \n\n Фамилия: {reg_surname} \n\n Телефон - {reg_phone}, \n\n Ваш Id - {message.from_user.id}'
                await message.answer(msg)
                await state.clear()
            else:
                await message.answer('Произошла ошибка при сохранении данных.')
        except Exception as e:
            print(f"Ошибка: {e}")

    else:
        await message.answer('Номер указане в неправильном формате')