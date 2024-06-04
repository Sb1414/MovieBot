import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand
from asyncio import run
from loguru import logger
import aiohttp
from aiogram.types import InlineKeyboardMarkup

from utils.texts.text import hello_message, film_command_message, error_message
from utils.keyboards.keyboards import get_genre_selector_keyboard, get_random_keyboard
from utils.states.form import Form
from utils.parser.response_parser import response_parser
from utils.defines.define import genre_translation

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    KINOPOISK_API_KEY = os.getenv("KINOPOISK_API_KEY")
    KINOPOISK_API_URL = os.getenv("KINOPOISK_API_URL")
    KINOPOISK_API_RANDOM_FILM_URL = os.getenv("KINOPOISK_API_RANDOM_FILM_URL")
    KINOPOISK_API_RANDOM_GENRES_FILM_URL = os.getenv("KINOPOISK_API_RANDOM_GENRES_FILM_URL")


header = {"accept": "application/json",
          "X-API-KEY": Config.KINOPOISK_API_KEY}

bot = Bot(token=Config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=hello_message)


@dp.message(Command("film"))
async def get_film_choice_menu(message: types.Message, state: FSMContext):
    await state.set_state(Form.genre)
    await bot.send_message(chat_id=message.chat.id, text=film_command_message,
                           reply_markup=await get_genre_selector_keyboard())


@dp.message(Command("random"))
async def get_random_film_command(message: types.Message):
    await get_film(message.chat.id, Config.KINOPOISK_API_RANDOM_FILM_URL, await get_random_keyboard())


@dp.callback_query(F.data == "one_more")
async def get_one_more_rand_film(query: types.CallbackQuery):
    await get_film(query.message.chat.id, Config.KINOPOISK_API_RANDOM_FILM_URL, await get_random_keyboard())


@dp.callback_query(Form.genre)
async def processing_request(query: types.CallbackQuery, state: FSMContext):
    genre = query.data.split("_")[1]
    await get_film(query.message.chat.id, Config.KINOPOISK_API_RANDOM_GENRES_FILM_URL + genre_translation[genre],
                   await get_genre_selector_keyboard())


async def get_film(chat_id: int, url: str, keyboard: InlineKeyboardMarkup):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=header) as response:
            if response.status == 200:
                response_data = await response.json()
                await bot.send_message(chat_id=chat_id, text=await response_parser(response_data),
                                       reply_markup=keyboard)
            else:
                logger.error("Bad response status code:", response.status)
                await bot.send_message(chat_id=chat_id, text=error_message)


async def main() -> None:
    await bot.set_my_commands([BotCommand(command="/film", description="🎬 Scenario for getting film."),
                               BotCommand(command="/random", description="🎱 Get a random film.")])
    await dp.start_polling(bot)


if __name__ == '__main__':
    logger.info("Бот работает перейдите в телеграмм и найдите @YaMovieBot_Test_bot")
    run(main())
