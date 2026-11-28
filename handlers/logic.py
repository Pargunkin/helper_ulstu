import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from data.menu import (
    DOCS_MENU_TEXT,
    MAIN_MENU_TEXT,
    NAV_MENU_TEXT,
    RESOURCES_MENU_TEXT,
    STUDENT_MENU_TEXT,
)
from data.navigation import (
    BUILDING_MENU_TEXT,
    BUILDINGS,
    CAMPUS_IMAGE,
    FLOOR_TEXT,
    MAP_MENU_TEXT,
    PLACES,
    PLACE_TEXT,
    floor_image,
    has_image,
    place_image,
)
from data.stubs import STUB_TEXTS
from services.cache import MEDIA_CACHE
from services.keyboards import (
    get_back_menu,
    get_building_keyboard,
    get_floor_keyboard,
    get_main_menu,
    get_map_keyboard,
    get_place_keyboard,
    get_student_back_keyboard,
    get_student_docs_keyboard,
    get_student_menu,
    get_student_nav_keyboard,
    get_student_resources_keyboard,
)
from services.utils import delete_previous_bot_message, safe_answer, safe_delete
from state import storage as app_state
from system import config


router = Router()


async def send_cached_photo(
    message: types.Message,
    filename: str,
    caption: str,
    keyboard,
) -> None:
    await delete_previous_bot_message(message.bot, message.chat.id)

    try:
        if filename not in MEDIA_CACHE:
            photo = FSInputFile(filename)
            sent_message = await message.answer_photo(
                photo=photo,
                caption=caption,
                reply_markup=keyboard,
            )
            MEDIA_CACHE[filename] = sent_message.photo[-1].file_id
            logging.info("[CACHE] Файл '%s' загружен.", filename)
        else:
            sent_message = await message.answer_photo(
                photo=MEDIA_CACHE[filename],
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


@router.callback_query(F.data == "menu_student", F.message.chat.type == "private")
async def process_student(callback: types.CallbackQuery) -> None:
    await send_text_menu(
        callback.message,
        STUDENT_MENU_TEXT,
        get_student_menu(),
    )
    await safe_answer(callback)


@router.callback_query(F.data == "student_nav", F.message.chat.type == "private")
async def process_student_nav(callback: types.CallbackQuery) -> None:
    await send_text_menu(
        callback.message,
        NAV_MENU_TEXT,
        get_student_nav_keyboard(),
    )
    await safe_answer(callback)


async def send_navigation_view(
    message: types.Message,
    image: str,
    text: str,
    keyboard,
) -> None:
    """Показывает фото со схемой, а если файла ещё нет — обычный текст."""
    if has_image(image):
        await send_cached_photo(message, image, text, keyboard)
    else:
        await send_text_menu(message, text, keyboard)


@router.callback_query(F.data == "student_map", F.message.chat.type == "private")
async def process_map(callback: types.CallbackQuery) -> None:
    await send_navigation_view(
        callback.message,
        CAMPUS_IMAGE,
        MAP_MENU_TEXT,
        get_map_keyboard(),
    )
    await safe_answer(callback)


@router.callback_query(F.data.startswith("map_building_"), F.message.chat.type == "private")
async def process_map_building(callback: types.CallbackQuery) -> None:
    building = callback.data.removeprefix("map_building_")
    if building not in BUILDINGS:
        await safe_answer(callback)
        return

    title, floors = BUILDINGS[building]
    await send_text_menu(
        callback.message,
        BUILDING_MENU_TEXT.format(title=title),
        get_building_keyboard(building, floors),
    )
    await safe_answer(callback)


@router.callback_query(F.data.startswith("map_floor_"), F.message.chat.type == "private")
async def process_map_floor(callback: types.CallbackQuery) -> None:
    _, _, building, raw_floor = callback.data.split("_")
    if building not in BUILDINGS or not raw_floor.isdigit():
        await safe_answer(callback)
        return

    title, floors = BUILDINGS[building]
    floor = max(1, min(floors, int(raw_floor)))
    image = floor_image(building, floor)
    if has_image(image):
        text = f"🏢 <b>{title} · {floor} этаж</b>\n\n<i>Схема этажа.</i>"
    else:
        text = FLOOR_TEXT.format(building=title, floor=floor)
    await send_navigation_view(
        callback.message,
        image,
        text,
        get_floor_keyboard(building),
    )
    await safe_answer(callback)


@router.callback_query(F.data.startswith("map_place_"), F.message.chat.type == "private")
async def process_map_place(callback: types.CallbackQuery) -> None:
    place = callback.data.removeprefix("map_place_")
    if place not in PLACES:
        await safe_answer(callback)
        return

    title, icon = PLACES[place]
    image = place_image(place)
    if has_image(image):
        text = f"{icon} <b>{title}</b>\n\n<i>Схема расположения.</i>"
    else:
        text = PLACE_TEXT.format(icon=icon, title=title)
    await send_navigation_view(
        callback.message,
        image,
        text,
        get_place_keyboard(),
    )
    await safe_answer(callback)


@router.callback_query(F.data == "student_docs", F.message.chat.type == "private")
async def process_student_docs(callback: types.CallbackQuery) -> None:
    await send_text_menu(
        callback.message,
        DOCS_MENU_TEXT,
        get_student_docs_keyboard(),
    )
    await safe_answer(callback)


@router.callback_query(F.data == "student_resources", F.message.chat.type == "private")
async def process_student_resources(callback: types.CallbackQuery) -> None:
    await send_text_menu(
        callback.message,
        RESOURCES_MENU_TEXT,
        get_student_resources_keyboard(),
    )
    await safe_answer(callback)


@router.callback_query(F.data == "menu_main", F.message.chat.type == "private")
async def process_back(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    # Удаляем сообщение с кнопкой, чтобы оно не зависло
    await safe_delete(callback.message)
    await send_main_menu(callback.message, MAIN_MENU_TEXT)
    await safe_answer(callback)


@router.callback_query(
    F.data.in_(set(STUB_TEXTS)),
    F.message.chat.type == "private",
)
async def process_stubs(callback: types.CallbackQuery) -> None:
    keyboard = (
        get_student_back_keyboard()
        if callback.data.startswith(("student_", "docs_"))
        else get_back_menu()
    )
    await send_text_menu(
        callback.message,
        STUB_TEXTS.get(callback.data, "Этот раздел в разработке."),
        keyboard,
    )
    await safe_answer(callback)


@router.message(F.chat.type == "private")
async def catch_all_messages(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await safe_delete(message)
    await send_main_menu(message, MAIN_MENU_TEXT)