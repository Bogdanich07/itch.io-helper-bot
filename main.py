from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import UserState, TOKEN
from handlers.follow_games import follow_all
from handlers.get_username import username_handler
from handlers.start import start
from sqlite import create_table

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

create_table()


def show_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [
        "/unfollow_games",
        "/change_user",
        "/follow_creators",
    ]
    keyboard.add(*buttons)

    return keyboard


dp.register_message_handler(start, commands=["start"])

dp.register_message_handler(username_handler, state=UserState.user_name)

dp.register_message_handler(follow_all, commands=["follow_all"], state="*")


if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
