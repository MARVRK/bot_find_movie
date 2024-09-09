from aiogram.types.inline_keyboard_button import InlineKeyboardButton

button = InlineKeyboardButton

def find_movie_keyboard():
    return [
        [button(text="movie", callback_data="movie")]
        ]
