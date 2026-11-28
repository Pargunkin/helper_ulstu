from aiogram import types

from data.emoji import (
    ICON_BACK,
    ICON_BACK_FAQ,
    ICON_BOOK,
    ICON_CHAT,
    ICON_DELETE,
    ICON_DORM,
    ICON_EXPELLED,
    ICON_FAQ,
    ICON_GUIDE,
    ICON_HELP,
    ICON_LEADERS,
    ICON_NEXT,
    ICON_OS_BACK,
    ICON_PREV,
    ICON_PROGRAMMING,
    ICON_QUEEN,
    ICON_READ,
    ICON_RESOURCES,
    ICON_SMILE,
    ICON_SPORT,
    ICON_STUDENT,
    ICON_STUDENT_CENTER,
    ICON_TRANSFER,
    ICON_TRANSLATE,
    ICON_WIFI,
)
from data.faq.wifi_guide import OS_ORDER, WIFI_OS

STUDENT_CENTER_URL = "https://ulstu.ru/for_student/cos/"

def get_main_menu():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Я — первокурсник",
                callback_data="menu_student",
                icon_custom_emoji_id=ICON_STUDENT
            )
        ],
        [
            types.InlineKeyboardButton(
                text="FAQ",
                callback_data="menu_faq",
                icon_custom_emoji_id=ICON_FAQ
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Лидеры",
                callback_data="menu_leaders",
                icon_custom_emoji_id=ICON_LEADERS
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_student_menu():
    kb = [
        [
            types.InlineKeyboardButton(text="🗺️ Навигация", callback_data="student_nav"),
            types.InlineKeyboardButton(text="🔔 Звонки", callback_data="student_bell")
        ],
        [
            types.InlineKeyboardButton(text="💰 Стипендии", callback_data="student_scholarship"),
            types.InlineKeyboardButton(text="🏃 Физкультура", callback_data="student_sport")
        ],
        [
            types.InlineKeyboardButton(text="📚 Ресурсы", callback_data="student_resources"),
            types.InlineKeyboardButton(text="📑 Справки", callback_data="student_docs")
        ],
        [
            types.InlineKeyboardButton(
                text="Назад в меню",
                callback_data="menu_main",
                icon_custom_emoji_id=ICON_BACK
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def get_student_nav_keyboard():
    kb = [
        [types.InlineKeyboardButton(text="🗺️ Карта", callback_data="student_map")],
        [types.InlineKeyboardButton(text="🌐 Навигация по сайту", callback_data="student_site")],
        [
            types.InlineKeyboardButton(
                text="Назад",
                callback_data="menu_student",
                icon_custom_emoji_id=ICON_BACK
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def get_map_keyboard():
    kb = [
        [types.InlineKeyboardButton(text="🚪 Аудитории 1–5", callback_data="map_auditoriums")],
        [
            types.InlineKeyboardButton(text="🏢 Корпус 3", callback_data="map_building_3"),
            types.InlineKeyboardButton(text="🏢 Корпус 5", callback_data="map_building_5"),
            types.InlineKeyboardButton(text="🏢 Корпус 6", callback_data="map_building_6")
        ],
        [
            types.InlineKeyboardButton(text="🏋️ «Новый» спортзал", callback_data="map_place_sport_new"),
            types.InlineKeyboardButton(text="🏋️ «Старый» спортзал", callback_data="map_place_sport_old")
        ],
        [types.InlineKeyboardButton(text="🛸 Фойе РЦНТК «Тарелка»", callback_data="map_place_tarelka")],
        [
            types.InlineKeyboardButton(
                text="Назад",
                callback_data="student_nav",
                icon_custom_emoji_id=ICON_BACK
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def get_building_keyboard(
    building: str,
    floors: int,
    per_row: int = 2,
    with_auditoriums: bool = False,
):
    buttons = [
        types.InlineKeyboardButton(
            text=f"{floor} этаж",
            callback_data=f"map_floor_{building}_{floor}"
        )
        for floor in range(1, floors + 1)
    ]

    kb = [buttons[index:index + per_row] for index in range(0, len(buttons), per_row)]
    if with_auditoriums:
        kb.insert(
            0,
            [types.InlineKeyboardButton(text="🚪 Аудитории 1–5", callback_data="map_auditoriums")],
        )
    kb.append([
        types.InlineKeyboardButton(
            text="Назад к карте",
            callback_data="student_map",
            icon_custom_emoji_id=ICON_BACK
        )
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def get_floor_keyboard(building: str):
    kb = [
        [
            types.InlineKeyboardButton(
                text="Назад к этажам",
                callback_data=f"map_building_{building}",
                icon_custom_emoji_id=ICON_BACK
            )
        ],
        [types.InlineKeyboardButton(text="На карту", callback_data="student_map")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def get_auditoriums_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(text="🏢 Корпус 3", callback_data="map_building_3"),
            types.InlineKeyboardButton(text="🏢 Корпус 6", callback_data="map_building_6")
        ],
        [
            types.InlineKeyboardButton(
                text="На карту",
                callback_data="student_map",
                icon_custom_emoji_id=ICON_BACK
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def get_place_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(
                text="На карту",
                callback_data="student_map",
                icon_custom_emoji_id=ICON_BACK
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def get_student_docs_keyboard():
    kb = [
        [types.InlineKeyboardButton(text="🪖 Воинский учёт", callback_data="docs_military")],
        [types.InlineKeyboardButton(text="🏅 Справка для физкультуры", callback_data="docs_sport")],
        [types.InlineKeyboardButton(text="🎫 Потеря пропуска", callback_data="docs_pass")],
        [types.InlineKeyboardButton(text="📇 Потеря студенческого", callback_data="docs_student_id")],
        [
            types.InlineKeyboardButton(
                text="Назад",
                callback_data="menu_student",
                icon_custom_emoji_id=ICON_BACK
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def get_student_resources_keyboard():
    kb = [
        [types.InlineKeyboardButton(text="💻 Программное обеспечение", callback_data="student_software")],
        [types.InlineKeyboardButton(text="📇 Контакты", callback_data="student_contacts")],
        [types.InlineKeyboardButton(text="🏢 Центр обслуживания студентов", callback_data="student_center")],
        [
            types.InlineKeyboardButton(
                text="Назад",
                callback_data="menu_student",
                icon_custom_emoji_id=ICON_BACK
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_back_menu():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Назад в меню", 
                callback_data="menu_main",
                icon_custom_emoji_id=ICON_BACK
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_student_back_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Назад",
                callback_data="menu_student",
                icon_custom_emoji_id=ICON_BACK
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def get_read_button():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Прочитано", 
                callback_data="anon_read",
                icon_custom_emoji_id=ICON_READ
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_faq_menu():
    kb = [
        [
            types.InlineKeyboardButton(text="Как не отчислиться?", callback_data="faq_expelled", icon_custom_emoji_id=ICON_EXPELLED),
            types.InlineKeyboardButton(text="Я тут выживу?", callback_data="faq_survive", icon_custom_emoji_id=ICON_HELP)
        ],
        [
            types.InlineKeyboardButton(text="Что такое БРС?", callback_data="faq_brs", icon_custom_emoji_id=ICON_BOOK),
            types.InlineKeyboardButton(text="Перевод на бюджет", callback_data="faq_transfer", icon_custom_emoji_id=ICON_TRANSFER)
        ],
        [
            types.InlineKeyboardButton(text="Сленг для учёбы", callback_data="faq_slang", icon_custom_emoji_id=ICON_TRANSLATE),
            types.InlineKeyboardButton(text="Академ. отпуск", callback_data="faq_academic", icon_custom_emoji_id=ICON_QUEEN)
        ],
        [
            types.InlineKeyboardButton(text="Как найти друзей?", callback_data="faq_friends", icon_custom_emoji_id=ICON_CHAT),
            types.InlineKeyboardButton(text="Где посидеть?", callback_data="faq_study_places", icon_custom_emoji_id=ICON_DORM)
        ],
        [
            types.InlineKeyboardButton(text="Хочу Wi–Fi", callback_data="faq_wifi", icon_custom_emoji_id=ICON_WIFI),
            types.InlineKeyboardButton(text="Стесняюсь спросить", callback_data="faq_ask_admin", icon_custom_emoji_id=ICON_FAQ)
        ],
        [
            types.InlineKeyboardButton(
                text="Назад в меню", 
                callback_data="menu_main",
                icon_custom_emoji_id=ICON_BACK
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_faq_back_button():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Назад в FAQ", 
                callback_data="menu_faq",
                icon_custom_emoji_id=ICON_BACK_FAQ
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_end_dialog_button():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Закончить диалог", 
                callback_data="end_dialog",
                icon_custom_emoji_id=ICON_DELETE
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_faq_survive_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Назад в FAQ", 
                callback_data="menu_faq",
                icon_custom_emoji_id=ICON_BACK_FAQ
            ),
            types.InlineKeyboardButton(
                text="Как не отчислиться?", 
                callback_data="faq_expelled",
                icon_custom_emoji_id=ICON_EXPELLED
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_faq_expelled_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Назад в FAQ", 
                callback_data="menu_faq",
                icon_custom_emoji_id=ICON_BACK_FAQ
            ),
            types.InlineKeyboardButton(
                text="Академ. отпуск", 
                callback_data="faq_academic",
                icon_custom_emoji_id=ICON_QUEEN
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_faq_slang_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Назад в FAQ", 
                callback_data="menu_faq",
                icon_custom_emoji_id=ICON_BACK_FAQ
            ),
            types.InlineKeyboardButton(
                text="Программистский сленг", 
                callback_data="faq_prog_slang",
                icon_custom_emoji_id=ICON_PROGRAMMING
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_faq_prog_slang_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Назад в сленг", 
                callback_data="faq_slang",
                icon_custom_emoji_id=ICON_TRANSLATE
            ),
            types.InlineKeyboardButton(
                text="Назад в FAQ", 
                callback_data="menu_faq",
                icon_custom_emoji_id=ICON_BACK_FAQ
            )
            
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_faq_friends_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Назад в FAQ", 
                callback_data="menu_faq",
                icon_custom_emoji_id=ICON_BACK_FAQ
            ),
            types.InlineKeyboardButton(
                text="Ресурсы", 
                callback_data="student_resources", 
                icon_custom_emoji_id=ICON_RESOURCES
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_faq_wifi_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Пошаговая инструкция",
                callback_data="wifi_guide",
                icon_custom_emoji_id=ICON_GUIDE
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Назад в FAQ",
                callback_data="menu_faq",
                icon_custom_emoji_id=ICON_BACK_FAQ
            ),
            types.InlineKeyboardButton(
                text="Где посидеть?",
                callback_data="faq_study_places",
                icon_custom_emoji_id=ICON_DORM
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def get_wifi_os_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(
                text=WIFI_OS[key]["title"],
                callback_data=f"wifi_os_{key}",
                icon_custom_emoji_id=WIFI_OS[key]["emoji_id"]
            )
            for key in OS_ORDER
        ],
        [
            types.InlineKeyboardButton(
                text="Назад в Wi–Fi",
                callback_data="faq_wifi",
                icon_custom_emoji_id=ICON_WIFI
            ),
            types.InlineKeyboardButton(
                text="Назад в FAQ",
                callback_data="menu_faq",
                icon_custom_emoji_id=ICON_BACK_FAQ
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def get_wifi_step_keyboard(os_key: str, index: int, total: int):
    """index — с нуля. На первом шаге нет «Назад», на последнем — «Далее»."""
    kb = []

    if index == 0:
        kb.append([
            types.InlineKeyboardButton(
                text="Далее",
                callback_data=f"wifi_step_{os_key}_{index + 2}",
                icon_custom_emoji_id=ICON_NEXT
            )
        ])
    elif index >= total - 1:
        kb.append([
            types.InlineKeyboardButton(
                text="Назад",
                callback_data=f"wifi_step_{os_key}_{index}",
                icon_custom_emoji_id=ICON_PREV
            )
        ])
    else:
        kb.append([
            types.InlineKeyboardButton(
                text="Назад",
                callback_data=f"wifi_step_{os_key}_{index}",
                icon_custom_emoji_id=ICON_PREV
            ),
            types.InlineKeyboardButton(
                text="Далее",
                callback_data=f"wifi_step_{os_key}_{index + 2}",
                icon_custom_emoji_id=ICON_NEXT
            )
        ])

    kb.append([
        types.InlineKeyboardButton(
            text="Назад к ОС",
            callback_data="wifi_guide",
            icon_custom_emoji_id=ICON_OS_BACK
        ),
        types.InlineKeyboardButton(
            text="Назад в FAQ",
            callback_data="menu_faq",
            icon_custom_emoji_id=ICON_BACK_FAQ
        )
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=kb)


def get_faq_academic_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Назад в FAQ",
                callback_data="menu_faq",
                icon_custom_emoji_id=ICON_BACK_FAQ
            ),
            types.InlineKeyboardButton(
                text="Как не отчислиться?",
                callback_data="faq_expelled",
                icon_custom_emoji_id=ICON_EXPELLED
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Центр обслуживания студентов",
                url=STUDENT_CENTER_URL,
                icon_custom_emoji_id=ICON_STUDENT_CENTER
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_faq_study_places_keyboard():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Назад в FAQ", 
                callback_data="menu_faq",
                icon_custom_emoji_id=ICON_BACK_FAQ
            ),
            types.InlineKeyboardButton(
                text="Хочу Wi–Fi", 
                callback_data="faq_wifi",
                icon_custom_emoji_id=ICON_WIFI
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)