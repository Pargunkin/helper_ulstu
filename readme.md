<p align="center">
  <img src="images/readme/welcome.png" alt="Баннер ULSTU Helper" width="100%">
</p>
<h1 align="center">
  <span>Студпомощник</span>
</h1>
<p align="center">
  <strong>«Студпомощник»</strong> — <strong>удобный карманный справочник</strong> для абитуриентов и первокурсников <a href="https://ulstu.ru/">УлГТУ</a>. Он решает проблему разрозненной и сложной подачи информации: <strong>вместо долгих поисков по сайту</strong> или <strong>неловких вопросов куратору</strong>, студент получает <strong>чёткие пошаговые инструкции</strong> прямо в мессенджере.
</p>
<h3 align="center">
  <a href="#-установка">Установка</a>
  <span> · </span>
  <a href="#-требования">Требования</a>
  <span> · </span>
  <a href="CHANGELOG.md">История изменений</a>
</h3>

## 📦 Установка

Какой-то допустим текст...
<br/>
<details>
<summary><strong>Установка Git Bash</strong></summary>
<br/>
Какой-то текст для инструкции.
</details>

## 🛠 Требования

- Какой-то там допустим Visual Studio и прочее-прочее

## 🌳 Структура

Легенда: ✅ готово · 💤 заглушка · 📝 в планах

```
Главное меню
├── 🏆 Лидеры                  menu_leaders      💤 заглушка
├── 🎒 Я — первокурсник        menu_student
│   ├── 🗺️ Навигация           student_nav       💤 карта корпусов
│   ├── 📑 Справки             student_docs      💤 инструкции по справкам
│   └── 📚 Ресурсы             student_resources 📝 раздел в разработке
└── ❓ FAQ                     menu_faq
    ├── Как не отчислиться?        faq_expelled     ✅
    ├── Я тут выживу?              faq_survive      ✅
    ├── Что такое БРС?             faq_brs          ✅
    ├── Смена направления          faq_transfer     💤
    ├── Сленг для учёбы            faq_slang        ✅
    │   └── Сленг программистов    faq_prog_slang   ✅
    ├── Академ. отпуск             faq_academic     ✅
    ├── Как найти друзей?          faq_friends      ✅
    ├── Где посидеть?              faq_study_places ✅
    ├── Хочу Wi–Fi                 faq_wifi         ✅
    │   └── Пошаговая инструкция   wifi_guide       ✅
    │       ├── Android            wifi_os_android  ✅
    │       ├── Windows            wifi_os_windows  ✅
    │       └── macOS              wifi_os_macos    ✅
    └── Стесняюсь спросить         faq_ask_admin    ✅
```

### Файлы

```
data/        тексты и данные (FAQ, эмодзи, заглушки)
handlers/    обработчики Telegram-событий
services/    клавиатуры, кэш медиа, сборка сообщений
state/       хранилище состояния и SQLite
system/      конфигурация, консоль, точка входа
```
