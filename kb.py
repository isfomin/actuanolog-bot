from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from rss_channels import channels

items = list(channels.keys())
is_even = not len(items) & 1
left_items = items[0::2]
right_items = items[1::2]

menu = [[KeyboardButton(text=f"/channel {left}"),
         KeyboardButton(text=f"/channel {right}")] for left, right in zip(left_items, right_items)]

if not is_even:
    menu.append([KeyboardButton(text=f"/channel {left_items[-1]}")])

menu = ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True)

