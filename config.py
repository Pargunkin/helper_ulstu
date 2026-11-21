import os
from dataclasses import dataclass
from pathlib import Path


class ConfigurationError(ValueError):
    pass


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_group_id: int


def load_dotenv(path: str | os.PathLike[str] | None = None) -> None:
    if path is None:
        path = Path(__file__).resolve().parent / ".env"
    else:
        path = Path(path)

    if not path.is_file():
        return

    with path.open("r", encoding="utf-8-sig") as file:
        for raw_line in file:
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("export "):
                line = line[len("export "):].lstrip()

            if "=" not in line:
                continue

            key, value = line.split("=", maxsplit=1)
            key = key.strip()
            value = value.strip()

            if not key:
                continue

            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            else:
                value = value.split(" #", maxsplit=1)[0].rstrip()

            os.environ.setdefault(key, value)


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip() or None

_ADMIN_GROUP_ID_RAW = os.getenv("ADMIN_GROUP_ID", "").strip()
_ADMIN_GROUP_ID_ERROR: str | None = None

try:
    ADMIN_GROUP_ID = int(_ADMIN_GROUP_ID_RAW) if _ADMIN_GROUP_ID_RAW else None
except ValueError:
    ADMIN_GROUP_ID = None
    _ADMIN_GROUP_ID_ERROR = "ADMIN_GROUP_ID должен быть целым числом."

MEDIA_CACHE: dict[str, str] = {}

IMG_BANNER = "images/banner.png"
IMG_ABOUT = "images/about.png"
IMG_FAQ_EXAMPLE = "images/faq/example.jpg"
IMG_FAQ_LIST = "images/faq/list.jpg"

def validate_config() -> Settings:
    errors: list[str] = []

    if not BOT_TOKEN:
        errors.append("не задан BOT_TOKEN")

    if _ADMIN_GROUP_ID_ERROR:
        errors.append(_ADMIN_GROUP_ID_ERROR)
    elif ADMIN_GROUP_ID is None:
        errors.append("не задан ADMIN_GROUP_ID")
    elif ADMIN_GROUP_ID == 0:
        errors.append("ADMIN_GROUP_ID не может быть равен 0")

    if errors:
        details = "\n".join(f"  - {error}" for error in errors)
        raise ConfigurationError(
            "Не удалось запустить бота: проверьте настройки в .env "
            "или переменные окружения:\n"
            f"{details}"
        )

    return Settings(
        bot_token=BOT_TOKEN,
        admin_group_id=ADMIN_GROUP_ID,
    )