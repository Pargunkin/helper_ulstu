"""Функции отправки медиа с кэшированием file_id."""

import logging

from aiogram import types
from aiogram.types import FSInputFile

from services.cache import MEDIA_CACHE
from services.utils import delete_previous_bot_message
from state import storage as app_state


async def send_cached_photo(
    message: types.Message,
    filename: str,
    caption: str,
    keyboard,
) -> None:
    await delete_previous_bot_message(message.bot, message.chat.id)

    try:
        sent_message = None

        if filename in MEDIA_CACHE:
            try:
                sent_message = await message.answer_photo(
                    photo=MEDIA_CACHE[filename],
                    caption=caption,
                    reply_markup=keyboard,
                )
                logging.info("[CACHE] Файл '%s' отправлен из кэша.", filename)
            except Exception:
                logging.warning(
                    "[CACHE] file_id для '%s' устарел, перезагружаю файл.", filename
                )
                MEDIA_CACHE.pop(filename, None)

        if sent_message is None:
            photo = FSInputFile(filename)
            sent_message = await message.answer_photo(
                photo=photo,
                caption=caption,
                reply_markup=keyboard,
            )
            MEDIA_CACHE[filename] = sent_message.photo[-1].file_id
            logging.info("[CACHE] Файл '%s' загружен.", filename)

        app_state.last_messages[message.chat.id] = sent_message.message_id
    except Exception:
        logging.exception("Ошибка при отправке медиа '%s'.", filename)
        MEDIA_CACHE.pop(filename, None)
        sent_message = await message.answer(text=caption, reply_markup=keyboard)
        app_state.last_messages[message.chat.id] = sent_message.message_id


async def send_cached_album(
    message: types.Message,
    filenames: list[str],
    caption: str,
    keyboard,
) -> None:
    """Отправляет альбом из нескольких фото с кэшированием file_id."""
    await delete_previous_bot_message(message.bot, message.chat.id)

    try:
        album = None

        if all(f in MEDIA_CACHE for f in filenames):
            try:
                album = await message.answer_media_group(
                    media=[
                        types.InputMediaPhoto(media=MEDIA_CACHE[f])
                        for f in filenames
                    ]
                )
                logging.info("[CACHE] Альбом отправлен из кэша.")
            except Exception:
                logging.warning(
                    "[CACHE] Устаревшие file_id в альбоме, перезагружаю с диска."
                )
                for f in filenames:
                    MEDIA_CACHE.pop(f, None)

        if album is None:
            album = await message.answer_media_group(
                media=[
                    types.InputMediaPhoto(media=FSInputFile(f))
                    for f in filenames
                ]
            )
            logging.info("[CACHE] Альбом загружен с диска.")

            for i, f in enumerate(filenames):
                if i < len(album):
                    MEDIA_CACHE[f] = album[i].photo[-1].file_id

        text_message = await message.answer(
            text=caption,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

        app_state.last_messages[message.chat.id] = [
            *(item.message_id for item in album),
            text_message.message_id,
        ]
    except Exception as error:
        logging.exception("Ошибка при отправке альбома: %s", error)
        for f in filenames:
            MEDIA_CACHE.pop(f, None)
        sent_message = await message.answer(
            text=caption,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )
        app_state.last_messages[message.chat.id] = sent_message.message_id