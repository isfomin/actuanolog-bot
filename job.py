import asyncio
import logging
from aiogram import Bot
from aiogram.types.bot_name import BotName

from config import AUTHOR_TG_ID
import kb


async def start_scheduler(bot: Bot):
    try:
        bot_name: BotName = await bot.get_my_name()
        await bot.send_message(AUTHOR_TG_ID, f"`{bot_name.name}` is started", reply_markup=kb.menu)
    except BaseException as e:
        logging.warning(f"{e}")


def run_schedule(bot: Bot):
    loop = asyncio.get_event_loop()
    loop.create_task(start_scheduler(bot))
