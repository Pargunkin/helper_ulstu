import asyncio
import colorsys
import logging
import math
import os
import platform
import random
import re
import shutil
import sys
import time
import unicodedata
import zlib
from collections import deque
from datetime import datetime
from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version

_START_TIME = time.time()


class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    REVERSE = '\033[7m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'

    L_RED = '\033[91m'
    L_YELLOW = '\033[93m'
    L_GREEN = '\033[92m'
    L_CYAN = '\033[96m'
    L_BLUE = '\033[94m'
    L_MAGENTA = '\033[95m'


LOGO_LINES = [
    "██╗   ██╗██╗     ███████╗████████╗██╗   ██╗",
    "██║   ██║██║     ██╔════╝╚══██╔══╝██║   ██║",
    "██║   ██║██║     ███████╗   ██║   ██║   ██║",
    "██║   ██║██║     ╚════██║   ██║   ██║   ██║",
    "╚██████╔╝███████╗███████║   ██║   ╚██████╔╝",
    " ╚═════╝ ╚══════╝╚══════╝   ╚═╝    ╚═════╝ ",
]
LOGO_WIDTH = len(LOGO_LINES[0])

HUE_STEP_X = 0.011
HUE_STEP_Y = 0.045
WHITE = "\033[38;2;255;255;255m"
GRAY = "\033[38;2;200;200;215m"
DARK = "\033[38;2;70;70;85m"
RED_SPLIT = "\033[38;2;255;45;85m"
CYAN_SPLIT = "\033[38;2;0;230;255m"
GLYPHS = "01░▒▓<>/\\|+*#$%&@"
SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
TAGLINE = "С Т У Д П О М О Щ Н И К"
STAGES = (
    "Загрузка конфигурации",
    "Подготовка базы данных",
    "Регистрация обработчиков",
    "Подключение к Telegram",
)


def enable_ansi() -> None:
    if os.name != "nt":
        return
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    except Exception:
        os.system("")


def hard_clear():
    sys.stdout.write("\033[2J\033[3J\033[H")
    sys.stdout.flush()


@lru_cache(maxsize=8192)
def _rgb_q(hue360: int, light50: int, sat100: int) -> str:
    r, g, b = colorsys.hls_to_rgb(hue360 / 360, light50 / 50, sat100 / 100)
    return f"\033[38;2;{int(r * 255)};{int(g * 255)};{int(b * 255)}m"


def rgb(hue: float, lightness: float = 0.55, saturation: float = 1.0) -> str:
    return _rgb_q(
        int(round((hue % 1.0) * 360)) % 360,
        max(0, min(50, int(round(lightness * 50)))),
        max(0, min(100, int(round(saturation * 100)))),
    )


def get_rainbow_color(offset):
    return rgb(offset)


