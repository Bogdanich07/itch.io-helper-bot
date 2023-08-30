from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import UserState, TOKEN
from sqlite import create_table
from handlers.start_handler import start
from handlers.username_handler import get_username

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

create_table()

def show_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['/unfollow_games', '/change_user', '/follow_creator',]
    keyboard.add(*buttons)

    return keyboard

dp.register_message_handler(start, commands=["start"])  # handlers/start_handler.py

dp.register_message_handler(
    get_username, state=UserState.user_name
)  # handlers/username_handler.py

@dp.callback_query_handler(lambda call: call.data == 'follow_all')
async def follow_all(call: types.CallbackQuery):
    # Here will be code
    await call.message.answer('Done! ✅')

if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
