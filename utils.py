import logging

from aiogram import Bot, types

import state


async def safe_delete(message: types.Message) -> None:
    try:
        if (
            message.chat.type == "private"
            and message.from_user
            and message.from_user.id == message.chat.id
        ):
            if message.chat.id not in state.saved_first_messages:
                state.saved_first_messages[message.chat.id] = True
                return

        await message.delete()
    except Exception:
        logging.debug(
            "Не удалось удалить сообщение %s в чате %s.",
            message.message_id,
            message.chat.id,
            exc_info=True,
        )


async def safe_answer(callback: types.CallbackQuery) -> None:
    try:
        await callback.answer()
    except Exception:
        logging.debug("Не удалось ответить на callback.", exc_info=True)


async def delete_previous_bot_message(bot: Bot, chat_id: int) -> None:
    message_ids = state.last_messages.get(chat_id)

    if not message_ids:
        return

    if isinstance(message_ids, list):
        ids_to_delete = message_ids
    else:
        ids_to_delete = [message_ids]

    for message_id in ids_to_delete:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception:
            logging.debug(
                "Не удалось удалить предыдущее сообщение %s в чате %s.",
                message_id,
                chat_id,
                exc_info=True,
            )

    state.last_messages.pop(chat_id, None)