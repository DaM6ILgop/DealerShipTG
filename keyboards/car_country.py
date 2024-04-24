from aiogram import types
from aiogram import Bot
from aiogram.dispatcher import router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import pyodbc

conn_str = (f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER=AzurLine;'
    f'DATABASE=TG_CarDealer2;'
    f'Trusted_Connection=yes;')

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()





