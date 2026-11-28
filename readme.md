<p align="center">
  <img src="images/readme/welcome.png" alt="ULSTU Helper" width="100%">
</p>

<h1 align="center">Студпомощник</h1>

<p align="center">
  <b>Карманный справочник для первокурсников УлГТУ</b><br>
  Вместо долгих поисков по сайту и неловких вопросов куратору — чёткие пошаговые инструкции прямо в Telegram.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white">
  <img alt="aiogram" src="https://img.shields.io/badge/aiogram-3.x-2CA5E0">
  <img alt="SQLite" src="https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white">
  <img alt="Платформа" src="https://img.shields.io/badge/платформа-Windows%20%7C%20Linux-4B5563">
</p>

<p align="center">
  <a href="#-возможности">Возможности</a> ·
  <a href="#-структура">Структура</a> ·
  <a href="#-быстрый-старт">Быстрый старт</a> ·
  <a href="#-команды">Команды</a>
</p>

---

## ✨ Возможности

| Раздел | Что внутри |
| --- | --- |
| ❓ **FAQ** | 10 вопросов о учёбе и студенческой жизни: от БРС и академ. отпуска до сленга и поиска друзей |
| 📶 **Wi-Fi** | Пошаговая инструкция подключения к `USTU_CORP` для **Android**, **Windows** и **macOS** с кнопками «Назад» и «Далее» |
| 🏫 **Академический отпуск** | Основания, полный перечень документов, сроки, порядок оформления через ЦОС |
| 🎭 **Анонимные вопросы** | Режим `/anon`: сообщение уходит разработчикам без имени и профиля |
| 🎲 **Мелочи на день** | Цитата, факт и погода по команде |

## 🌳 Структура

`✅ готово` · `💤 заглушка` · `📝 в планах`

```
Главное меню
├── 🏆 Лидеры                    menu_leaders       💤
├── 🎒 Я — первокурсник          menu_student
│   ├── 🗺️ Навигация             student_nav        💤
│   ├── 📑 Справки               student_docs       💤
│   └── 📚 Ресурсы               student_resources  📝
└── ❓ FAQ                       menu_faq
    ├── Как не отчислиться?          faq_expelled      ✅
    ├── Я тут выживу?                faq_survive       ✅
    ├── Что такое БРС?               faq_brs           ✅
    ├── Смена направления            faq_transfer      💤
    ├── Сленг для учёбы              faq_slang         ✅
    │   └── Сленг программистов      faq_prog_slang    ✅
    ├── Академ. отпуск               faq_academic      ✅
    ├── Как найти друзей?            faq_friends       ✅
    ├── Где посидеть?                faq_study_places  ✅
    ├── Хочу Wi–Fi                   faq_wifi          ✅
    │   └── Пошаговая инструкция     wifi_guide        ✅
    │       ├── Android              wifi_os_android   ✅
    │       ├── Windows              wifi_os_windows   ✅
    │       └── macOS                wifi_os_macos     ✅
    └── Стесняюсь спросить           faq_ask_admin     ✅
```

## 🚀 Быстрый старт

```bash
git clone https://github.com/Pargunkin/helper_ulstu.git
cd helper_ulstu

python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / macOS

pip install aiogram aiohttp
```

Создай `.env` рядом с `readme.md`:

```env
BOT_TOKEN=токен_из_@BotFather
ADMIN_GROUP_ID=id_группы_для_анонимных_вопросов
```

Запуск:

```bash
python system/main.py
```

## 🛠 Требования

| Компонент | Версия |
| --- | --- |
| Python | 3.11 и выше |
| aiogram | 3.x |
| aiohttp | актуальная |
| ОС | Windows, Linux или macOS |
| Терминал | с поддержкой truecolor для цветной консоли |

## ⌨️ Команды

| Команда | Действие |
| --- | --- |
| `/start` | Главное меню |
| `/about` | О боте, команда и версия |
| `/anon` | Включить или выключить анонимный режим |
| `/quote` | Цитата дня |
| `/fact` | Факт об УлГТУ и программировании |
| `/weather` | Погода около УлГТУ или в указанном городе: `/weather Казань` |

---

<p align="center">
  <sub>Сделано студентами УлГТУ для студентов УлГТУ</sub>
</p>
