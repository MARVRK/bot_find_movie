import logging
import asyncio

from aiogram import Router

from main.data.loader import dp, bot
from main.handlers import user_menu, admin_menu

logging.basicConfig(filename="log.txt", level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
log = logging.getLogger(__name__)


async def main():
    log.info("Bot started")
    dp.include_router(user_menu.router)
    dp.include_router(admin_menu.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    log.info("Run Main")
    asyncio.run(main())
