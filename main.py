from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext

from config import UserState, TOKEN
from sqlite import create_table, update_follows
from handlers.start_handler import start
from handlers.username_handler import get_username

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

create_table()

def show_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = ['/unfollow_games', '/change_user', '/follow_creators',]
    keyboard.add(*buttons)

    return keyboard

dp.register_message_handler(start, commands=["start"])  # handlers/start_handler.py

dp.register_message_handler(
    get_username, state=UserState.user_name
)  # handlers/username_handler.py

@dp.callback_query_handler(lambda call: call.data == 'follow_all', state="*")
async def follow_all(call: types.CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    update_follows(user_id, 'game1, game2')
    await call.message.answer('Done! ✅')

if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
