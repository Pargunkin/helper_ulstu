import datetime
import logging
import random

import aiohttp
from aiogram import F, Router, types
from aiogram.filters import Command

from data.emoji import WEATHER_EMOJIS
from data.texts import FACTS, GREETINGS, QUOTES, WMO_CODES
from handlers.logic import send_cached_photo
from services.keyboards import get_back_menu
from services.utils import delete_previous_bot_message, safe_delete
from system import config
from state import storage as bot_state

router = Router()


@router.message(Command("about"), F.chat.type == "private")
async def cmd_about(message: types.Message):
    text = (
        "<tg-emoji emoji-id='5422439311196834318'>💡</tg-emoji> <b>«Студпомощник»</b> — <b>удобный карманный справочник</b> для <i>абитуриентов</i> и <i>первокурсников</i> <a href='https://ulstu.ru'>УлГТУ</a>. Он решает проблему разрозненной и сложной подачи информации: <b>вместо долгих поисков по сайту</b> или <b>неловких вопросов куратору</b>, студент получает <b>чёткие пошаговые инструкции</b> прямо в мессенджере.\n\n"
        "<tg-emoji emoji-id='5325547803936572038'>✨</tg-emoji> <b>Команда:</b> <a href='https://t.me/daikuuu'>Паргунькин</a>, <a href='https://t.me/ramiskooo'>Хусейнов</a>, <a href='https://t.me/Arthur_Krm'>Каримов</a>, <a href='https://t.me/k0lhozn1ck'>Романов</a>\n"
        "<tg-emoji emoji-id='5447410659077661506'>🌐</tg-emoji> <b>Ссылка:</b> <a href='https://t.me/helper_ulstu_bot'>@helper_ulstu_bot</a>\n"
        "<tg-emoji emoji-id='5341715473882955310'>⚙️</tg-emoji> <b>Версия:</b> 0.7.2, бета–тест"
    )
    await safe_delete(message)
    await send_cached_photo(message, config.IMG_ABOUT, text, get_back_menu())

@router.message(Command("quote"), F.chat.type == "private")
async def cmd_quote(message: types.Message):
    emojis = [
        ("5197434882321567830", "💵"),
        ("5197369495739455200", "💻"),
        ("5377505475015235101", "🚀"),
        ("5377775044342599336", "🔥"),
        ("5197161121106123533", "🧠"),
        ("5377746319601324795", "🎯"),
        ("5379773896352355687", "⭐")
    ]
    
    quotes = [
        "«Программы должны писаться для людей, чтобы их могли читать, и лишь во вторую очередь — для машин, чтобы они могли их исполнять», — <i>Харольд Абельсон</i>",
        "«Преждевременная оптимизация — корень всех зол», — <i>Дональд Кнут</i>",
        "«Простота — залог надежности», — <i>Эдсгер Дейкстра</i>",
        "«Есть два способа проектирования программного обеспечения: один способ — сделать его настолько простым, чтобы в нем очевидно не было недостатков, а другой — сделать его настолько сложным, чтобы в нем не было очевидных недостатков», — <i>Чарльз Хоар</i>",
        "«Говорить — дешево. Покажи мне код», — <i>Линус Торвальдс</i>",
        "«Программирование — это искусство говорить другому человеку то, что он хочет, как это сделать», — <i>Дональд Кнут</i>",
        "«Сначала решите проблему, а потом пишите код», — <i>Джон Джонсон</i>",
        "«Любой дурак может написать код, который поймет компьютер. Хорошие программисты пишут код, который поймут люди», — <i>Мартин Фаулер</i>",
        "«Единственный способ делать великую работу — любить то, что ты делаешь», — <i>Стив Джобс</i>",
        "«Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма», — <i>Уинстон Черчилль</i>",
        "«Не бойтесь медленно идти, бойтесь стоять на месте», — <i>Китайская пословица</i>",
        "«Образование — самое мощное оружие, которое вы можете использовать, чтобы изменить мир», — <i>Нельсон Мандела</i>",
        "«Великие умы обсуждают идеи, средние умы обсуждают события, мелкие умы обсуждают людей», — <i>Элеонора Рузвельт</i>",
        "«Тот, кто хочет — ищет возможности, тот, кто не хочет — ищет причины», — <i>Сократ</i>",
        "«Дисциплина — это решение делать то, чего очень не хочется делать, чтобы достичь того, чего очень хочется достичь», — <i>Джон Максвелл</i>"
    ]

    quote = random.choice(quotes)
    random_emoji_id, fallback_emoji = random.choice(emojis)
    
    text = f"<tg-emoji emoji-id='{random_emoji_id}'>{fallback_emoji}</tg-emoji> <b>Цитата дня:</b>\n\n<blockquote>{quote}</blockquote>"
    
    await safe_delete(message)
    await delete_previous_bot_message(message.bot, message.chat.id)
    sent_message = await message.answer(text=text, reply_markup=get_back_menu())
    bot_state.last_messages[message.chat.id] = sent_message.message_id