def _ease_out(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def _render_logo(reveal: int, shift: float, sweep: float | None) -> list[str]:
    rows = []
    for i, line in enumerate(LOGO_LINES):
        parts = []
        for j, ch in enumerate(line):
            if ch == " " or j > reveal:
                parts.append(" ")
                continue
            lightness = 0.55
            if sweep is not None:
                distance = abs((j + i * 2) - sweep)
                if distance < 4:
                    lightness += (4 - distance) * 0.09
            color = rgb(j * HUE_STEP_X + i * HUE_STEP_Y - shift, lightness)
            parts.append(f"{color}{Colors.BOLD}{ch}")
        rows.append("".join(parts) + Colors.RESET)
    return rows


class _Scene:
    """Холст с клетками (символ, цвет); один кадр = одна строка вывода."""

    ROW_RULE_TOP = 1
    ROW_LOGO = 3
    ROW_TAGLINE = 10
    ROW_BAR = 12
    ROW_STATUS = 13
    ROW_RULE_BOTTOM = 14

    def __init__(self, term_width: int) -> None:
        self.margin = max(0, min(8, (term_width - 1 - LOGO_WIDTH) // 2))
        self.width = LOGO_WIDTH + self.margin * 2
        self.height = 16
        self.padding = " " * max(0, (term_width - self.width) // 2)

        self.cells = [
            (i, j, ch)
            for i, line in enumerate(LOGO_LINES)
            for j, ch in enumerate(line)
            if ch != " "
        ]
        self.mask = {(i, j) for i, j, _ in self.cells}
        self.halo = {
            (i + di, j + dj)
            for i, j in self.mask
            for di in (-1, 0, 1)
            for dj in (-1, 0, 1)
        } - self.mask

        self.locks = {
            (i, j): j / LOGO_WIDTH * 0.6 + random.uniform(0.0, 0.3)
            for i, j in self.mask
        }
        self.rain = [
            (
                random.uniform(0.5, 1.3),
                random.uniform(0, self.height + 9),
                random.randint(5, 9),
                random.uniform(0.55, 1.0),
            )
            for _ in range(self.width)
        ]

    def blank(self) -> list[list]:
        return [[None] * self.width for _ in range(self.height)]

    def put(self, grid, row: int, col: int, ch: str, color: str) -> None:
        if 0 <= row < self.height and 0 <= col < self.width:
            grid[row][col] = (ch, color)

    def put_text(self, grid, row: int, col: int, text: str, color) -> None:
        for index, ch in enumerate(text):
            if ch != " ":
                self.put(grid, row, col + index, ch, color(index) if callable(color) else color)

    def logo_color(self, i: int, j: int, shift: float, lightness: float = 0.55) -> str:
        return rgb(j * HUE_STEP_X + i * HUE_STEP_Y - shift, lightness) + Colors.BOLD

    def draw_rules(self, grid, progress: float, shift: float) -> None:
        length = int(LOGO_WIDTH * _ease_out(progress))
        start = self.margin + (LOGO_WIDTH - length) // 2
        for row in (self.ROW_RULE_TOP, self.ROW_RULE_BOTTOM):
            for k in range(length):
                self.put(grid, row, start + k, "═", rgb(k * HUE_STEP_X - shift, 0.5))

    def draw_logo(self, grid, shift: float, sweep: float | None = None, lightness: float = 0.55) -> None:
        for i, j, ch in self.cells:
            light = lightness
            if sweep is not None:
                distance = abs((j + i * 2) - sweep)
                if distance < 4:
                    light += (4 - distance) * 0.09
            self.put(grid, self.ROW_LOGO + i, self.margin + j, ch, self.logo_color(i, j, shift, light))

    def draw_halo(self, grid, shift: float, pulse: float) -> None:
        lightness = 0.14 + 0.14 * pulse
        for i, j in self.halo:
            color = rgb(j * HUE_STEP_X + i * HUE_STEP_Y - shift, lightness)
            self.put(grid, self.ROW_LOGO + i, self.margin + j, "░", color)

    def draw_tagline(self, grid, fraction: float, shift: float) -> None:
        shown = int(len(TAGLINE) * max(0.0, min(1.0, fraction)))
        col = self.margin + (LOGO_WIDTH - len(TAGLINE)) // 2
        text = TAGLINE[:shown]
        self.put_text(
            grid, self.ROW_TAGLINE, col, text,
            lambda k: rgb(k * 0.025 - shift, 0.68) + Colors.BOLD,
        )

    def draw_progress(self, grid, progress: float, shift: float, frame: int, done: bool) -> None:
        filled = int(LOGO_WIDTH * progress)
        for j in range(LOGO_WIDTH):
            if j < filled:
                self.put(grid, self.ROW_BAR, self.margin + j, "━", rgb(j * HUE_STEP_X - shift, 0.55))
            else:
                self.put(grid, self.ROW_BAR, self.margin + j, "─", DARK)

        percent = f"{int(progress * 100):3d}%"
        self.put_text(grid, self.ROW_STATUS, self.margin + LOGO_WIDTH - len(percent), percent, WHITE + Colors.BOLD)
        if done:
            self.put_text(grid, self.ROW_STATUS, self.margin, "✅  Готово", "\033[38;2;80;255;140m" + Colors.BOLD)
        else:
            stage = STAGES[min(len(STAGES) - 1, int(progress * len(STAGES)))]
            spin = SPINNER[frame % len(SPINNER)]
            self.put(grid, self.ROW_STATUS, self.margin, spin, rgb(frame * 0.04, 0.6) + Colors.BOLD)
            self.put_text(grid, self.ROW_STATUS, self.margin + 2, stage + "...", GRAY)

    def emit(self, grid) -> str:
        lines = []
        for row in grid:
            last = None
            buf = []
            for cell in row:
                if cell is None:
                    if last is not None:
                        buf.append(Colors.RESET)
                        last = None
                    buf.append(" ")
                else:
                    ch, color = cell
                    if color != last:
                        buf.append(color)
                        last = color
                    buf.append(ch)
            if last is not None:
                buf.append(Colors.RESET)
            lines.append(self.padding + "".join(buf))
        return "\033[H" + "\n".join(lines) + "\n"


def _frames(scene: _Scene):
    """Генератор кадров: (текст_кадра, пауза)."""
    # Акт 1: цифровой дождь «расшифровывается» в логотип
    total = 42
    for f in range(total + 1):
        t = f / total
        grid = scene.blank()

        for col, (speed, offset, trail, life) in enumerate(scene.rain):
            if t > life:
                continue
            head = (offset + speed * f) % (scene.height + trail)
            for row in range(scene.height):
                d = head - row
                if 0 <= d < trail:
                    if d < 1:
                        color = rgb(0.45, 0.85)
                    else:
                        color = rgb(0.38, 0.12 + 0.35 * (1 - d / trail))
                    scene.put(grid, row, col, random.choice(GLYPHS), color)

        for i, j, ch in scene.cells:
            lock = scene.locks[(i, j)]
            row, col = scene.ROW_LOGO + i, scene.margin + j
            if t >= lock:
                age = (t - lock) * total
                if age < 2:
                    scene.put(grid, row, col, ch, WHITE + Colors.BOLD)
                else:
                    boost = max(0.0, 0.3 - age * 0.04)
                    scene.put(grid, row, col, ch, scene.logo_color(i, j, 0.0, 0.55 + boost))
            elif random.random() < 0.8:
                scene.put(grid, row, col, random.choice(GLYPHS), rgb(0.4, random.uniform(0.2, 0.45)))

        scene.draw_rules(grid, t, 0.0)
        yield scene.emit(grid), 0.038

    # Акт 2: глитч с RGB-расслоением
    glitch_frames = 9
    for g in range(glitch_frames):
        grid = scene.blank()
        offsets = {}
        if g < glitch_frames - 2:
            for i in random.sample(range(len(LOGO_LINES)), random.randint(1, 3)):
                offsets[i] = random.choice((-3, -2, -1, 1, 2, 3))

        for i, j, ch in scene.cells:
            col = scene.margin + j + offsets.get(i, 0)
            row = scene.ROW_LOGO + i
            if g < glitch_frames - 2:
                scene.put(grid, row, col - 1, ch, RED_SPLIT)
                scene.put(grid, row, col + 1, ch, CYAN_SPLIT)
        for i, j, ch in scene.cells:
            col = scene.margin + j + offsets.get(i, 0)
            scene.put(grid, scene.ROW_LOGO + i, col, ch, scene.logo_color(i, j, 0.0))

        scene.draw_rules(grid, 1.0, 0.0)
        scene.draw_tagline(grid, g / glitch_frames * 0.3, 0.0)
        yield scene.emit(grid), 0.045

    # Акт 3: неоновое свечение, блик и загрузка
    total = 50
    sweep_span = LOGO_WIDTH + 20
    for f in range(total + 1):
        t = f / total
        shift = f * 0.02
        pulse = 0.5 + 0.5 * math.sin(f * 0.3)
        sweep = -10 + (t * 1.8 % 1.0) * sweep_span
        progress = _ease_out(t)

        grid = scene.blank()
        scene.draw_halo(grid, shift, pulse)
        scene.draw_rules(grid, 1.0, shift)
        scene.draw_logo(grid, shift, sweep)
        scene.draw_tagline(grid, 0.3 + t * 2.0, shift)
        scene.draw_progress(grid, progress, shift, f, done=False)
        yield scene.emit(grid), 0.035

    grid = scene.blank()
    scene.draw_rules(grid, 1.0, 0.0)
    scene.draw_logo(grid, 0.0)
    scene.draw_tagline(grid, 1.0, 0.0)
    scene.draw_progress(grid, 1.0, 0.0, 0, done=True)
    yield scene.emit(grid), 0.45


async def play_intro():
    enable_ansi()
    scene = _Scene(shutil.get_terminal_size().columns)

    hard_clear()
    sys.stdout.write("\033[?25l")

    try:
        for frame, delay in _frames(scene):
            sys.stdout.write(frame)
            sys.stdout.flush()
            await asyncio.sleep(delay)
    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        hard_clear()


def _static_logo() -> str:
    return "\n".join(_render_logo(LOGO_WIDTH, 0.0, None))


PANEL_WIDTH = LOGO_WIDTH + 7
BOT_VERSION = "0.7.2 (бета–тест)"
STATUS_BAR_ENABLED = True

LABEL_COLOR = "\033[38;2;130;140;170m"
VALUE_COLOR = "\033[38;2;235;235;245m"
OK_COLOR = "\033[38;2;80;255;140m"
WARN_COLOR = "\033[38;2;255;215;80m"
BAD_COLOR = "\033[38;2;255;90;100m"
BAR_BG = "\033[48;2;22;22;36m"
BAR_RESET = Colors.RESET + BAR_BG
ANSI_RE = re.compile(r"\033\[[0-9;?]*[A-Za-z]")
UPDATE_RE = re.compile(
    r"Update id=(\d+) is (not )?handled\. Duration (\d+) ms by bot id=\d+"
)


def _write(text: str) -> None:
    sys.stdout.write(text)
    sys.stdout.flush()


def _display_width(text: str) -> int:
    plain = ANSI_RE.sub("", text)
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in plain)


def _speed_color(milliseconds: float) -> str:
    if milliseconds < 100:
        return OK_COLOR
    if milliseconds < 500:
        return WARN_COLOR
    return BAD_COLOR


def _gradient_rule(width: int, char: str = "═", shift: float = 0.0) -> str:
    parts = [f"{rgb(j * HUE_STEP_X - shift)}{char}" for j in range(width)]
    return "".join(parts) + Colors.RESET


def _section(title: str, width: int = PANEL_WIDTH) -> str:
    """Градиентная линия с названием по центру."""
    label = f" {title} "
    start = max(0, (width - len(label)) // 2)
    parts = []
    for k in range(width):
        if start <= k < start + len(label):
            parts.append(f"{WHITE}{Colors.BOLD}{label[k - start]}")
        else:
            parts.append(f"{rgb(k * HUE_STEP_X)}━")
    return "".join(parts) + Colors.RESET


def _package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "?"


def _format_uptime(seconds: float) -> str:
    seconds = int(seconds)
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def _memory_mb() -> float | None:
    try:
        if os.name == "nt":
            import ctypes
            from ctypes import wintypes

            class ProcessMemoryCounters(ctypes.Structure):
                _fields_ = [
                    ("cb", wintypes.DWORD),
                    ("PageFaultCount", wintypes.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t),
                    ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t),
                    ("PeakPagefileUsage", ctypes.c_size_t),
                ]

            kernel32 = ctypes.windll.kernel32
            psapi = ctypes.windll.psapi
            kernel32.GetCurrentProcess.restype = wintypes.HANDLE
            psapi.GetProcessMemoryInfo.argtypes = [
                wintypes.HANDLE,
                ctypes.POINTER(ProcessMemoryCounters),
                wintypes.DWORD,
            ]
            counters = ProcessMemoryCounters()
            counters.cb = ctypes.sizeof(counters)
            if psapi.GetProcessMemoryInfo(
                kernel32.GetCurrentProcess(), ctypes.byref(counters), counters.cb
            ):
                return counters.WorkingSetSize / (1024 * 1024)
            return None

        import resource

        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    except Exception:
        return None


class _Stats:
    """Счётчики сессии, которые наполняются из логов aiogram."""

    def __init__(self) -> None:
        self.updates = 0
        self.unhandled = 0
        self.warnings = 0
        self.errors = 0
        self.total_ms = 0
        self.latencies: deque[int] = deque(maxlen=14)

    @property
    def average_ms(self) -> float | None:
        return self.total_ms / self.updates if self.updates else None

    def observe(self, record: logging.LogRecord) -> None:
        if record.levelno >= logging.ERROR:
            self.errors += 1
        elif record.levelno == logging.WARNING:
            self.warnings += 1

        if record.name == "aiogram.event":
            match = UPDATE_RE.search(record.getMessage())
            if match:
                duration = int(match.group(3))
                self.updates += 1
                self.total_ms += duration
                self.latencies.append(duration)
                if match.group(2):
                    self.unhandled += 1


STATS = _Stats()


class StatsFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        STATS.observe(record)
        return True


def _panel_rows(bot_info, extras) -> list[tuple[str, str | None, str | None]]:
    """Строки панели: (готовый_префикс, значение, цвет_значения)."""
    rows: list[tuple[str, str | None, str | None]] = [
        (f"{Colors.YELLOW}{Colors.BOLD}>>> {Colors.REVERSE}🚀 Бот «Студпомощник» успешно запущен!{Colors.RESET}", None, None),
        ("", None, None),
    ]

    info: list[tuple[str, str]] = []
    if bot_info is not None:
        username = getattr(bot_info, "username", None)
        info.append(("Бот", f"@{username}" if username else "—"))
        info.append(("Имя", getattr(bot_info, "full_name", "—")))
        info.append(("ID", str(getattr(bot_info, "id", "—"))))
    info.append(("Версия", BOT_VERSION))
    info.extend(extras or [])
    info.append(("Запущен", datetime.now().strftime("%d.%m.%Y  %H:%M:%S")))
    info.append((
        "Среда",
        f"Python {platform.python_version()} · aiogram {_package_version('aiogram')} · {platform.system()}",
    ))
    info.append(("Процесс", f"PID {os.getpid()} · режим polling"))

    for index, (label, value) in enumerate(info):
        bullet = f"{rgb(0.52 + index * 0.07, 0.62)}{Colors.BOLD}◆{Colors.RESET}"
        rows.append((f"{bullet} {LABEL_COLOR}{label:<9}{Colors.RESET}", value, VALUE_COLOR))

    rows.append(("", None, None))
    rows.append((f"{Colors.RED}⚠  Для остановки работы нажмите {Colors.BOLD}Ctrl+C{Colors.RESET}", None, None))
    return rows


def _rail(index: int) -> str:
    return f"{rgb(0.52 + index * 0.035, 0.6)}{Colors.BOLD}┃{Colors.RESET}"


def _edge_parts(corner: str, base_hue: float) -> list[str]:
    parts = [f"{rgb(base_hue, 0.6)}{Colors.BOLD}{corner}"]
    parts += [
        f"{rgb(base_hue + j * HUE_STEP_X, 0.6)}{Colors.BOLD}━"
        for j in range(PANEL_WIDTH - 1)
    ]
    return parts


def _row_text(index: int, prefix: str, value: str | None, color: str | None) -> str:
    text = f"{_rail(index)} {prefix}"
    if value is not None:
        text += f"{color}{value}{Colors.RESET}"
    return text


def print_banner(bot_info=None, extras=None) -> int:
    """Статичный вариант панели. Возвращает число напечатанных строк."""
    enable_ansi()
    rows = _panel_rows(bot_info, extras)

    lines = [""] + _static_logo().split("\n") + [""]
    lines.append("".join(_edge_parts("┏", 0.52)) + Colors.RESET)
    for index, (prefix, value, color) in enumerate(rows):
        lines.append(_row_text(index, prefix, value, color))
    lines.append("".join(_edge_parts("┗", 0.52 + len(rows) * 0.035)) + Colors.RESET)
    lines += ["", "", _section("ЖУРНАЛ СОБЫТИЙ"), ""]

    if bot_info is not None and getattr(bot_info, "username", None):
        sys.stdout.write(f"\033]0;ULSTU Helper · @{bot_info.username}\007")
    _write("\n".join(lines) + "\n")
    return len(lines)


async def play_banner(bot_info=None, extras=None) -> int:
    """Анимированная панель: логотип по строкам, рамка «рисуется», значения расшифровываются."""
    enable_ansi()
    rows = _panel_rows(bot_info, extras)

    if bot_info is not None and getattr(bot_info, "username", None):
        sys.stdout.write(f"\033]0;ULSTU Helper · @{bot_info.username}\007")

    _write("\n")
    for line in _static_logo().split("\n"):
        _write(line + "\n")
        await asyncio.sleep(0.04)
    _write("\n")

    async def draw_edge(corner: str, base_hue: float) -> None:
        parts = _edge_parts(corner, base_hue)
        for start in range(0, len(parts), 6):
            _write("".join(parts[start:start + 6]))
            await asyncio.sleep(0.012)
        _write(Colors.RESET + "\n")

    await draw_edge("┏", 0.52)

    steps = 4
    for index, (prefix, value, color) in enumerate(rows):
        rail = _rail(index)
        if value is None:
            _write(f"{rail} {prefix}\n")
            await asyncio.sleep(0.03)
            continue
        for step in range(steps):
            keep = int(len(value) * step / steps)
            noise = "".join(
                ch if ch == " " else random.choice(GLYPHS) for ch in value[keep:]
            )
            _write(f"\r{rail} {prefix}{color}{value[:keep]}{rgb(0.4, 0.45)}{noise}{Colors.RESET}")
            await asyncio.sleep(0.022)
        _write(f"\r{rail} {prefix}{color}{value}{Colors.RESET}\n")

    await draw_edge("┗", 0.52 + len(rows) * 0.035)
    _write("\n\n" + _section("ЖУРНАЛ СОБЫТИЙ") + "\n\n")
    return len(rows) + 14


def print_goodbye():
    enable_ansi()
    uptime = _format_uptime(time.time() - _START_TIME)
    average = f"{STATS.average_ms:.0f} ms" if STATS.average_ms is not None else "—"

    print()
    print(_section("ЗАВЕРШЕНИЕ РАБОТЫ"))
    print(f"{Colors.RED}🛑 Бот остановлен. До встречи!{Colors.RESET}")
    print()
    summary = [
        ("Время работы", uptime, VALUE_COLOR),
        ("Апдейтов", str(STATS.updates), VALUE_COLOR),
        ("Среднее время", average, _speed_color(STATS.average_ms or 0)),
        ("Предупреждений", str(STATS.warnings), WARN_COLOR if STATS.warnings else VALUE_COLOR),
        ("Ошибок", str(STATS.errors), BAD_COLOR if STATS.errors else OK_COLOR),
    ]
    for index, (label, value, color) in enumerate(summary):
        bullet = f"{rgb(0.52 + index * 0.07, 0.62)}{Colors.BOLD}◆{Colors.RESET}"
        print(f"{bullet} {LABEL_COLOR}{label:<15}{Colors.RESET}{color}{Colors.BOLD}{value}{Colors.RESET}")
    print(_gradient_rule(PANEL_WIDTH))
    print()


class StatusBar:
    """Живая панель внизу консоли: логи прокручиваются выше неё."""

    SPARK = "▁▂▃▄▅▆▇█"

    def __init__(self) -> None:
        self._task: asyncio.Task | None = None
        self._lines = 0
        self._cols = 0

    def start(self, printed_lines: int = 0) -> None:
        if not STATUS_BAR_ENABLED or self._task is not None:
            return
        enable_ansi()
        size = shutil.get_terminal_size()
        if size.lines < 12 or size.columns < 40:
            return

        self._lines, self._cols = size.lines, size.columns
        cursor_row = printed_lines + 2
        commands = [f"\033[1;{self._lines - 1}r"]
        if printed_lines <= 0 or cursor_row >= self._lines:
            commands.append(f"\033[{self._lines - 1};1H\n\n")
        else:
            commands.append(f"\033[{cursor_row};1H")
        _write("".join(commands))
        self._task = asyncio.get_running_loop().create_task(self._run())

    async def stop(self) -> None:
        if self._task is None:
            return
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        self._task = None
        _write(f"\0337\033[{self._lines};1H\033[2K\033[r\0338")

    async def _run(self) -> None:
        tick = 0
        while True:
            self._follow_resize()
            self._draw(tick)
            tick += 1
            await asyncio.sleep(0.5)

    def _follow_resize(self) -> None:
        size = shutil.get_terminal_size()
        if (size.lines, size.columns) == (self._lines, self._cols):
            return
        old_row = self._lines
        self._lines, self._cols = size.lines, size.columns
        _write(f"\0337\033[{old_row};1H\033[2K\033[1;{self._lines - 1}r\0338")

    @staticmethod
    def _console_columns() -> int | None:
        """Реальная ширина окна консоли Windows (shutil иногда отдаёт запасные 80)."""
        if os.name != "nt":
            return None
        try:
            import ctypes
            from ctypes import wintypes

            class _Info(ctypes.Structure):
                _fields_ = [
                    ("size_x", ctypes.c_short),
                    ("size_y", ctypes.c_short),
                    ("cursor_x", ctypes.c_short),
                    ("cursor_y", ctypes.c_short),
                    ("attributes", wintypes.WORD),
                    ("left", ctypes.c_short),
                    ("top", ctypes.c_short),
                    ("right", ctypes.c_short),
                    ("bottom", ctypes.c_short),
                    ("max_x", ctypes.c_short),
                    ("max_y", ctypes.c_short),
                ]

            kernel32 = ctypes.windll.kernel32
            kernel32.GetStdHandle.restype = wintypes.HANDLE
            info = _Info()
            handle = kernel32.GetStdHandle(-11)
            if kernel32.GetConsoleScreenBufferInfo(handle, ctypes.byref(info)):
                columns = info.right - info.left + 1
                return columns if columns > 0 else None
        except Exception:
            pass
        return None

    def _draw(self, tick: int) -> None:
        columns = shutil.get_terminal_size(fallback=(0, 0)).columns
        columns = max(columns, self._console_columns() or 0)
        if columns:
            bar = self._render(tick, columns - 1)
        else:
            # Консоль не сообщает ширину (shutil отдаёт запасные 80): считаем, что места
            # достаточно, а остаток строки закрашиваем сами.
            bar = self._render(tick, 140, stretch=True)
        _write(f"\0337\033[{self._lines};1H{bar}{Colors.RESET}\0338")

    @staticmethod
    def _segment(label: str, value: str, color: str = VALUE_COLOR) -> str:
        return f"{LABEL_COLOR}{label} {color}{Colors.BOLD}{value}{BAR_RESET}"

    def _sparkline(self, count: int = 14) -> str:
        values = list(STATS.latencies)[-count:] if count > 0 else []
        if not values:
            return ""
        chars = []
        for value in values:
            index = min(7, int(min(value, 400) / 400 * 7.999))
            chars.append(f"{_speed_color(value)}{self.SPARK[index]}")
        return " " + "".join(chars) + BAR_RESET

    def _render(self, tick: int, width: int, stretch: bool = False) -> str:
        dot = "\033[38;2;12;12;18m" if tick % 2 else WHITE
        pill = f"\033[48;2;60;220;130m\033[38;2;12;12;18m{Colors.BOLD} {dot}●\033[38;2;12;12;18m ONLINE {BAR_RESET}"

        average = STATS.average_ms
        average_text = f"{average:.0f}ms" if average is not None else "—"
        memory = _memory_mb()
        divider = f" {DARK}│{BAR_RESET} "

        avg_segment = self._segment(
            "AVG", average_text, _speed_color(average) if average is not None else VALUE_COLOR
        )
        min_bars = min(len(STATS.latencies), 3)
        avg_base = avg_segment + self._sparkline(min_bars)
        segments = [
            self._segment("UP", _format_uptime(time.time() - _START_TIME)),
            self._segment("UPD", str(STATS.updates)),
            avg_base,
            self._segment("WARN", str(STATS.warnings), WARN_COLOR if STATS.warnings else LABEL_COLOR),
            self._segment("ERR", str(STATS.errors), BAD_COLOR if STATS.errors else LABEL_COLOR),
        ]
        if memory is not None:
            segments.append(self._segment("RAM", f"{memory:.0f}MB"))

        version_short = BOT_VERSION.split(" ")[0]
        # Подпись справа уступает место счётчикам: сначала сокращается, потом убирается.
        right_variants = [
            f"{rgb(0.55, 0.7)}{Colors.BOLD}ULSTU Helper{BAR_RESET} "
            f"{LABEL_COLOR}v{version_short}{BAR_RESET}",
            f"{LABEL_COLOR}v{version_short}{BAR_RESET}",
            "",
        ]

        def fit(right_text: str) -> tuple[list[str], int]:
            taken: list[str] = []
            used = _display_width(pill)
            reserved = _display_width(right_text)
            for segment in segments:
                cost = _display_width(divider) + _display_width(segment)
                if used + cost + 1 + reserved > width:
                    break
                taken.append(segment)
                used += cost
            return taken, used

        right, (included, total) = max(
            ((variant, fit(variant)) for variant in right_variants),
            key=lambda item: (min(len(item[1][0]), 5), bool(item[0]), len(item[1][0])),
        )
        used_right = _display_width(right)

        # Минимум 3 столбика гарантированы; остальное место после сегментов идёт графику.
        if avg_base in included:
            spare = width - total - 1 - used_right
            count = min(len(STATS.latencies), 14, min_bars + max(0, spare))
            included[included.index(avg_base)] = avg_segment + self._sparkline(count)

        left = pill + "".join(divider + segment for segment in included)

        if _display_width(left) + 1 + used_right > width:
            right, used_right = "", 0

        if stretch:
            return f"{BAR_BG}{left}  {right}\033[K{Colors.RESET}"

        fill = max(0, width - _display_width(left) - used_right)
        return f"{BAR_BG}{left}{' ' * fill}{right}{Colors.RESET}"


def _bg_badge(text: str, background: tuple, foreground: tuple, width: int = 5) -> str:
    return (
        f"\033[48;2;{background[0]};{background[1]};{background[2]}m"
        f"\033[38;2;{foreground[0]};{foreground[1]};{foreground[2]}m"
        f"{Colors.BOLD} {text:<{width}} {Colors.RESET}"
    )


class ColorFormatter(logging.Formatter):
    """Цветной формат логов: полоса уровня, время, бейдж, источник › сообщение."""

    DARK_TEXT = (12, 12, 18)
    LIGHT_TEXT = (255, 255, 255)

    LEVELS = {
        logging.DEBUG: ("DEBUG", (110, 120, 145), LIGHT_TEXT, "\033[38;2;120;130;155m"),
        logging.INFO: ("INFO", (60, 220, 130), DARK_TEXT, "\033[38;2;225;228;240m"),
        logging.WARNING: ("WARN", (255, 200, 60), DARK_TEXT, "\033[38;2;255;215;100m"),
        logging.ERROR: ("ERROR", (255, 70, 90), LIGHT_TEXT, "\033[38;2;255;120;130m"),
        logging.CRITICAL: ("CRIT", (210, 30, 130), LIGHT_TEXT, "\033[38;2;255;90;170m"),
    }

    TAG_RE = re.compile(r"\[([A-ZА-Я ]{3,20})\]")
    QUOTE_RE = re.compile(r"'([^'\n]{1,80})'")
    MENTION_RE = re.compile(r"(?<!\w)@\w{3,}")
    PREFIX_WIDTH = 32

    def __init__(self) -> None:
        super().__init__(datefmt="%H:%M:%S")
        enable_ansi()

    @staticmethod
    def _source_tag(name: str) -> str:
        short = "bot" if name == "root" else name.rsplit(".", 1)[-1]
        short = short[:10]
        hue = (zlib.crc32(name.encode("utf-8")) % 360) / 360
        return f"{rgb(hue, 0.68, 0.85)}{short:<10}{Colors.RESET}"

    def _prettify(self, message: str, base: str) -> str:
        update = UPDATE_RE.search(message)
        if update:
            update_id, not_handled, duration = update.group(1), update.group(2), int(update.group(3))
            speed = _speed_color(duration)
            if not_handled:
                return (
                    f"\033[38;2;255;200;80m◌ Update #{update_id} не обработан{Colors.RESET}"
                    f" {LABEL_COLOR}·{Colors.RESET} {speed}{duration} ms{Colors.RESET}"
                )
            return (
                f"\033[38;2;110;200;255m⚡ Update #{update_id}{Colors.RESET}{base} обработан"
                f" {LABEL_COLOR}·{Colors.RESET} {speed}{Colors.BOLD}{duration} ms{Colors.RESET}"
            )

        message = self.TAG_RE.sub(
            lambda m: f"{_bg_badge(m.group(1), (150, 80, 255), (255, 255, 255), len(m.group(1)))}{base}",
            message,
        )
        message = self.QUOTE_RE.sub(
            lambda m: f"\033[38;2;110;220;255m{Colors.BOLD}{m.group(1)}{Colors.RESET}{base}",
            message,
        )
        message = self.MENTION_RE.sub(
            lambda m: f"\033[38;2;255;140;220m{Colors.BOLD}{m.group(0)}{Colors.RESET}{base}",
            message,
        )
        return f"{base}{message}{Colors.RESET}"

    def format(self, record: logging.LogRecord) -> str:
        label, background, foreground, base = self.LEVELS.get(
            record.levelno, self.LEVELS[logging.INFO]
        )
        stripe = f"\033[38;2;{background[0]};{background[1]};{background[2]}m▌{Colors.RESET}"
        stamp = f"{LABEL_COLOR}{self.formatTime(record, self.datefmt)}{Colors.RESET}"
        badge = _bg_badge(label, background, foreground)
        arrow = f"{rgb(0.55, 0.62)}{Colors.BOLD}›{Colors.RESET}"
        prefix = f"{stripe} {stamp} {badge} {self._source_tag(record.name)} {arrow} "

        indent = " " * self.PREFIX_WIDTH
        text = self._prettify(record.getMessage(), base).replace("\n", f"\n{indent}")
        result = prefix + text

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
            rail = f"\033[38;2;255;70;90m{Colors.BOLD}┃{Colors.RESET}"
            for line in record.exc_text.splitlines():
                result += f"\n{indent}{rail} \033[38;2;255;140;150m{line}{Colors.RESET}"

        return result
