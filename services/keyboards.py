from aiogram import types

from data.emoji import (
    ICON_ABITUR,
    ICON_BACK,
    ICON_BACK_FAQ,
    ICON_BOOK,
    ICON_CHAT,
    ICON_DELETE,
    ICON_DORM,
    ICON_EXPELLED,
    ICON_FAQ,
    ICON_HELP,
    ICON_PROGRAMMING,
    ICON_QUEEN,
    ICON_READ,
    ICON_RESOURCES,
    ICON_SMILE,
    ICON_SPORT,
    ICON_STUDENT,
    ICON_TRANSFER,
    ICON_TRANSLATE,
    ICON_WIFI,
)

def get_main_menu():
    kb = [
        [
            types.InlineKeyboardButton(
                text="Я — абитуриент", 
                callback_data="menu_abitur",
                icon_custom_emoji_id=ICON_ABITUR
            )
        ],
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
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_abitur_menu():
    kb = [
        [types.InlineKeyboardButton(text="📊 Проходные баллы", callback_data="abitur_balls")],
        [types.InlineKeyboardButton(text="📄 Документы", callback_data="abitur_docs")],
        [
            types.InlineKeyboardButton(
                text="Назад в меню", 
                callback_data="menu_main",
                icon_custom_emoji_id=ICON_BACK
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb)

def get_student_menu():
    kb = [
        [types.InlineKeyboardButton(text="🗺️ Навигация", callback_data="student_nav")],
        [types.InlineKeyboardButton(text="📑 Справки", callback_data="student_docs")],
        [
            types.InlineKeyboardButton(
                text="Назад в меню", 
                callback_data="menu_main",
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
            types.InlineKeyboardButton(text="Смена направления", callback_data="faq_transfer", icon_custom_emoji_id=ICON_TRANSFER)
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