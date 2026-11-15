import asyncio
import colorsys
import sys
import shutil

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
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

def hard_clear():
    sys.stdout.write("\033[H")
    term_width = shutil.get_terminal_size().columns
    blank_line = " " * term_width + "\n"
    for _ in range(20):
        sys.stdout.write(blank_line)
    sys.stdout.write("\033[H")
    sys.stdout.flush()

def get_rainbow_color(offset):
    hue = offset % 1.0
    r, g, b = colorsys.hls_to_rgb(hue, 0.5, 1.0)
    return f"\033[38;2;{int(r*255)};{int(g*255)};{int(b*255)}m"

async def play_intro():
    hard_clear()
    logo_lines = [
        "██╗   ██╗██╗     ███████╗████████╗██╗   ██╗",
        "██║   ██║██║     ██╔════╝╚══██╔══╝██║   ██║",
        "██║   ██║██║     ███████╗   ██║   ██║   ██║",
        "██║   ██║██║     ╚════██║   ██║   ██║   ██║",
        "╚██████╔╝███████╗███████║   ██║   ╚██████╔╝",
        " ╚═════╝ ╚══════╝╚══════╝   ╚═╝    ╚═════╝ "
    ]
    term_width = shutil.get_terminal_size().columns
    logo_width = len(logo_lines[0])
    padding = " " * max(0, (term_width - logo_width) // 2)
    sys.stdout.write("\033[?25l")

    for frame in range(40):
        sys.stdout.write("\033[H")
        for i, line in enumerate(logo_lines):
            color = get_rainbow_color((frame * 0.05) + (i * 0.1))
            sys.stdout.write(f"{padding}{color}{Colors.BOLD}{line}{Colors.RESET}\n")
        sys.stdout.flush()
        await asyncio.sleep(0.06)

    await asyncio.sleep(0.5)
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()
    hard_clear()

def print_banner():
    banner = f"""
{Colors.L_RED}{Colors.BOLD}██╗   ██╗██╗     ███████╗████████╗██╗   ██╗{Colors.RESET}
{Colors.L_YELLOW}{Colors.BOLD}██║   ██║██║     ██╔════╝╚══██╔══╝██║   ██║{Colors.RESET}
{Colors.L_GREEN}{Colors.BOLD}██║   ██║██║     ███████╗   ██║   ██║   ██║{Colors.RESET}
{Colors.L_CYAN}{Colors.BOLD}██║   ██║██║     ╚════██║   ██║   ██║   ██║{Colors.RESET}
{Colors.L_BLUE}{Colors.BOLD}╚██████╔╝███████╗███████║   ██║   ╚██████╔╝{Colors.RESET}
{Colors.L_MAGENTA}{Colors.BOLD} ╚═════╝ ╚══════╝╚══════╝   ╚═╝    ╚═════╝ {Colors.RESET}

{Colors.YELLOW}{Colors.BOLD}>>> {Colors.REVERSE}🚀 Бот «Студпомощник» успешно запущен!{Colors.RESET}

{Colors.GREEN}✅ Соединение с Telegram API установлено{Colors.RESET}
{Colors.CYAN}ℹ  Версия: 0.3.3 (бета–тест){Colors.RESET}
{Colors.CYAN}ℹ  Ожидание сообщений...{Colors.RESET}

{Colors.RED}⚠  Для остановки работы нажмите {Colors.BOLD}Ctrl+C{Colors.RESET}

════════════════════════════════════════════════════
"""
    print(banner)