from aiogram import F, Router, types

from data.texts import FAQ_TEXTS
from services.keyboards import (
    get_faq_academic_keyboard,
    get_faq_back_button,
    get_faq_expelled_keyboard,
    get_faq_friends_keyboard,
    get_faq_menu,
    get_faq_prog_slang_keyboard,
    get_faq_slang_keyboard,
    get_faq_study_places_keyboard,
    get_faq_survive_keyboard,
    get_faq_wifi_keyboard,
)
from services.media import send_cached_album
from services.utils import delete_previous_bot_message, safe_answer
from state import storage as bot_state
from system import config

router = Router()


@router.callback_query(F.data == "menu_faq", F.message.chat.type == "private")
async def process_faq_menu(callback: types.CallbackQuery):
    await delete_previous_bot_message(callback.bot, callback.message.chat.id)

    sent_message = await callback.message.answer(
        text="<tg-emoji emoji-id='5436113877181941026'>❓</tg-emoji> <b>Часто задаваемые вопросы (<i>FAQ</i>)</b>\n\nВыбери <b>вопрос</b> или <b>категорию</b>, которые тебя интересуют, нажав на кнопку ниже...",
        reply_markup=get_faq_menu()
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
    elif callback.data == "faq_slang":
        reply_markup = get_faq_slang_keyboard()
    elif callback.data == "faq_prog_slang":
        reply_markup = get_faq_prog_slang_keyboard()
    elif callback.data == "faq_friends":
        reply_markup = get_faq_friends_keyboard()
    elif callback.data == "faq_study_places":
        reply_markup = get_faq_study_places_keyboard()
    elif callback.data == "faq_wifi":
        reply_markup = get_faq_wifi_keyboard()
    elif callback.data == "faq_academic":
        reply_markup = get_faq_academic_keyboard()
    else:
        reply_markup = get_faq_back_button()

    if callback.data == "faq_brs":
        await send_cached_album(
            callback.message,
            filenames=[config.IMG_FAQ_EXAMPLE, config.IMG_FAQ_LIST],
            caption=answer_text,
            keyboard=reply_markup,
        )
    elif callback.data == "faq_wifi":
        await send_cached_album(
            callback.message,
            filenames=[
                config.IMG_FAQ_WIFI_1,
                config.IMG_FAQ_WIFI_2,
                config.IMG_FAQ_WIFI_3,
            ],
            caption=answer_text,
            keyboard=reply_markup,
        )
    elif callback.data == "faq_study_places":
        await send_cached_album(
            callback.message,
            filenames=[
                config.IMG_FAQ_PLACES_1,
                config.IMG_FAQ_PLACES_2,
                config.IMG_FAQ_PLACES_3,
            ],
            caption=answer_text,
            keyboard=reply_markup,
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