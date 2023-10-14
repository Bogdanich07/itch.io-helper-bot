from aiogram import types
from aiogram.dispatcher import FSMContext

from sqlite import insert_user
from handlers.follow_games import follow_games_handler, empty_collection_handler
from config import UserState
import info


async def username_handler(message: types.Message, state: FSMContext):
    user_name = message.text.lower()
    await state.update_data(user_name=user_name)

    if await info.check_username(user_name):
        user_id = message.from_user.id
        await insert_user(user_id, user_name)

        if titles := await info.get_titles(user_name):
            await follow_games_handler(message, ", ".join(titles), user_name)
            await UserState.next()
        else:
            await empty_collection_handler(message)
    else:
        await invalid_username(message, user_name)


async def invalid_username(message: types.Message, user_name: str):
    await message.answer(
        f"Oops... user {user_name} doesn't exist 😕\nPlease enter a valid nickname",
        reply_markup=types.ReplyKeyboardRemove(),
    )