@router.message(Command("fact"), F.chat.type == "private")
async def cmd_fact(message: types.Message):
    facts = FACTS

    emojis = [
        ("5395695537687123235", "💡"),
        ("5361741454685256344", "🤔"),
        ("5334544901428229844", "🔥"),
        ("5431609822288033666", "🚀"),
        ("5269531045165816230", "🤯"),
        ("5391112412445288650", "🧠"),
        ("5210956306952758910", "✨"),
        ("5377535110289576661", "📚")
    ]
    
    fact = random.choice(facts)
    random_emoji_id, fallback_emoji = random.choice(emojis)
    
    text = (
        f"<tg-emoji emoji-id='{random_emoji_id}'>{fallback_emoji}</tg-emoji> <b>А вы знали, что...</b>\n\n"
        f"<blockquote>{fact}</blockquote>"
    )
    
    await safe_delete(message)
    await delete_previous_bot_message(message.bot, message.chat.id)
    sent_message = await message.answer(text=text, reply_markup=get_back_menu())
    bot_state.last_messages[message.chat.id] = sent_message.message_id

@router.message(Command("weather"), F.chat.type == "private")
async def cmd_weather(message: types.Message):
    args = message.text.split(maxsplit=1)
    
    if len(args) > 1:
        city = args[1].strip()
        is_default = False
    else:
        city = "УлГТУ"
        is_default = True
        
    await safe_delete(message)
    await delete_previous_bot_message(message.bot, message.chat.id)
    
    if is_default:
        wait_msg = await message.answer("<i><tg-emoji emoji-id='5386367538735104399'>⌛️</tg-emoji> Запрашиваю погоду около УлГТУ...</i>")
    else:
        wait_msg = await message.answer(f"<i><tg-emoji emoji-id='5386367538735104399'>⌛️</tg-emoji> Запрашиваю погоду для «{city}»...</i>")
    
    try:
        async with aiohttp.ClientSession() as session:
            if is_default:
                lat, lon = 54.3190, 48.3914
                resolved_name = "УлГТУ (<i>Северный Венец</i>)"
            else:
                geo_url = (
                    f"https://geocoding-api.open-meteo.com/v1/search"
                    f"?name={city}&count=1&language=ru&format=json"
                )
                async with session.get(geo_url, timeout=10) as geo_response:
                    geo_data = await geo_response.json()
                    if not geo_data.get('results'):
                        raise Exception(f"Город «{city}» не найден")
                    location = geo_data['results'][0]
                    lat, lon = location['latitude'], location['longitude']
                    resolved_name = location['name']

            weather_url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}"
                f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m"
                f"&timezone=auto"
            )
            async with session.get(weather_url, timeout=10) as weather_response:
                if weather_response.status != 200:
                    raise Exception("Сервис погоды временно недоступен")
                data = await weather_response.json()

        current = data['current']
        weather_code = current['weather_code']
        description = WMO_CODES.get(weather_code, "Неизвестно")
        
        wind_kmh = current['wind_speed_10m']
        wind_ms = float(wind_kmh) / 3.6
        
        text = (
            f"<tg-emoji emoji-id='5391032818111363540'>📍</tg-emoji> <b>Погода: {resolved_name}</b>\n\n"
            f"<blockquote>{description}</blockquote>\n"
            f"<tg-emoji emoji-id='5470049770997292425'>🌡</tg-emoji> <b>Температура:</b> {current['temperature_2m']}°C (<i>ощущается как {current['apparent_temperature']}°C</i>)\n"
            f"<tg-emoji emoji-id='5393512611968995988'>💧</tg-emoji> <b>Влажность:</b> {current['relative_humidity_2m']}%\n"
            f"<tg-emoji emoji-id='5467538555158943525'>💨</tg-emoji> <b>Ветер:</b> {wind_ms:.1f} м/с (<i>{wind_kmh} км/ч</i>)"
        )
        
        await wait_msg.delete()
        sent_message = await message.answer(text=text, reply_markup=get_back_menu())
        bot_state.last_messages[message.chat.id] = sent_message.message_id

    except Exception as e:
        await wait_msg.delete()
        error_text = (
            "<tg-emoji emoji-id='5350584327946127806'>🤕</tg-emoji> Не удалось получить погоду!\n"
            "Проверьте название города или попробуйте позже..."
        )
        sent_message = await message.answer(text=error_text, reply_markup=get_back_menu())
        bot_state.last_messages[message.chat.id] = sent_message.message_id
        logging.error(f"Ошибка погоды: {e}")

GREETINGS = {
    "привет", "приветик", "приветствую", "здравствуйте", 
    "здравствуй", "хай", "ку", "добрый день", 
    "добрый вечер", "доброе утро", "салют", "йо",
    "здарова", "салам", "хеллоу", "хелло", "васап",
    "йоу", "привст", "прв", "здорова",
    "здоровья", "здравия", "добра", "здравия"
}

@router.message(lambda message: message.text and any(greeting in message.text.lower() for greeting in GREETINGS), F.chat.type == "private")
async def text_hello(message: types.Message):
    await safe_delete(message)
    await delete_previous_bot_message(message.bot, message.chat.id)
    sent_message = await message.answer(
        "Привет-привет <tg-emoji emoji-id='5336819370079299297'>👋</tg-emoji>! Нажми на кнопку ниже, чтобы вернуться в меню...", 
        reply_markup=get_back_menu()
    )
    bot_state.last_messages[message.chat.id] = sent_message.message_id