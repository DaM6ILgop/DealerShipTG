from aiogram.fsm.state import StatesGroup, State

#Класс для получения данных, введенных пользователем
class CarState(StatesGroup):
    car_list = []
    select_countries = State()
