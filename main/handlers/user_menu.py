import logging

from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.filters import Command
from main.data.loader import bot
from main.api_sql.db import DataBase

logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = Router()
db = DataBase()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Hi, i am Bot which helps you to find movie!")


@router.message(Command("search"))
async def find_movie(message: Message):
    find_movies_names = db.get_all_movies()
    buttons = []

    for id, movie in find_movies_names:
        buttom = InlineKeyboardButton(text=movie, callback_data=f"movie_{id}")
        buttons.append([buttom])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Choose a movie:", reply_markup=keyboard)


@router.callback_query(lambda call: call.data.startswith("movie_"))
async def movie_callback(call):
    movie_id = call.data.split("_")[1]

    movie_info = db.fetch_all_data(movie_id)
    movie_details = (f"Name: {movie_info[1]}",
                     f"Date_of_release: {movie_info[2]}",
                     f"Category: {movie_info[3]}",
                     f"Movie_age: {movie_info[4]}")

    await bot.send_message(call.message.chat.id, "\n".join(movie_details))

    if movie_info[5]:
        image_file = BufferedInputFile(movie_info[5], filename="movie_poster.png")
        await bot.send_photo(call.message.chat.id, image_file)
