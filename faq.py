import logging

from aiogram import F, Router, types

import config
import state as bot_state
from keyboards import (
    get_faq_back_button,
    get_faq_expelled_keyboard,
    get_faq_menu,
    get_faq_survive_keyboard,
)
from utils import delete_previous_bot_message, safe_answer

router = Router()

FAQ_TEXTS = {
    "faq_expelled": (
"""
<tg-emoji emoji-id='5447544503143504937'>😫</tg-emoji> <b>Как не отчислиться?</b>

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
"""
    ),
    "faq_survive": (
"""
<tg-emoji emoji-id='5386535377467094223'>🍞</tg-emoji> <b>Я тут вообще выживу?</b>

Почти наверняка — <b>да</b>. По <b>лонгитюдным данным НИУ ВШЭ</b> можно отметить, что происходит со студентами на самом деле:
<tg-emoji emoji-id='5251596872350454252'>1️⃣</tg-emoji> <b>Тишина в общих каналах, растерянность, ощущение «я один такой тупой»</b> — исследователи называют это типичными сигналами риска.
<tg-emoji emoji-id='5233730869256016719'>2️⃣</tg-emoji> <b>Классические страхи первокурсника</b> — буквально один и тот же набор у <b>миллионов людей</b> каждый год. Они подробно разобраны в <a href='https://norma-media.ru/lifestyle/adaptacziya-pervokursnikov-8-strahov-i-sovety-kak-spravitsya'>студенческих гайдах</a>.
<tg-emoji emoji-id='5226858719718953055'>3️⃣</tg-emoji> <b>«Я ожидал одно, а получил совсем другое»</b> — ожидания от ВУЗа почти никогда <b><u>не</u> совпадают</b> с реальностью, и данный разрыв переживают практически все. <b>Главная трудность первокурсников</b> — самоорганизация без внешнего контроля, а вовсе не интеллект.
<tg-emoji emoji-id='5246949837995267651'>4️⃣</tg-emoji> <b>Тоска по дому и одиночество</b> — в британских исследованиях причин ухода студентов именно это оказалось <b>сильнейшим фактором</b>, сильнее проблем с самим курсом. Это переживание, а не приговор.

Почему кажется, что <b>«я не выживу»</b>, хотя выживешь:
<tg-emoji emoji-id='5471979757501439582'>1️⃣</tg-emoji> <b>«Все остальные всё поняли, один я нет».</b> Это не так. У каждого <b>свой темп адаптации</b>, и многие просто не показывают, что им тоже тяжело — сравнивай себя <b>с собой на прошлой неделе</b>, не с соседом по парте.
<tg-emoji emoji-id='5373066076558996568'>2️⃣</tg-emoji> <b>«У меня уже хвост/двойка/пропуск — всё, конец».</b> Нет: отчисляют не за единичную ошибку, а за <b>систематическое молчание</b> при накоплении долгов. Один завал — есть <b>пересдача</b>, несколько — <b>индивидуальный график</b>. А ВУЗу терять тебя невыгодно — крайняя мера применяется неохотно.

Если хочешь получить практические советы, рекомендуем изучить вопрос «<tg-emoji emoji-id='5447544503143504937'>😫</tg-emoji> <b>Как не отчислиться?</b>», он также присутствует в списке <b>часто задаваемых вопросов</b>!
"""
    ),
    "faq_brs": (
"""
<tg-emoji emoji-id='5341498088408234504'>💯</tg-emoji> <b>Что такое БРС?</b>
<blockquote><b>БРС</b> — балльно–рейтинговая система — способ оценивания, при котором ты не «<b>сдаёшь экзамен и всё</b>», а <b>набираешь баллы</b> за всё, что делаешь в течение семестра, а из накопленных баллов складывается итоговая оценка.</blockquote>
<b>Если кратко:</b> у дисциплины есть <b>максимальное количество баллов</b>, которое можно набрать (<i>у всех дисциплин оно разное</i>), и есть разные типы работ в семестре: <i>ответы на семинарах</i>, <i>лабораторные</i>, <i>контрольные работы</i>, <i>посещаемость</i> — за них начисляется <b>определённая часть баллов</b>. А ещё — за сам <b>экзамен</b> или <b>зачёт</b>.

Для отслеживания своих результатов, как правило, нужно обращаться в раздел «<b>Обучение</b>» в <a href='https://lk.ulstu.ru/'>ЛМС УлГТУ</a>: результаты могут быть представлены в <b>виде PDF–документа</b> или <b>электронной таблицы</b>. В противном случае информацию придётся уточнять <b>у преподавателя</b> интересующей вас дисциплины!

<tg-emoji emoji-id='5210956306952758910'>👀</tg-emoji> <i>На скриншоте выше вы можете увидеть, как <b>выглядят списки</b> и <b>как с ними нужно работать</b>...</i>"
"""
    ),
    "faq_transfer": "Не доделал...",
    "faq_slang": "Не доделал...",
    "faq_academic": "Не доделал...",
    "faq_friends": "Не доделал...",
    "faq_study_places": "Не доделал...",
    "faq_smile": "Не доделал...",
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