import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

import config
import state as app_state
from keyboards import (
    get_abitur_menu,
    get_back_menu,
    get_main_menu,
    get_student_menu,
)
from utils import delete_previous_bot_message, safe_answer, safe_delete


router = Router()


MAIN_MENU_TEXT = (
    "<tg-emoji emoji-id='5413735113294899665'>👋</tg-emoji> "
    "<b>Приветик!</b> Я — «<b>Студпомощник</b>» — бот четырёх студентов. "
    "Помогу разобраться с поступлением и учёбой в УлГТУ.\n\n"
    "<tg-emoji emoji-id='5397782960512444700'>📍</tg-emoji> "
    "Ты в <b>главном меню</b> всего бота!\n"
    "<tg-emoji emoji-id='5424818078833715060'>📣</tg-emoji> "
    "Выбери, кто ты такой(–ая)...\n\n"
    "<i>* Абитуриент — тот, кто только собирается поступать в ВУЗ!</i>"
)


async def send_cached_photo(
    message: types.Message,
    filename: str,
    caption: str,
    keyboard,
) -> None:
    await delete_previous_bot_message(message.bot, message.chat.id)

    try:
        if filename not in config.MEDIA_CACHE:
            photo = FSInputFile(filename)
            sent_message = await message.answer_photo(
                photo=photo,
                caption=caption,
                reply_markup=keyboard,
            )
            config.MEDIA_CACHE[filename] = sent_message.photo[-1].file_id
            logging.info("[CACHE] Файл '%s' загружен.", filename)
        else:
            sent_message = await message.answer_photo(
                photo=config.MEDIA_CACHE[filename],
                caption=caption,
                reply_markup=keyboard,
            )
            logging.info("[CACHE] Файл '%s' отправлен из кэша.", filename)

        app_state.last_messages[message.chat.id] = sent_message.message_id
    except Exception:
        logging.exception("Ошибка при отправке медиа '%s'.", filename)
        sent_message = await message.answer(text=caption, reply_markup=keyboard)
        app_state.last_messages[message.chat.id] = sent_message.message_id


async def send_text_menu(
    message: types.Message,
    text: str,
    keyboard,
) -> None:
    await delete_previous_bot_message(message.bot, message.chat.id)
    sent_message = await message.answer(text=text, reply_markup=keyboard)
    app_state.last_messages[message.chat.id] = sent_message.message_id


async def send_main_menu(message: types.Message, text: str) -> None:
    await send_cached_photo(message, config.IMG_BANNER, text, get_main_menu())


@router.message(Command("start"), F.chat.type == "private")
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await safe_delete(message)
    await send_main_menu(message, MAIN_MENU_TEXT)


@router.callback_query(F.data == "menu_abitur", F.message.chat.type == "private")
async def process_abitur(callback: types.CallbackQuery) -> None:
    await send_text_menu(
        callback.message,
        "🎓 Раздел для абитуриентов. Что вас интересует?",
        get_abitur_menu(),
    )
    await safe_answer(callback)


@router.callback_query(F.data == "menu_student", F.message.chat.type == "private")
async def process_student(callback: types.CallbackQuery) -> None:
    await send_text_menu(
        callback.message,
        "🎒 Раздел для первокурсников. Что вас интересует?",
        get_student_menu(),
    )
    await safe_answer(callback)


@router.callback_query(F.data == "menu_main", F.message.chat.type == "private")
async def process_back(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await send_main_menu(callback.message, MAIN_MENU_TEXT)
    await safe_answer(callback)


@router.callback_query(
    F.data.in_({"abitur_balls", "abitur_docs", "student_nav", "student_docs"}),
    F.message.chat.type == "private",
)
async def process_stubs(callback: types.CallbackQuery) -> None:
    texts = {
        "abitur_balls": "📊 Здесь скоро появится информация о проходных баллах.",
        "abitur_docs": "📄 Здесь скоро появится чек-лист документов.",
        "student_nav": "🗺️ Здесь скоро появится карта корпусов и поиск аудиторий.",
        "student_docs": "📑 Здесь скоро появятся инструкции по получению справок.",
    }

    await send_text_menu(
        callback.message,
        texts.get(callback.data, "Этот раздел в разработке."),
        get_back_menu(),
    )
    await safe_answer(callback)


@router.message(F.chat.type == "private")
async def catch_all_messages(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await safe_delete(message)
    await send_main_menu(message, MAIN_MENU_TEXT)