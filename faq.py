import logging

from aiogram import F, Router, types

import config
import state as bot_state
from keyboards import (
    get_faq_back_button,
    get_faq_expelled_keyboard,
    get_faq_menu,
    get_faq_survive_keyboard,
    get_faq_slang_keyboard,
    get_faq_prog_slang_keyboard,
    get_faq_friends_keyboard,
    get_faq_study_places_keyboard,
)
from utils import delete_previous_bot_message, safe_answer

router = Router()

FAQ_TEXTS = {
    # Страхи перед отчислением
    "faq_expelled": """<tg-emoji emoji-id='5447544503143504937'>😫</tg-emoji> <b>Как не отчислиться?</b>

Хотелось бы подчеркнуть <b>несколько фактов</b>, которые необходимо всегда держать в голове:
<tg-emoji emoji-id='5440431740948599226'>1️⃣</tg-emoji> ВУЗу <b><u>не</u> нравится</b> терять студентов как минимум по одной причине: приходится <b>сокращать</b> ставку преподавателя. Поэтому отчисление — <b>крайняя мера</b>. Это означает, что дверь для диалога <b>почти всегда открыта!</b>
<tg-emoji emoji-id='5233568665521116311'>2️⃣</tg-emoji> Отчисляют почти никогда не за <b>отсутствие способностей</b>, а за <b>потерю контроля над учебным процессом</b>.
<tg-emoji emoji-id='5233584930562264124'>3️⃣</tg-emoji> <b>Долги и задолженности</b> в ВУЗе не являются концом света: они <u>были</u>, <u>есть</u> и <u>будут</u>.

Если вы ещё не поступили, а <b>уже беспокоитесь</b>, — это <b>замечательно</b>. Вот что хотелось бы отметить:
<tg-emoji emoji-id='5314581682983032296'>1️⃣</tg-emoji> <b>Стоит изучить правила игры.</b> Узнай, как в ВУЗе устроены БРС (<i>балльно–рейтинговая система</i>), пересдачи, допуск к экзаменам, что считается «автоматом».
<tg-emoji emoji-id='5316616750157020011'>2️⃣</tg-emoji> <b>Не пропускай вводные пары</b> «потому что там ничего интересного не будет» — именно на них ты ознакамливаешься с характером преподавателей и требованиями, форматом аттестации.
<tg-emoji emoji-id='5316590160014488998'>3️⃣</tg-emoji> <b>Заведи знакомства: одногруппники</b> — конспекты, взаимопомощь и информация; <b>старшекурсники</b> — знания о том, какие преподаватели строгие, где брать материалы и как реально сдаются предметы.

<tg-emoji emoji-id='5368464165130225746'>1️⃣</tg-emoji> Записывай каждое <b>домашнее задание</b>, каждый <b>дедлайн</b> в момент, <b>когда их озвучили</b>, в одно место — <u>календарь с напоминаниями</u>, а не в «блокнот, который потеряется».
<tg-emoji emoji-id='5370982398945150957'>2️⃣</tg-emoji> Делай <b>мелкие домашние задания</b> (<i>например: историю, английский язык, деловые коммуникации</i>) <b>в тот же день</b>, когда их задали.
<tg-emoji emoji-id='5368784887518089173'>3️⃣</tg-emoji> Выполняй <b>лабораторные</b> или <b>практические работы</b> по порядку. Если идеального понимания каждой темы не добьёшься, то хотя бы будешь <b>постепенно</b> укладывать всё в голове.
<tg-emoji emoji-id='5370639334137418113'>4️⃣</tg-emoji> Веди конспект так, чтобы <b>им можно было пользоваться перед сессией</b>, а не переписывать заново в декабре.
<tg-emoji emoji-id='5368549841137846718'>5️⃣</tg-emoji> Возможно, это <i>звучит смешно на первый взгляд</i>, но <b>соблюдай гигиену:</b> уборка в ВУЗе, если и проводится, то явно <b>не идеально</b>, — <b>мой руки</b> перед приёмом пищи, <b>не оставляй вещи на полу</b> ни в одной аудитории.

А если проблемы <b>уже начались</b>, вот что хотелось бы добавить:
<tg-emoji emoji-id='5219935417121394505'>1️⃣</tg-emoji> <b>Не скрывайся и не унывай.</b> Не выходишь из завала сам — лучше пожертвуй общением и гулянками — сходи <b>в деканат</b> или <b>к преподавателю</b>, или <b>к куратору</b>, честно объясни ситуацию. Легко можно <b>получить индивидуальный график пересдач</b> — ВУЗу невыгодно тебя терять.
<tg-emoji emoji-id='5199658498559854923'>2️⃣</tg-emoji> Если ситуация <b>системная</b> (<i>болезнь, семейные обстоятельства</i>) — не забывай об <b>академическом отпуске</b>, это нормальный рабочий инструмент, а не позор.
<tg-emoji emoji-id='5197545864276495943'>3️⃣</tg-emoji> <b>Разочаровался в специальности?</b> Не бросай молча — сначала разберись: возможно, проблема в <b>конкретных предметах первого семестра</b>, а не в профессии.
""",

    # Адаптация и страхи первокурсников
    "faq_survive": """<tg-emoji emoji-id='5386535377467094223'>🍞</tg-emoji> <b>Я тут вообще выживу?</b>

Почти наверняка — <b>да</b>. По <b>лонгитюдным данным НИУ ВШЭ</b> можно отметить, что происходит со студентами на самом деле:
<tg-emoji emoji-id='5251596872350454252'>1️⃣</tg-emoji> <b>Тишина в общих каналах, растерянность, ощущение «я один такой тупой»</b> — исследователи называют это типичными сигналами риска.
<tg-emoji emoji-id='5233730869256016719'>2️⃣</tg-emoji> <b>Классические страхи первокурсника</b> — буквально один и тот же набор у <b>миллионов людей</b> каждый год. Они подробно разобраны в <a href='https://norma-media.ru/lifestyle/adaptacziya-pervokursnikov-8-strahov-i-sovety-kak-spravitsya'>студенческих гайдах</a>.
<tg-emoji emoji-id='5226858719718953055'>3️⃣</tg-emoji> <b>«Я ожидал одно, а получил совсем другое»</b> — ожидания от ВУЗа почти никогда <b><u>не</u> совпадают</b> с реальностью, и данный разрыв переживают практически все. <b>Главная трудность первокурсников</b> — самоорганизация без внешнего контроля, а вовсе не интеллект.
<tg-emoji emoji-id='5246949837995267651'>4️⃣</tg-emoji> <b>Тоска по дому и одиночество</b> — в британских исследованиях причин ухода студентов именно это оказалось <b>сильнейшим фактором</b>, сильнее проблем с самим курсом. Это переживание, а не приговор.

Почему кажется, что <b>«я не выживу»</b>, хотя выживешь:
<tg-emoji emoji-id='5471979757501439582'>1️⃣</tg-emoji> <b>«Все остальные всё поняли, один я нет».</b> Это не так. У каждого <b>свой темп адаптации</b>, и многие просто не показывают, что им тоже тяжело — сравнивай себя <b>с собой на прошлой неделе</b>, не с соседом по парте.
<tg-emoji emoji-id='5373066076558996568'>2️⃣</tg-emoji> <b>«У меня уже хвост/двойка/пропуск — всё, конец».</b> Нет: отчисляют не за единичную ошибку, а за <b>систематическое молчание</b> при накоплении долгов. Один завал — есть <b>пересдача</b>, несколько — <b>индивидуальный график</b>. А ВУЗу терять тебя невыгодно — крайняя мера применяется неохотно.

Если хочешь получить практические советы, рекомендуем изучить вопрос «<tg-emoji emoji-id='5447544503143504937'>😫</tg-emoji> <b>Как не отчислиться?</b>», он также присутствует в списке <b>часто задаваемых вопросов</b>!
""",

    # Балльно-рейтинговая система
    "faq_brs": """<tg-emoji emoji-id='5341498088408234504'>💯</tg-emoji> <b>Что такое БРС?</b>

<blockquote><b>БРС</b> — балльно–рейтинговая система — способ оценивания, при котором ты не «<b>сдаёшь экзамен и всё</b>», а <b>набираешь баллы</b> за всё, что делаешь в течение семестра, а из накопленных баллов складывается итоговая оценка.</blockquote>
<b>Если кратко:</b> у дисциплины есть <b>максимальное количество баллов</b>, которое можно набрать (<i>у всех дисциплин оно разное</i>), и есть разные типы работ в семестре: <i>ответы на семинарах</i>, <i>лабораторные</i>, <i>контрольные работы</i>, <i>посещаемость</i> — за них начисляется <b>определённая часть баллов</b>. А ещё — за сам <b>экзамен</b> или <b>зачёт</b>.

Для отслеживания своих результатов, как правило, нужно обращаться в раздел «<b>Обучение</b>» в <a href='https://lk.ulstu.ru/'>ЛМС УлГТУ</a>: результаты могут быть представлены в <b>виде PDF–документа</b> или <b>электронной таблицы</b>. В противном случае информацию придётся уточнять <b>у преподавателя</b> интересующей вас дисциплины!

<tg-emoji emoji-id='5210956306952758910'>👀</tg-emoji> <i>На скриншоте выше вы можете увидеть, как <b>выглядят списки</b> и <b>как с ними нужно работать</b>...</i>"
""",

    # Перевод на другое направление
    "faq_transfer": """<tg-emoji emoji-id='5323772371830588991'>🫡</tg-emoji> <b>Смена направления</b>

<i>Пока не готово, так как нужно поинтересоваться у деканата...</i>
""",

    # Студенческий сленг
    "faq_slang": """<tg-emoji emoji-id='5305720405242159172'>🔑</tg-emoji> <b>Сленг для учёбы</b>

Данный раздел больше подойдёт <b>иностранцам</b> или <b>студентам</b>, которые только-только знакомятся с условиями обучения в ВУЗе...

<tg-emoji emoji-id='5325547803936572038'>✨</tg-emoji> <b>Студенческие «штучки»</b>
<tg-emoji emoji-id='5427222599094517391'>‼️</tg-emoji> <b>Пара (<i>class</i>)</b> — учебное занятие, обычно два академических часа подряд
<tg-emoji emoji-id='5427153093638766320'>‼️</tg-emoji> <b>Препод (<i>professor</i>)</b> — преподаватель
<tg-emoji emoji-id='5429152284950934930'>‼️</tg-emoji> <b>Универ, шарага (<i>uni, ironic “my humble institution”</i>)</b> — университет
<tg-emoji emoji-id='5192775886482459664'>‼️</tg-emoji> <b>Первак (<i>freshman</i>)</b> — первокурсник
<tg-emoji emoji-id='5422469414622608277'>‼️</tg-emoji> <b>Общага (<i>dorm</i>)</b> — общежитие
<tg-emoji emoji-id='5195283073641499085'>‼️</tg-emoji> <b>Стипуха (<i>stipend, allowance</i>)</b> — стипендия
<tg-emoji emoji-id='5415772126089070331'>‼️</tg-emoji> <b>Окно (<i>gap between classes</i>)</b> — свободный промежуток между парами
<tg-emoji emoji-id='5222201759694341178'>‼️</tg-emoji> <b>Хвост (<i>backlog, unpassed credit</i>)</b> — несданный зачёт, экзамен, работа
<tg-emoji emoji-id='5427071605224258696'>‼️</tg-emoji> <b>Автомат (<i>automatic pass</i>)</b> — оценка без сдачи экзамена — за работу в семестре
<tg-emoji emoji-id='5420478611381567211'>‼️</tg-emoji> <b>Сессия, мясорубка (<i>exam period</i>)</b> — период экзаменов–отсевов
<tg-emoji emoji-id='5195445170002214719'>‼️</tg-emoji> <b>Зачётка (<i>gradebook</i>)</b> — зачётная книжка
<tg-emoji emoji-id='5422453695042306513'>‼️</tg-emoji> <b>Студак (<i>student ID</i>)</b> — студенческий билет
<tg-emoji emoji-id='5193022357475705620'>‼️</tg-emoji> <b>Бегунок (<i>clearance sheet</i>)</b> — обходной лист
<tg-emoji emoji-id='5193022400425379085'>‼️</tg-emoji> <b>Лаба (<i>lab assignment</i>)</b> — лабораторная работа
<tg-emoji emoji-id='5202073893677840013'>‼️</tg-emoji> <b>Курсач (<i>term paper</i>)</b> — курсовая работа
<tg-emoji emoji-id='5222199457591870060'>‼️</tg-emoji> <b>Контроша (<i>test, quiz</i>)</b> — контрольная работа
<tg-emoji emoji-id='5316565051635678936'>‼️</tg-emoji> <b>Вышка, матан (<i>calculus</i>)</b> — высшая математика, математический анализ
<tg-emoji emoji-id='5416020662961584769'>‼️</tg-emoji> <b>Шпоры (<i>cheat notes</i>)</b> — шпаргалки
<tg-emoji emoji-id='5415956234157178054'>‼️</tg-emoji> <b>Скатать (<i>to copy off someone</i>)</b> — списать
<tg-emoji emoji-id='5417958797018675206'>‼️</tg-emoji> <b>Забить на пару (<i>to skip class</i>)</b> — прогулять занятие
<tg-emoji emoji-id='5418385626573584301'>‼️</tg-emoji> <b>Завалить (<i>to fail</i>)</b> — не сдать экзамен, контрольную
<tg-emoji emoji-id='5415707512601066913'>‼️</tg-emoji> <b>Ботан, заучка (<i>nerd, grind</i>)</b> — тот, кто учит всё подряд
<tg-emoji emoji-id='5271687312021933370'>‼️</tg-emoji> <b>Зубрить, задротить (<i>to cram</i>)</b> — учить механически, без понимания
<tg-emoji emoji-id='5426860580596103334'>‼️</tg-emoji> <b>Халява (<i>freebie</i>)</b> — что-то, доставшееся без особых усилий
<tg-emoji emoji-id='5271664668954350948'>‼️</tg-emoji> <b>Апнуть (<i>to level up</i>)</b> — повысить уровень
<tg-emoji emoji-id='5269269507427289187'>‼️</tg-emoji> <b>Гриндить (<i>to grind</i>)</b> — долго и нудно делать однотипные задания ради результата
<tg-emoji emoji-id='5269338961343432611'>‼️</tg-emoji> <b>Тильт (<i>tilt, tilt mode</i>)</b> — состояние, когда всё валится из рук из-за неудач
<tg-emoji emoji-id='5274267122782982624'>‼️</tg-emoji> <b>Вайб (<i>vibe</i>)</b> — атмосфера, настроение
<tg-emoji emoji-id='5422535853471709738'>‼️</tg-emoji> <b>Чилл (<i>to chill</i>)</b> — расслабленное состояние, отдых
<tg-emoji emoji-id='5273804541920299303'>‼️</tg-emoji> <b>Жиза (<i>relatable</i>)</b> — жизненная, узнаваемая ситуация
""",
    
    # Программистский сленг
    "faq_prog_slang": """<tg-emoji emoji-id='5231018528689108942'>🖥</tg-emoji> <b>Сленг для программистов</b>

<tg-emoji emoji-id='5276017910366610357'>‼️</tg-emoji> <b>Баг, фиксить, дебажить (<i>bug, fix, debug</i>)</b> — ошибка в программе, исправлять и искать её
<tg-emoji emoji-id='5276245341769836476'>‼️</tg-emoji> <b>Фича (<i>feature</i>)</b> — функция продукта
<tg-emoji emoji-id='5274194048209398109'>‼️</tg-emoji> <b>Таск (<i>task</i>)</b> — задача в трекере
<tg-emoji emoji-id='5274260822065948801'>‼️</tg-emoji> <b>Дедлайн (<i>deadline</i>)</b> — срок сдачи
<tg-emoji emoji-id='5275985324449736372'>‼️</tg-emoji> <b>Релиз, хотфикс (<i>release, hotfix</i>)</b> — выпуск версии, срочное исправление критического бага
<tg-emoji emoji-id='5274182881294429839'>‼️</tg-emoji> <b>Кранч (<i>crunch</i>)</b> — аврал, большой объём работы в сжатые сроки
<tg-emoji emoji-id='5276104617166383228'>‼️</tg-emoji> <b>Техдолг (<i>technical debt</i>)</b> — последствия быстрых временных решений, которые потом усложняют жизнь
<tg-emoji emoji-id='5274249418927778366'>‼️</tg-emoji> <b>Легаси (<i>legacy code</i>)</b> — старый код, который никто не понимает, но все боятся трогать
<tg-emoji emoji-id='5273831677523666619'>‼️</tg-emoji> <b>Коммит, репа, ПР (<i>commit, repo, PR</i>)</b> — зафиксировать изменения, хранилище кода, пулл−реквест на проверку
<tg-emoji emoji-id='5276225391646746856'>‼️</tg-emoji> <b>Деплой, задеплоить (<i>deploy</i>)</b> — выложить новую версию на сервер
<tg-emoji emoji-id='5276362508477670577'>‼️</tg-emoji> <b>Продакшн (<i>prod, production</i>)</b> — рабочая среда, то, что видят реальные пользователи
<tg-emoji emoji-id='5274095401400543889'>‼️</tg-emoji> <b>Бэкап (<i>backup</i>)</b> — резервная копия
<tg-emoji emoji-id='5275997792739796367'>‼️</tg-emoji> <b>Джун, мидл, сеньор (<i>junior, middle, senior</i>)</b> — уровни опыта
<tg-emoji emoji-id='5275968333559113658'>‼️</tg-emoji> <b>Фронт, бэк, фулстек (<i>frontend, backend, fullstack</i>)</b> — видимая часть, серверная часть и универсал
<tg-emoji emoji-id='5273944557854140615'>‼️</tg-emoji> <b>Вайб−кодинг (<i>vibe coding</i>)</b> — быстрое программирование «по вайбу», часто с опорой на нейросети
<tg-emoji emoji-id='5276516203882359646'>‼️</tg-emoji> <b>Кланкер (<i>clanker</i>)</b> — уничижительное название для ИИ, робота или «бездушного» автоматизированного решения
<tg-emoji emoji-id='5274085806443604103'>‼️</tg-emoji> <b>Таскмаскинг (<i>taskmasking</i>)</b> — имитация бурной деятельности: человек выглядит занятым, но реально ничего полезного не делает
<tg-emoji emoji-id='5276129669710619845'>‼️</tg-emoji> <b>Аура−фарминг (<i>aura farming</i>)</b> — создание продуманного «естественно крутого» образа без явной демонстрации усилий
<tg-emoji emoji-id='5276271425106225527'>‼️</tg-emoji> <b>Эйджентик−инжиниринг (<i>agentic engineering</i>)</b> — управление ИИ−агентами, которые сами планируют и выполняют задачи; «взрослая» альтернатива вайб−кодингу
<tg-emoji emoji-id='5273862751612052806'>‼️</tg-emoji> <b>Слоп (<i>slop</i>)</b> — низкокачественный код или контент, сгенерированный ИИ без должной проверки
<tg-emoji emoji-id='5273923022888119233'>‼️</tg-emoji> <b>Галлюцинация (<i>hallucination</i>)</b> — уверенный, но неверный ответ нейросети
<tg-emoji emoji-id='5276244843553630595'>‼️</tg-emoji> <b>Промпт−инжиниринг (<i>prompt engineering</i>)</b> — составление запросов к нейросети так, чтобы получить нужный результат
""",

    # Академический отпуск
    "faq_academic": """<tg-emoji emoji-id='5265002646397285605'>🏫</tg-emoji> <b>Академический отпуск</b>

<i>Пока не готово, так как нужно поинтересоваться у деканата...</i>
""",

    # Как найти друзей
    "faq_friends": """<tg-emoji emoji-id='5443038326535759644'>💬</tg-emoji> <b>Как найти друзей?</b>

Психология банальна, но работает: людям становится близок тот, с кем они <b>часто пересекаются в одном месте и делают одно дело</b>. Поэтому формула такая: <b>постоянные точки пересечения</b> <tg-emoji emoji-id='5381819718124452001'>➡️</tg-emoji> <b>общее дело</b> <tg-emoji emoji-id='5381819718124452001'>➡️</tg-emoji> <b>время</b>. Не «стать душой компании за первую неделю», а стабильно появляться там, где те же люди. Отсюда рекомендуем ознакомиться с <i>общими чатами</i> <a href='https://yandex.ru/maps/-/CXWtmR94'>УлГТУ</a> на различные тематики и с прочими <i>социальными сетями</i>, где можно найти знакомства.

<tg-emoji emoji-id='5332724926216428039'>📇</tg-emoji> Базой может служить <b>беседа</b> твоего направления или других направлений, а также <b>каналы</b>, связанные с общественной деятельностью или прочими развлечениями. Ссылки на них можешь найти в разделе «<tg-emoji emoji-id='5447410659077661506'>🌐</tg-emoji> <b>Ресурсы</b>».

<tg-emoji emoji-id='5445044153572411510'>🍬</tg-emoji> Если желаешь более <b>«прямолинейный подход»</b>, вот тебе несколько вариантов:
<tg-emoji emoji-id='5192761820464589480'>💝</tg-emoji> <b><a href='https://t.me/leomatchbot'>Дайвинчик</a></b> — чат–бот для знакомств
<tg-emoji emoji-id='5192753492523004571'>💝</tg-emoji> <b><a href='https://t.me/bibinto_bot'>Бибинто</a></b> — чат–бот для оценивания внешности
<tg-emoji emoji-id='5192867974876278993'>💝</tg-emoji> <b><a href='https://dating.vk.ru'>ВК знакомства</a></b> — сервис для поиска друзей, романтических партнёров или единомышленников внутри экосистемы ВКонтакте
<tg-emoji emoji-id='5190832375126341100'>💝</tg-emoji> <b><a href='https://www.mamba.ru/ru'>Mamba</a></b> — крупная российская платформа для онлайн–знакомств и общения
<tg-emoji emoji-id='5190495924568240622'>💝</tg-emoji> <b><a href='https://twinby.ru'>Twinby</a></b> — российское мобильное приложение для онлайн–знакомств
""",

    # Где спокойно посидеть
    "faq_study_places": """<tg-emoji emoji-id='5395463497783983254'>☕️</tg-emoji> <b>Где спокойной посидеть?</b>

Под <b>«спокойно посидеть»</b> мы подразумеваем возможность устроиться там, где есть <i>свободная розетка</i> для зарядного устройства, и, располагая <b>зарядкой</b> и <b>доступным интернетом</b>, заниматься домашними заданиями или просто отдыхать.

<tg-emoji emoji-id='5445221832074483553'>💼</tg-emoji> По своему опыту можем подсказать несколько таких мест: <b>читальный зал</b>, <b>несколько кабинетов</b> на четвёртом этаже третьего корпуса, <b>столики</b> рядом с дверьми в третьем корпусе. Это, пожалуй, самые комфортные из всех мест. Подробнее о каждом можете увидеть на фотографии выше <tg-emoji emoji-id='5202126386768140453'>👀</tg-emoji>...
<blockquote>Конечно, чтобы с комфортом посидеть в условиях <i>белых списков</i> и при отсутствии <i>хорошего VPN</i>, стоит <b>подключиться к Wi–Fi</b>, который предоставляет ВУЗ. Для этого мы добавили соответствующий раздел «<tg-emoji emoji-id='5341715473882955310'>⚙️</tg-emoji> <b>Хочу Wi–Fi</b>».</blockquote>
""",

    "faq_wifi": "Не доделал...",
    "faq_ask_admin": "Не доделал...",
}


