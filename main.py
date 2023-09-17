from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
import asyncio

from config import UserState, TOKEN
from handlers.follow_games import follow_all
from handlers.get_username import username_handler
from handlers.start import start
from sqlite import create_table, read_table
from info import get_last_update, get_devlog, UpdateInfo

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


async def check_for_updates(break_time):
    while True:
        users = read_table()
        for user_id in users.keys():
            for game_url, prev_update in users[user_id].items():
                if prev_update != get_last_update(game_url):
                    update_url = get_devlog(game_url)
                    update = UpdateInfo(update_url)

                    header, likes_count = (
                        update.get_header(),
                        update.get_likes_count(),
                    )

                    await bot.send_message(
                        user_id,
                        text=f"*{header}*\n\nRating: {likes_count} [👍]({update_url}) ",
                        parse_mode=ParseMode.MARKDOWN,
                    )

        await asyncio.sleep(break_time)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(check_for_updates(30))

    executor.start_polling(dp, skip_updates=True)
