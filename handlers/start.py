from aiogram import types

from config import UserState
from sqlite import check_user_existence


async def start(message: types.Message):
    from main import show_keyboard

    user_id = message.from_user.id
    if check_user_existence(user_id):
        await message.answer("Welcome back :3", reply_markup=show_keyboard())
    else:
        await message.answer(
            "Let's start! Firstly send me your nickname on itch.io to follow the games from your collection"
        )
        await UserState.user_name.set()
