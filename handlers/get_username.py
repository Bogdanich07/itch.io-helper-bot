from aiogram import types
from aiogram.dispatcher import FSMContext

from sqlite import insert_user
from handlers.follow_games import follow_games_handler, empty_collection_handler
from config import UserState
import info


async def username_handler(message: types.Message, state: FSMContext):
    # sourcery skip: use-named-expression
    user_name = message.text.lower()
    await state.update_data(user_name=user_name)

    if info.check_username(user_name):
        user_id = message.from_user.id
        insert_user(user_id, user_name)

        await welcome(message, user_name)

        titles = info.get_titles(user_name)
        if titles:
            await follow_games_handler(message, ', '.join(titles))
            await UserState.next()
        else:
            await empty_collection_handler(message)
    else:
        await invalid_username(message, user_name)


async def welcome(message: types.Message, user_name: str):
    await message.answer(
        f"Nice to meet you {user_name}! Now you can follow games and creators 🥳"
    )


async def invalid_username(message: types.Message, user_name: str):
    await message.answer(
        f"Oops... user {user_name} doesn't exist 😕\nPlease enter a valid nickname",
        reply_markup=types.ReplyKeyboardRemove(),
    )