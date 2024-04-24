import pyodbc
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

conn_str = ( f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER=AzurLine;'
    f'DATABASE=TG_CarDealer2;'
    f'Trusted_Connection=yes;')

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

#Добавление пользователя в базу данных
async def handle_user_data(user_data):
    # Пример SQL-запроса для вставки данных в таблицу
    sql_query = "INSERT INTO [Tg_CarDealer2].[dbo].[Clients] (Tg_user_name, Tg_user_surname, User_phone, Tg_user_id) VALUES (?, ?, ?, ?)"
    print("User_id", user_data['tg_user_id'])
    try:
        # Выполнение запроса с данными пользователя
        cursor.execute(sql_query, (
        user_data['regname'], user_data['regsurname'], user_data['regphone'], user_data['tg_user_id']))
        conn.commit()  # Применение изменений в базе данных
        return True
    except Exception as e:
        print(f"Ошибка при вставке данных в базу данных: {e}")
        return False



#Проверка наличия пользователя в БД
async def user_is_register(user_id):
    try:
        cursor.execute("SELECT COUNT(*) FROM Clients WHERE Tg_user_id = ?", (user_id,))
        count = cursor.fetchone()[0]
        return count > 0
    except Exception as e:
        print(f"Ошибка при проверке наличия пользовтеля в базще данных: {e}")
        return False


async def delete_account(call: CallbackQuery):
    if call.data == "confirm_delete":
        try:
            # Удаление аккаунта из базы данных
            user_id = call.from_user.id
            cursor.execute("DELETE FROM Clients WHERE Tg_user_id = ?", (user_id,))
            conn.commit()
            await call.message.answer("Ваш аккаунт удален (╯°□°）╯︵ ┻━┻")
        except Exception as e:
            print(f"Ошибка при удалении записи из базы данных {e}")
            await call.message.answer("Ошибка при удалении записи из базы данных")
    elif call.data == "cancel_delete":
        await call.message.answer("Благодарим, что остаетесь с нами (◍•ᴗ•◍)❤️")


async def delete_account_confirmation(message: Message):
    # Отправляем сообщение с подтверждением удаления аккаунта и кнопками "Да" и "Нет"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="confirm_delete")],
        [InlineKeyboardButton(text="Нет", callback_data="cancel_delete")]
    ])
    await message.answer("Вы точно уверены, что хотите удалить аккаунт?", reply_markup=keyboard)


