import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from asyncio import run
import loguru
import requests

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    KINOPOISK_API_KEY = os.getenv("KINOPOISK_API_KEY")
    KINOPOISK_API_URL = os.getenv("KINOPOISK_API_URL")


bot = Bot(token=Config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(
        'Привет! Я твой телеграмм-бот. Вот список доступных команд:\n\n/start - Начать диалог с ботом\n/film - Получить информацию о фильме')


@dp.message()
async def film_command(message: types.Message):
    await message.answer('Информация о фильме: \n\nНазвание: ...\nЖанр: ...\nГод выпуска: ...')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
