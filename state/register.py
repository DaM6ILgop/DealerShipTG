from aiogram.fsm.state import StatesGroup, State

#Класс для получения данных, введенных пользователем
class RegisterState(StatesGroup):
    reg_name = State()
    reg_surname = State()
    reg_phone = State()
