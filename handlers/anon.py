import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.keyboards import get_back_menu, get_end_dialog_button, get_read_button
from services.utils import delete_previous_bot_message, safe_delete
from state import storage as bot_state
from system import config


router = Router()


class AnonState(StatesGroup):
    waiting_for_question = State()


@router.message(Command("anon"), F.chat.type == "private")
async def cmd_anon(message: types.Message, state: FSMContext) -> None:
    await safe_delete(message)
    await delete_previous_bot_message(message.bot, message.chat.id)

    text = (
        "<tg-emoji emoji-id='5296369303661067030'>🔒</tg-emoji> <b>Режим анонимности включён</b>\n\n"
        "Напиши свой вопрос (<i>вообще про что угодно</i>). Я перешлю его нашим <b>разработчикам</b>. Твоё имя <b>НИКТО</b> не увидит!\n\n"
        "<i>Чтобы отменить, просто нажми на кнопку ниже <tg-emoji emoji-id='5406745015365943482'>🟢</tg-emoji></i>"
    )

    sent_message = await message.answer(text=text, reply_markup=get_back_menu())
    bot_state.last_messages[message.chat.id] = sent_message.message_id
    await state.set_state(AnonState.waiting_for_question)


@router.message(
    AnonState.waiting_for_question,
    F.chat.type == "private",
    F.text,
    ~F.text.startswith("/"),
)
async def process_anon_question(message: types.Message, state: FSMContext) -> None:
    user_question = message.html_text
    user_id = message.from_user.id

    try:
        group_msg = await message.bot.send_message(
            chat_id=config.ADMIN_GROUP_ID,
            text=(
                f"<tg-emoji emoji-id='5253742260054409879'>📩</tg-emoji> "
                f"<b>Новый анонимный вопрос:</b>\n\n"
                f"{user_question}\n\n"
                f"(<i>Ответьте на это сообщение, чтобы написать автору</i>)"
            ),
            reply_markup=get_end_dialog_button(),
        )
    except Exception:
        logging.exception("Не удалось отправить анонимный вопрос в группу разработчиков.")

        try:
            await message.answer(
                "<tg-emoji emoji-id='5447644880824181073'>⚠️</tg-emoji> "
                "Произошла ошибка на стороне сервера. Попробуйте позже..."
            )
        except Exception:
            logging.exception("Не удалось сообщить пользователю об ошибке отправки вопроса.")

        return

    bot_state.anon_threads[group_msg.message_id] = user_id
    bot_state.anon_replies[group_msg.message_id] = []

    await state.clear()
    await safe_delete(message)
    await delete_previous_bot_message(message.bot, message.chat.id)

    try:
        sent_message = await message.answer(
            "<tg-emoji emoji-id='5206607081334906820'>✅</tg-emoji> "
            "<b>Твой вопрос отправлен!</b> Ответ придёт сюда же... "
            "Можешь продолжать пользоваться ботом.",
            reply_markup=get_back_menu(),
        )
        bot_state.last_messages[message.chat.id] = sent_message.message_id
    except Exception:
        logging.exception(
            "Вопрос доставлен в группу, но не удалось отправить подтверждение пользователю."
        )


@router.message(
    AnonState.waiting_for_question,
    F.chat.type == "private",
)
async def handle_unexpected_anon_input(
    message: types.Message,
    state: FSMContext,
) -> None:
    try:
        await message.answer(
            "Пожалуйста, отправь вопрос текстовым сообщением. "
            "Режим анонимности останется включён."
        )
    except Exception:
        logging.exception(
            "Не удалось попросить пользователя отправить текстовый анонимный вопрос."
        )


@router.message(F.chat.id == config.ADMIN_GROUP_ID, F.reply_to_message)
async def handle_admin_reply(message: types.Message) -> None:
    replied_msg_id = message.reply_to_message.message_id
    student_id = bot_state.anon_threads.get(replied_msg_id)

    if not student_id:
        return

    if replied_msg_id in bot_state.anon_replies:
        bot_state.anon_replies[replied_msg_id].append(message.message_id)

    if message.text:
        reply_text = message.html_text
    else:
        reply_text = (
            "<tg-emoji emoji-id='5447644880824181073'>⚠️</tg-emoji> "
            "(<i>Разработчик отправил не текст, а медиафайл</i>)"
        )

    try:
        sent_reply = await message.bot.send_message(
            chat_id=student_id,
            text=(
                "<tg-emoji emoji-id='5443038326535759644'>💬</tg-emoji> "
                "<b>Пришёл ответ на твой вопрос:</b>\n\n"
                f"{reply_text}"
            ),
            reply_markup=get_read_button(),
        )
        bot_state.last_messages[student_id] = sent_reply.message_id
    except Exception:
        logging.exception("Не удалось отправить ответ разработчика пользователю.")
        try:
            await message.reply(
                "⚠️ <b>Ошибка:</b> возможно, пользователь заблокировал бота."
            )
        except Exception:
            logging.exception("Не удалось сообщить разработчику об ошибке доставки ответа.")

        return

    try:
        custom_reaction = types.ReactionTypeCustomEmoji(
            custom_emoji_id="5461117441612462242"
        )
        await message.react([custom_reaction])
    except Exception:
        logging.debug(
            "Не удалось поставить пользовательскую реакцию; пробуем стандартную.",
            exc_info=True,
        )
        try:
            await message.react([types.ReactionTypeEmoji(emoji="👍")])
        except Exception:
            logging.debug("Не удалось поставить стандартную реакцию.", exc_info=True)


@router.callback_query(F.data == "anon_read")
async def process_anon_read(callback: types.CallbackQuery) -> None:
    await safe_delete(callback.message)
    bot_state.last_messages.pop(callback.from_user.id, None)

    try:
        await callback.answer("Сообщение было успешно удалено")
    except Exception:
        logging.debug("Не удалось ответить на callback anon_read.", exc_info=True)


@router.callback_query(F.data == "end_dialog")
async def process_end_dialog(callback: types.CallbackQuery) -> None:
    group_msg_id = callback.message.message_id

    try:
        await callback.message.delete()
    except Exception:
        logging.exception("Не удалось удалить оригинальный вопрос из группы.")
        await callback.answer(
            "⚠️ Не удалось удалить вопрос (возможно, прошло больше 48 часов).",
            show_alert=True,
        )
        return

    replies = bot_state.anon_replies.get(group_msg_id, [])
    for msg_id in replies:
        try:
            await callback.bot.delete_message(
                chat_id=config.ADMIN_GROUP_ID,
                message_id=msg_id,
            )
        except Exception:
            logging.debug(
                "Не удалось удалить сообщение ответа %s из группы.",
                msg_id,
                exc_info=True,
            )

    bot_state.anon_threads.pop(group_msg_id, None)
    bot_state.anon_replies.pop(group_msg_id, None)

    await callback.answer("✅ Диалог завершён, чат очищен!")