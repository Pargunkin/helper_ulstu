import asyncio
import logging
import time

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update

from state.storage import close_db as close_bot_storage
from system import config
from handlers.anon import router as anon_router
from handlers.commands import router as commands_router
from system.console import (
    ColorFormatter,
    StatsFilter,
    StatusBar,
    play_banner,
    play_intro,
    print_goodbye,
)
from handlers.faq import router as faq_router
from handlers.logic import router as logic_router


def configure_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter())
    console_handler.addFilter(StatsFilter())
    logger.addHandler(console_handler)

    logging.getLogger("aiogram.event").setLevel(logging.INFO)


class IgnoreGroupSpamMiddleware(BaseMiddleware):
    def __init__(self, admin_group_id: int) -> None:
        self.admin_group_id = admin_group_id

    async def __call__(self, handler, event: Update, data: dict):
        message = event.message

        if (
            message is not None
            and message.chat.id == self.admin_group_id
            and message.reply_to_message is None
        ):
            return None

        return await handler(event, data)


class ExitAnonOnCommandMiddleware(BaseMiddleware):
    """Любая команда, кроме /anon, сбрасывает FSM (и выходит из анонимного режима).

    raw_state тоже обнуляется: фильтры состояний читают именно его,
    а не state.get_state(), поэтому одного state.clear() недостаточно.
    """

    async def __call__(self, handler, event, data):
        text = getattr(event, "text", None)
        state = data.get("state")
        if (
            state is not None
            and text
            and text.startswith("/")
            and not text.startswith("/anon")
        ):
            await state.clear()
            data["raw_state"] = None

        return await handler(event, data)


async def main() -> None:
    settings = config.validate_config()

    storage = MemoryStorage()
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher(storage=storage)

    dispatcher.update.outer_middleware(
        IgnoreGroupSpamMiddleware(settings.admin_group_id)
    )

    dispatcher.message.outer_middleware(ExitAnonOnCommandMiddleware())

    dispatcher.include_router(commands_router)
    dispatcher.include_router(anon_router)
    dispatcher.include_router(faq_router)
    dispatcher.include_router(logic_router)

    status_bar = StatusBar()
    try:
        bot_info = await bot.get_me()

        started = time.perf_counter()
        await bot.get_me()
        ping_ms = round((time.perf_counter() - started) * 1000)

        await play_intro()
        printed_lines = await play_banner(
            bot_info,
            extras=[
                ("Пинг API", f"{ping_ms} ms"),
                ("Роутеры", str(len(dispatcher.sub_routers))),
            ],
        )
        status_bar.start(printed_lines)

        await bot.delete_webhook(drop_pending_updates=True)
        await dispatcher.start_polling(bot)
    finally:
        await status_bar.stop()
        close_bot_storage()
        await bot.session.close()


if __name__ == "__main__":
    configure_logging()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_goodbye()
    except config.ConfigurationError as error:
        logging.error("%s", error)
    except Exception:
        logging.exception("Бот завершился из-за необработанной ошибки.")