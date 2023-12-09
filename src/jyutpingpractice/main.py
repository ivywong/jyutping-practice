import curses
import sys

from .quiz import quiz_mode, QuizType
from .utils import get_user_choice

OPTIONS = ['Tones Quiz', 'Initials Quiz', 'Finals Quiz', 'Overall Quiz', 'Quit']
MENU_PROMPT =  "Enter the number of your choice: "
CURSOR_ROW = len(OPTIONS) + 3

def print_menu(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Jyutping Drills", curses.A_UNDERLINE)

    for i, mode in enumerate(OPTIONS):
        stdscr.addstr(2 + i, 0, f"{i+1}. {mode}")
    
    stdscr.addstr(CURSOR_ROW, 0, MENU_PROMPT)
    stdscr.move(CURSOR_ROW, len(MENU_PROMPT))
    stdscr.refresh()

def validate_menu_choice(choice: int):
    return choice is not None and 1 <= choice <= len(OPTIONS)

def handle_choice(stdscr, user_choice: int):
    choice_text = OPTIONS[user_choice - 1]
    if choice_text == 'Quit':
        sys.exit(0)
    elif choice_text == 'Tones Quiz':
        quiz_mode(stdscr=stdscr, type=QuizType.TONE)
    elif choice_text == 'Initials Quiz':
        quiz_mode(stdscr=stdscr, type=QuizType.INITIAL)
    elif choice_text == 'Finals Quiz':
        quiz_mode(stdscr=stdscr, type=QuizType.FINAL)
    elif choice_text == 'Overall Quiz':
        quiz_mode(stdscr=stdscr, type=QuizType.ALL)

def main(stdscr):
    stdscr.clear()

    while True:
        print_menu(stdscr)
        user_choice = get_user_choice(stdscr, cursor_row=CURSOR_ROW, cursor_col=len(MENU_PROMPT), num_chars=1, choice_type=int)

        if validate_menu_choice(user_choice):
            stdscr.clear()
            stdscr.addstr(0, 0, f"Selected Option: {user_choice}")
            stdscr.refresh()

            handle_choice(stdscr, user_choice)

            stdscr.addstr(2, 0, "Press any key to return to the menu.")
            stdscr.refresh()
            stdscr.getch()
        else:
            stdscr.addstr(CURSOR_ROW + 1, 0, "Invalid choice. Please enter a valid number.")
            stdscr.refresh()
            stdscr.getch()

curses.wrapper(main)
