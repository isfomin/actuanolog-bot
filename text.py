GMT_RSS_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"
UTC_RSS_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %z"
DATE_FORMAT = "%H:%M:%S %d-%m-%Y"

greet = "Привет, {name}! Я помогу тебе быть в курсе событий."
menu = "Главное меню"
args_not_found = "Ошибка: не переданы аргументы"

rss_item_template = """
{date}
*{title}*  
Автор: *{author}*  
[{link}]({link})

Теги: `{tags}`
"""

rss_channel_template = """
Показано: *{count}*
RSS-канал: *{title}*
{description}
"""