from aiogram.dispatcher.filters.state import StatesGroup, State
from dotenv import load_dotenv
import os


load_dotenv()

TOKEN = os.getenv("TOKEN")


class UserState(StatesGroup):
    user_name = State()
    add_games = State()
    follow_games = State()