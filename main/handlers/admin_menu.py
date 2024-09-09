import logging
import os
import uuid

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from main.data.loader import bot
from main.api_sql.db import db, DataBase

logging.basicConfig(filename="log.txt", level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

router = Router()
db = DataBase()


class Movie(StatesGroup):
    article = State()
    date_of_release = State()
    category = State()
    movie_age = State()
    photo = State()


@router.message(Command("add_movie"))
async def add_name(message: Message, state: FSMContext):
    await message.answer("Write name of the movie")
    await state.set_state(Movie.article)

@router.message(Movie.article)
async def add_release_date (message: Message, state: FSMContext):
    await state.update_data(article=message.text)
    await message.answer("Write date of release")
    await state.set_state(Movie.date_of_release)

@router.message(Movie.date_of_release)
async def category (message: Message, state: FSMContext):
    await state.update_data(date_of_release=message.text)
    await message.answer("Write category of the movie")
    await state.set_state(Movie.category)

@router.message(Movie.category)
async def category (message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Write age of the movie")
    await state.update_data(category=message.text)
    await state.set_state(Movie.movie_age)

@router.message(Movie.movie_age)
async def movie_age(message: Message, state: FSMContext):
    await state.update_data(movie_age=message.text)
    await message.answer("Send photo of the movie")
    await state.set_state(Movie.photo)

@router.message(Movie.photo)
async def photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    file_info = await bot.get_file(file_id)

    dowloaded_file = await bot.download_file(file_info.file_path)
    image_byte = dowloaded_file.read()

    await state.update_data(photo=image_byte)
    await message.answer("Movie added")

    data = await state.get_data()
    db.upload_data(name=data["article"],
                   date_of_release=data["date_of_release"],
                   category=data["category"],
                   movie_age=data["movie_age"],
                   image=data["photo"])
    await message.answer(f"name_of_the_movie: {data['article']}")
    await state.clear()