"""Данные раздела «Карта»: корпуса, этажи и площадки кампуса."""

from pathlib import Path

CAMPUS_IMAGE = "images/navigation/campus.jpg"

# Корпуса и количество этажей
BUILDINGS: dict[str, tuple[str, int]] = {
    "3": ("Корпус 3", 4),
    "6": ("Корпус 6", 9),
}

# Отдельные площадки
PLACES: dict[str, tuple[str, str]] = {
    "sport": ("Спортзал", "🏋️"),
    "tarelka": ("Фойе РЦНТК «Тарелка»", "🛸"),
}

MAP_MENU_TEXT = (
    "🗺️ <b>Карта</b>\n\n"
    "Выбери корпус или площадку. Внутри корпусов — этажи, "
    "а на этажах будут схемы аудиторий."
)

BUILDING_MENU_TEXT = "🏢 <b>{title}</b>\n\nВыбери этаж:"

FLOOR_TEXT = (
    "🏢 <b>{building} · {floor} этаж</b>\n\n"
    "<i>Здесь будет схема этажа: аудитории, лестницы и выходы...</i>"
)

PLACE_TEXT = (
    "{icon} <b>{title}</b>\n\n"
    "<i>Здесь будет описание и схема, как найти это место...</i>"
)


def floor_image(building: str, floor: int) -> str:
    """Путь к схеме этажа. Файл можно просто положить в папку — подхватится сам."""
    return f"images/navigation/building_{building}_floor_{floor}.jpg"


def place_image(place: str) -> str:
    return f"images/navigation/place_{place}.jpg"


def has_image(path: str) -> bool:
    return Path(path).is_file()
