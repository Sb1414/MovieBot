from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


async def get_genre_selector_keyboard() -> InlineKeyboardMarkup:
    drama = InlineKeyboardButton(text='Драма 🤧', callback_data='genre_drama')
    comedy = InlineKeyboardButton(text='Комедия 😂', callback_data='genre_comedy')
    fantasy = InlineKeyboardButton(text='Фэнтези 👻', callback_data='genre_fantasy')
    adventure = InlineKeyboardButton(text='Приключения ✈️', callback_data='genre_adventure')
    horror = InlineKeyboardButton(text='Ужастик 👹', callback_data='genre_horror')
    science = InlineKeyboardButton(text='Научная фантастика 🦾', callback_data='genre_science')
    action = InlineKeyboardButton(text='Боевик 🔥', callback_data='genre_action')
    detective = InlineKeyboardButton(text='Детектив 🕵️', callback_data='genre_detective')
    thriller = InlineKeyboardButton(text='Триллер 😵', callback_data='genre_thriller')
    historical = InlineKeyboardButton(text='Документальный 📄', callback_data='genre_historical')
    romance = InlineKeyboardButton(text='Романтика 🏩', callback_data='genre_romance')
    choice_genre_inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[[drama, comedy], [fantasy, adventure], [horror, thriller], [science], [action, detective],
                         [historical, romance]])
    return choice_genre_inline_kb


async def get_random_keyboard() -> InlineKeyboardMarkup:
    random_film_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Еще один фильм", callback_data='one_more')]])
    return random_film_kb
