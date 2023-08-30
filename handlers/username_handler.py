from aiogram import types
from aiogram.dispatcher import FSMContext

from sqlite import insert_user
import info


async def get_username(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.text.lower()

    if info.check_username(user_name):
        insert_user(user_id, user_name)

        await welcome(message, user_name)

        if info.get_titles(user_name):
            await follow_games_handler(message, user_name)

            await state.finish()
        else:
            await empty_collection_handler(message)
    else:
        await invalid_username(message, user_name)


async def welcome(message: types.Message, user_name: str):
    from main import show_keyboard

    await message.answer(
        f"Nice to meet you {user_name}! Now you can follow games and creators 🥳",
        reply_markup=show_keyboard(),
    )


async def invalid_username(message: types.Message, user_name: str):
    await message.answer(
        f"Oops... user {user_name} doesn't exist 😕\nPlease enter a valid nickname",
        reply_markup=types.ReplyKeyboardRemove(),
    )


async def follow_games_handler(message: types.Message, user_name: str):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(
        "Tap here to follow all", callback_data="follow_all"
    )
    keyboard.add(btn1)

    titles = info.get_titles(user_name)
    await message.answer(f"Your collection: {', '.join(titles)}", reply_markup=keyboard)


async def empty_collection_handler(message: types.Message):
    await message.answer(
        'Oops... It seems like your collection is empty, private, or you have not enabled the "show on my profile" option 😕'
    )
