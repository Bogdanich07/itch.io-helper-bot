from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
import asyncio
import json

from config import UserState, TOKEN
from handlers.follow_games import follow_all
from handlers.get_username import username_handler
from handlers.start import start
from sqlite import create_table, read_table, update_follows
from info import get_last_update, get_devlog

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

create_table()


dp.register_message_handler(start, commands=["start"])

dp.register_message_handler(username_handler, state=UserState.user_name)

dp.register_message_handler(follow_all, commands=["follow_all"], state="*")


async def check_for_updates(break_time):
    while True:
        users = await read_table()
        for user_id in users.keys():
            result = {}
            for game_url, prev_update in users[user_id].items():
                last_update = await get_last_update(game_url)
                result[game_url] = last_update

                if prev_update != last_update:
                    update_url = await get_devlog(game_url)

                    await bot.send_message(
                        user_id,
                        text=f"[Click!]({update_url})",
                        parse_mode=ParseMode.MARKDOWN,
                    )

            await update_follows(user_id, json.dumps(result))

        await asyncio.sleep(break_time)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(check_for_updates(30))

    executor.start_polling(dp, skip_updates=True)
