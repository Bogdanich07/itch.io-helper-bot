from aiogram import types
from aiogram.dispatcher import FSMContext

from config import UserState
from sqlite import check_user_existence

async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if await check_user_existence(user_id):
        await message.answer("Welcome back :3")
    else:
        await message.answer(
            "Let's start! Firstly send me your nickname on itch.io to follow the games from your collection"
        )
        await UserState.user_name.set()
    await state.update_data(user_id=user_id)
