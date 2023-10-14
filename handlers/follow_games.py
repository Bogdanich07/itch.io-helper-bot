from aiogram import types
from aiogram.dispatcher import FSMContext
import json

from config import UserState
from sqlite import update_follows
import info


async def follow_games_handler(message: types.Message, titles: str, user_name: str):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/follow_all")
    keyboard.add(btn1)

    links = await info.get_links(user_name)
    games = {link: await info.get_last_update(link) for link in links}

    await update_follows(message.from_user.id, json.dumps(games))

    await UserState.next()
    await message.answer(f"Nice to meet you! Here's your collection: {titles}", reply_markup=keyboard)


async def empty_collection_handler(message: types.Message):
    await message.answer(
        'Oops... It seems like your collection is empty, private, or you have not enabled the "show on my profile" option 😕'
    )


async def follow_all(message: types.Message, state: FSMContext):
    await message.answer("Done! ✅")
