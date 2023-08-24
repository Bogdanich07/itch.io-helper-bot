import logging
from aiogram import types
from aiogram.types import ParseMode


async def greet(message: types.Message):
    await message.reply("Hey there!", parse_mode=ParseMode.MARKDOWN)


logging.basicConfig(level=logging.INFO)
