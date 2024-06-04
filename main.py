import logging
import requests
from telegram import Update
from telegram import Filters
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger()

KINOPOISK_API_KEY = 'RZ0GYP8-9FV4A1R-M09SVA1-93QCKB6'
KINOPOISK_API_URL = 'https://api.kinopoisk.dev/v1/movie'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот, который поможет тебе найти фильмы по жанрам. '
                                'Введи /genres, чтобы увидеть список доступных жанров.')

def genres(update: Update, context: CallbackContext) -> None:
    response = requests.get(KINOPOISK_API_URL + '/genres',
                             headers={'X-API-KEY': KINOPOISK_API_KEY})
    genres = response.json()['items']
    genre_names = ', '.join([genre['name'] for genre in genres])
    update.message.reply_text('Доступные жанры: ' + genre_names)

def movies_by_genre(update: Update, context: CallbackContext) -> None:
    genre_name = update.message.text.split()[1]
    response = requests.get(KINOPOISK_API_URL + '/movies',
                             params={'genre': genre_name},
                             headers={'X-API-KEY': KINOPOISK_API_KEY})
    movies = response.json()['items']
    if not movies:
        update.message.reply_text('По заданному жанру фильмов не найдено.')
        return
    for movie in movies:
        update.message.reply_text(f'{movie["nameRu"]} ({movie["year"]}) '
                                    f'[{movie["ratingKinopoisk"]}]')

def main() -> None:
    updater = Updater("7219681669:AAE06Hfvy5w4xbQVLC0KI4ycu65ihZs-_8o", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("genres", genres))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), movies_by_genre))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()