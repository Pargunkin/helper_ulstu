"""Тексты FAQ, собранные из тематических модулей."""

from data.faq.academic import ACADEMIC_TEXTS
from data.faq.slang import SLANG_TEXTS
from data.faq.student_life import STUDENT_LIFE_TEXTS
from data.faq.wifi import WIFI_TEXTS

FAQ_TEXTS: dict[str, str] = {
    **ACADEMIC_TEXTS,
    **SLANG_TEXTS,
    **STUDENT_LIFE_TEXTS,
    **WIFI_TEXTS,
}
