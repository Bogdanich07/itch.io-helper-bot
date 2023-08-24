from aiogram import Bot, Dispatcher

from handlers.start_handler import greet
from config import TOKEN

# logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher(bot)

dp.register_message_handler(greet, commands=["start"])

if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
