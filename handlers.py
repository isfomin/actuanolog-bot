import requests
import xml.etree.ElementTree as ET
import logging
from aiogram import Router, F, flags
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, LinkPreviewOptions, CallbackQuery
from datetime import datetime
from aiogram.enums.parse_mode import ParseMode

from config import YANDEX_TOKEN
from rss_channels import channels
import text
import kb
import rss.provider as rss
import rss.parser as parser

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@flags.chat_action("typing")
@router.message(Command("weather"))
async def tech_news_handler(msg: Message):
    headers = {
        'X-Yandex-API-Key': YANDEX_TOKEN
    }

    response = requests.get('https://api.weather.yandex.ru/v2/forecast?lat=52.37125&lon=4.89388', headers=headers)

    await msg.answer(f"{response.text[:500]}")


# answer max size: 4100 symbols
@flags.chat_action("typing")
@router.message(Command("channel"))
async def habr_news_handler(msg: Message, command: CommandObject):
    if command.args is None:
        await msg.answer(text.args_not_found)
        return

    channel = command.args
    result = parser.parse_xml(rss.get(channels[channel]["url"]))
    counter = 0
    for item in result["items"][:5]:
        counter = counter + 1
        categories = ', '.join([f'{cat}' for cat in item['tags']]) if isinstance(item['tags'], list) else item['tags']
        date = datetime.strptime(item['pub_date'], channels[channel]["date_format"])

        answer_text = text.rss_item_template.format(
            date=date.strftime(text.DATE_FORMAT),
            title=item['title'],
            author=item['author'],
            link=item["link"],
            tags=categories
        )

        await msg.answer(f"{answer_text}", parse_mode=ParseMode.MARKDOWN,
                         link_preview_options=LinkPreviewOptions(is_disabled=True))

    annotation = text.rss_channel_template.format(
        count=counter,
        title=result["channel_title"],
        description=result["channel_description"]
    )

    await msg.answer(f"{annotation}", parse_mode=ParseMode.MARKDOWN)