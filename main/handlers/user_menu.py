import logging

from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command

from main.data.loader import bot
from main.api_sql.db import DataBase

logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = Router()
db = DataBase()


class CodePlug(StatesGroup):
    code_plug = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hi, i am Bot which helps you to find movie!")


@router.message(Command("search"))
async def find_movie_by_code(message: Message, state: FSMContext):
    await message.answer("Please select code of the movie")
    await state.set_state(CodePlug.code_plug)


@router.message(CodePlug.code_plug)
async def fetch_the_movie(message: Message, state: FSMContext):
    code_movie = message.text
    movie_info = db.fetch_all_data(code_movie)

    if movie_info:
        if code_movie == movie_info[4] and code_movie is not None:
            movie_details = (f"Name: {movie_info[1]}",
                             f"Date_of_release: {movie_info[2]}",
                             f"Category: {movie_info[3]}",
                             f"Movie_code: {movie_info[4]}")
            await bot.send_message(message.chat.id, text="\n".join(movie_details))

            if movie_info[5]:
                image_file = BufferedInputFile(movie_info[5], filename="movie_poster.png")
                await bot.send_photo(message.chat.id, image_file)
    else:
        await message.answer("Sorry, there is now movie in database")

    await state.clear()

### This Was Done to Make AutoButtons Generatio #####

# @router.message(Command("search"))
# async def find_movie_by_code(message: Message):
#     await message.answer("Please select code of the movie")
# find_movies_names = db.get_all_movies()
# buttons = []
#
# for id, movie in find_movies_names:
#     buttom = InlineKeyboardButton(text=movie, callback_data=f"movie_{id}")
#     buttons.append([buttom])
#
# keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
# await message.answer("Choose a movie:", reply_markup=keyboard)

### This Was Done to send data from Buttons to Call_back#####

# @router.callback_query(lambda call: call.data.startswith("movie_"))
# async def movie_callback(call):
#     movie_id = call.data.split("_")[1]
#
#     movie_info = db.fetch_all_data(movie_id)
#     movie_details = (f"Name: {movie_info[1]}",
#                      f"Date_of_release: {movie_info[2]}",
#                      f"Category: {movie_info[3]}",
#                      f"Movie_age: {movie_info[4]}")
#
#     await bot.send_message(call.message.chat.id, "\n".join(movie_details))
#
#     if movie_info[5]:
#         image_file = BufferedInputFile(movie_info[5], filename="movie_poster.png")
#         await bot.send_photo(call.message.chat.id, image_file)
