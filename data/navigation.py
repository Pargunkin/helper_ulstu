"""Данные раздела «Карта»: корпуса, этажи и площадки кампуса."""

from pathlib import Path

CAMPUS_IMAGE = "images/navigation/campus.jpg"
AUDITORIUMS_IMAGE = "images/navigation/auditoriums.jpg"

# Корпус: (название, количество этажей, этажей в ряду)
BUILDINGS: dict[str, tuple[str, int, int]] = {
    "3": ("Корпус 3", 4, 2),
    "5": ("Корпус 5", 4, 2),
    "6": ("Корпус 6", 9, 3),
}

# Отдельные площадки
PLACES: dict[str, tuple[str, str]] = {
    "sport_new": ("«Новый» спортзал", "🏋️"),
    "sport_old": ("«Старый» спортзал", "🏋️"),
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

AUDITORIUMS_TEXT = (
    "🚪 <b>Аудитории 1–5</b>\n\n"
    "<i>Здесь будет описание, как пройти в аудитории 1–5. "
    "Из них можно попасть сразу в корпус 3 и в корпус 6.</i>"
)


def floor_image(building: str, floor: int) -> str:
    """Путь к схеме этажа. Файл можно просто положить в папку — подхватится сам."""
    return f"images/navigation/building_{building}_floor_{floor}.jpg"


def place_image(place: str) -> str:
    return f"images/navigation/place_{place}.jpg"


def has_image(path: str) -> bool:
    return Path(path).is_file()
