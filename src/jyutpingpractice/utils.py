import curses
import random

from playsound import playsound
from importlib_resources import files, as_file
from pathlib import Path

AUDIO_FILEPATH = files('jyutpingpractice.assets.syllables')
AUDIO_SUFFIX = '.mp3'

def get_user_choice(stdscr, cursor_row: int, cursor_col: int, num_chars: int, choice_type: callable):
    curses.echo()
    user_input = stdscr.getstr(cursor_row, cursor_col, num_chars).decode('utf-8')
    curses.noecho()

    try:
        choice = choice_type(user_input)
        return choice
    except ValueError:
        return None

def get_matching_audio(syllable: str) -> list[str]:
    with as_file(AUDIO_FILEPATH) as dir:
        # TODO: return more accurate matches as some patterns are subsets of others
        matching_files = dir.glob(f'*{syllable}*{AUDIO_SUFFIX}')
        return [ path.stem for path in matching_files ]

def get_random_audio(n: int) -> list[str]:
    with as_file(AUDIO_FILEPATH) as dir:
        matching_files = list(dir.glob(f'*{AUDIO_SUFFIX}'))
        return [ path.stem for path in random.choices(matching_files, k=n) ]

def play_audio(syllable: str):
    playsound(str(AUDIO_FILEPATH.joinpath(f'{syllable}{AUDIO_SUFFIX}')))