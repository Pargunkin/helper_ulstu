import asyncio
import logging

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update

import config
from anon import router as anon_router
from commands import router as commands_router
from console import Colors, play_intro, print_banner
from faq import router as faq_router
from logic import router as logic_router


class ColorFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: (
            Colors.CYAN
            + "[%(asctime)s]"
            + Colors.RESET
            + " "
            + Colors.CYAN
            + "%(levelname)s"
            + Colors.RESET
            + ": %(message)s"
        ),
        logging.INFO: (
            Colors.CYAN
            + "[%(asctime)s]"
            + Colors.RESET
            + " "
            + Colors.GREEN
            + "%(levelname)s"
            + Colors.RESET
            + ": %(message)s"
        ),
        logging.WARNING: (
            Colors.CYAN
            + "[%(asctime)s]"
            + Colors.RESET
            + " "
            + Colors.YELLOW
            + "%(levelname)s"
            + Colors.RESET
            + ": %(message)s"
        ),
        logging.ERROR: (
            Colors.CYAN
            + "[%(asctime)s]"
            + Colors.RESET
            + " "
            + Colors.RED
            + "%(levelname)s"
            + Colors.RESET
            + ": %(message)s"
        ),
        logging.CRITICAL: (
            Colors.CYAN
            + "[%(asctime)s]"
            + Colors.RESET
            + " "
            + Colors.RED
            + Colors.BOLD
            + "%(levelname)s"
            + Colors.RESET
            + ": %(message)s"
        ),
    }

    def format(self, record: logging.LogRecord) -> str:
        log_format = self.FORMATS.get(record.levelno, self.FORMATS[logging.INFO])
        formatter = logging.Formatter(log_format, datefmt="%H:%M:%S")
        return formatter.format(record)


def configure_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter())
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

    dispatcher.include_router(anon_router)
    dispatcher.include_router(commands_router)
    dispatcher.include_router(faq_router)
    dispatcher.include_router(logic_router)

    await play_intro()
    print_banner()

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    configure_logging()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}🛑 Бот остановлен. До встречи!{Colors.RESET}")
    except config.ConfigurationError as error:
        logging.error("%s", error)
    except Exception:
        logging.exception("Бот завершился из-за необработанной ошибки.")