@router.callback_query(F.data == "menu_faq", F.message.chat.type == "private")
async def process_faq_menu(callback: types.CallbackQuery):
    await delete_previous_bot_message(callback.bot, callback.message.chat.id)

    sent_message = await callback.message.answer(
        text="<tg-emoji emoji-id='5436113877181941026'>❓</tg-emoji> <b>Часто задаваемые вопросы (<i>FAQ</i>)</b>\n\nВыбери <b>вопрос</b> или <b>категорию</b>, которые тебя интересуют, нажав на кнопку ниже...",
        reply_markup=get_faq_menu()
    )
    bot_state.last_messages[callback.message.chat.id] = sent_message.message_id
    await safe_answer(callback)


@router.callback_query(F.data.startswith("faq_"), F.message.chat.type == "private")
async def process_faq_item(callback: types.CallbackQuery):
    answer_text = FAQ_TEXTS[callback.data]

    await delete_previous_bot_message(callback.bot, callback.message.chat.id)

    if callback.data == "faq_survive":
        reply_markup = get_faq_survive_keyboard()
    elif callback.data == "faq_expelled":
        reply_markup = get_faq_expelled_keyboard()
    elif callback.data == "faq_slang":
        reply_markup = get_faq_slang_keyboard()
    elif callback.data == "faq_prog_slang":
        reply_markup = get_faq_prog_slang_keyboard()
    elif callback.data == "faq_friends":
        reply_markup = get_faq_friends_keyboard()
    elif callback.data == "faq_study_places":
        reply_markup = get_faq_study_places_keyboard()
    else:
        reply_markup = get_faq_back_button()

    if callback.data == "faq_brs":
        try:
            album = await callback.message.answer_media_group(
                media=[
                    types.InputMediaPhoto(
                        media=types.FSInputFile(config.IMG_FAQ_EXAMPLE)
                    ),
                    types.InputMediaPhoto(
                        media=types.FSInputFile(config.IMG_FAQ_LIST)
                    ),
                ]
            )

            text_message = await callback.message.answer(
                text=answer_text,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
            )

            bot_state.last_messages[callback.message.chat.id] = [
                *(item.message_id for item in album),
                text_message.message_id,
            ]
        except Exception as error:
            logging.exception("Ошибка при отправке фото БРС: %s", error)
            sent_message = await callback.message.answer(
                text=answer_text,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
            )
            bot_state.last_messages[callback.message.chat.id] = (
                sent_message.message_id
            )
    elif callback.data == "faq_study_places":
        try:
            # 1. Отправляем альбом из трех фото
            album = await callback.message.answer_media_group(
                media=[
                    types.InputMediaPhoto(
                        media=types.FSInputFile(config.IMG_FAQ_PLACES_1)
                    ),
                    types.InputMediaPhoto(
                        media=types.FSInputFile(config.IMG_FAQ_PLACES_2)
                    ),
                    types.InputMediaPhoto(
                        media=types.FSInputFile(config.IMG_FAQ_PLACES_3)
                    ),
                ]
            )

            text_message = await callback.message.answer(
                text=answer_text,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
            )

            bot_state.last_messages[callback.message.chat.id] = [
                *(item.message_id for item in album),
                text_message.message_id,
            ]
            
        except Exception as error:
            logging.exception("Ошибка при отправке альбома мест: %s", error)
            sent_message = await callback.message.answer(
                text=answer_text,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
            )
            bot_state.last_messages[callback.message.chat.id] = sent_message.message_id
    else:
        sent_message = await callback.message.answer(
            text=answer_text,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )
        bot_state.last_messages[callback.message.chat.id] = (
            sent_message.message_id
        )

    await safe_answer(callback)