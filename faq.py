import logging

from aiogram import F, Router, types

import config
import state as bot_state
from keyboards import (
    get_faq_back_button,
    get_faq_expelled_keyboard,
    get_faq_menu,
    get_faq_survive_keyboard,
)
from utils import delete_previous_bot_message, safe_answer

router = Router()

FAQ_TEXTS = {
    "faq_expelled": (
        "<tg-emoji emoji-id='5447544503143504937'>😫</tg-emoji> "
        "<b>Как не отчислиться?</b>\n\n"
        "Хотелось бы подчеркнуть несколько фактов, которые необходимо "
        "всегда держать в голове:\n"
    ),
    "faq_survive": (
        "<tg-emoji emoji-id='5386535377467094223'>🍞</tg-emoji> "
        "<b>Я тут вообще выживу?</b>\n\n"
        "Почти наверняка — да."
    ),
    "faq_brs": (
        "<tg-emoji emoji-id='5341498088408234504'>💯</tg-emoji> "
        "<b>Что такое БРС?</b>\n\n"
        "<blockquote><b>БРС</b> — балльно–рейтинговая система — способ "
        "оценивания, при котором ты получаешь баллы за семестр и сдаёшь "
        "экзамен на основании набранных баллов.</blockquote>\n\n"
        "<b>Если кратко:</b> у дисциплины есть максимальное количество "
        "баллов, которое можно набрать.\n\n"
        "Для отслеживания своих результатов обращайся в раздел "
        "<b>«Обучение»</b> в ЛМС УлГТУ."
    ),
    "faq_transfer": "Не доделал...",
    "faq_slang": "Не доделал...",
    "faq_academic": "Не доделал...",
    "faq_friends": "Не доделал...",
    "faq_study_places": "Не доделал...",
    "faq_smile": "Не доделал...",
    "faq_ask_admin": "Не доделал...",
}


@router.callback_query(F.data == "menu_faq", F.message.chat.type == "private")
async def process_faq_menu(callback: types.CallbackQuery):
    await delete_previous_bot_message(callback.bot, callback.message.chat.id)

    sent_message = await callback.message.answer(
        text=(
            "<tg-emoji emoji-id='5436113877181941026'>❓</tg-emoji> "
            "<b>Часто задаваемые вопросы (<i>FAQ</i>)</b>\n\n"
            "Выбери вопрос или категорию, которые тебя интересуют."
        ),
        reply_markup=get_faq_menu(),
    )
    bot_state.last_messages[callback.message.chat.id] = sent_message.message_id
    await safe_answer(callback)


@router.callback_query(F.data.startswith("faq_"), F.message.chat.type == "private")
async def process_faq_item(callback: types.CallbackQuery):
    answer_text = FAQ_TEXTS[callback.data]

    await delete_previous_bot_message(callback.bot, callback.message.chat.id)

    if callback.data == "faq_survive":
        reply_markup = get_faq_survive_keyboard()
    elif callback.data == "faq_expelled":
        reply_markup = get_faq_expelled_keyboard()
    else:
        reply_markup = get_faq_back_button()

    if callback.data == "faq_brs":
        try:
            album = await callback.message.answer_media_group(
                media=[
                    types.InputMediaPhoto(
                        media=types.FSInputFile(config.IMG_FAQ_EXAMPLE)
                    ),
                    types.InputMediaPhoto(
                        media=types.FSInputFile(config.IMG_FAQ_LIST)
                    ),
                ]
            )

            text_message = await callback.message.answer(
                text=answer_text,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
            )

            bot_state.last_messages[callback.message.chat.id] = [
                *(item.message_id for item in album),
                text_message.message_id,
            ]
        except Exception as error:
            logging.exception("Ошибка при отправке фото БРС: %s", error)
            sent_message = await callback.message.answer(
                text=answer_text,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
            )
            bot_state.last_messages[callback.message.chat.id] = (
                sent_message.message_id
            )
    else:
        sent_message = await callback.message.answer(
            text=answer_text,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )
        bot_state.last_messages[callback.message.chat.id] = (
            sent_message.message_id
        )

    await safe_answer(callback)