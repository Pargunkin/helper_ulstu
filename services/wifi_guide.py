"""Сборка сообщений пошаговой инструкции по Wi-Fi."""

from data.emoji import ICON_GUIDE
from data.faq.wifi_guide import (
    OS_ORDER,
    STEP_DONE,
    STEP_DONE_ID,
    STEP_NUMBERS,
    STEP_TODO,
    STEP_TODO_ID,
    WIFI_GUIDES,
    WIFI_OS,
)

def _step_emoji(emoji: str, emoji_id: str) -> str:
    return f"<tg-emoji emoji-id='{emoji_id}'>{emoji}</tg-emoji>"


def step_text(os_key: str, number: int) -> str:
    """Текст шага инструкции. number — с единицы."""
    steps = WIFI_GUIDES[os_key]
    total = len(steps)
    index = max(0, min(total - 1, number - 1))
    title, body = steps[index]

    done = _step_emoji(STEP_DONE, STEP_DONE_ID)
    todo = _step_emoji(STEP_TODO, STEP_TODO_ID)
    progress = done * (index + 1) + todo * (total - index - 1)
    os_info = WIFI_OS[os_key]
    number_emoji = "".join(
        _step_emoji(emoji, emoji_id)
        for emoji, emoji_id in STEP_NUMBERS.get(index + 1, [])
    )

    return (
        f"<blockquote>{_step_emoji(os_info['emoji'], os_info['emoji_id'])} "
        f"<b>{os_info['title']}</b>, шаг <b>{index + 1}</b> из <b>{total}</b>\n"
        f"{progress}</blockquote>\n\n"
        f"{number_emoji} <b>{title}</b>\n\n{body}"
    )


def guide_menu_text() -> str:
    lines = [
        f"<tg-emoji emoji-id='{ICON_GUIDE}'>🕯</tg-emoji> <b>Пошаговая инструкция</b>",
        "",
        "Выбери свою систему — проведу <i>по шагам</i>, без лишней воды:",
        "",
    ]
    for key in OS_ORDER:
        info = WIFI_OS[key]
        lines.append(
            f"{_step_emoji(info['emoji'], info['emoji_id'])} "
            f"<b>{info['title']}</b> — {info['hint']}"
        )
    lines.append("")
    lines.append(
        "<blockquote><tg-emoji emoji-id='5422439311196834318'>💡</tg-emoji> <b>Всего 7–10 шагов.</b> По инструкции можно перемещаться с помощью соответствующих кнопок внизу...</blockquote>"
    )
    return "\n".join(lines)
