from aiogram import types
from aiogram.dispatcher import FSMContext

from sqlite import update_follows

def show_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [
        "/unfollow_games",
        "/change_user",
        "/follow_creators",
    ]
    keyboard.add(*buttons)

    return keyboard

async def follow_games_handler(message: types.Message, titles: str):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/follow_all")
    keyboard.add(btn1)

    update_follows(message.from_user.id, titles)

    await message.answer(f"Your collection: {titles}", reply_markup=keyboard)


async def empty_collection_handler(message: types.Message):
    await message.answer(
        'Oops... It seems like your collection is empty, private, or you have not enabled the "show on my profile" option 😕'
    )

async def follow_all(message: types.Message, state: FSMContext):
    await message.answer("Done! ✅", reply_markup=show_keyboard())
