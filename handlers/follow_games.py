from aiogram import types
from aiogram.dispatcher import FSMContext
import json

from config import UserState
from sqlite import update_follows
import info


def show_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [
        "/unfollow_games",
        "/change_user",
        "/follow_creators",
    ]
    keyboard.add(*buttons)

    return keyboard


async def follow_games_handler(message: types.Message, titles: str, user_name: str):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/follow_all")
    keyboard.add(btn1)

    links = info.get_links(user_name)
    games = {link: info.get_last_update(link) for link in links}

    update_follows(message.from_user.id, json.dumps(games))

    await UserState.next()
    await message.answer(f"Your collection: {titles}", reply_markup=keyboard)


async def empty_collection_handler(message: types.Message):
    await message.answer(
        'Oops... It seems like your collection is empty, private, or you have not enabled the "show on my profile" option 😕'
    )


async def follow_all(message: types.Message, state: FSMContext):
    await message.answer("Done! ✅", reply_markup=show_keyboard())
