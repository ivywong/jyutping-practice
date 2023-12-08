import curses
import sys
from enum import Enum

OPTIONS = ['Tutor Mode', 'Initials Quiz', 'Finals Quiz', 'Vowels Quiz', 'Custom Quiz', 'Quit']
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

def get_menu_choice(stdscr):
    curses.echo()
    user_input = stdscr.getstr(CURSOR_ROW, len(MENU_PROMPT), 1).decode('utf-8')
    curses.noecho()

    try:
        choice = int(user_input)
        return choice
    except ValueError:
        return None

def handle_choice(stdscr, user_choice: int):
    if OPTIONS[user_choice - 1] == 'Quit':
        sys.exit(0)

def validate_menu_choice(choice: int):
    return choice is not None and 1 <= choice <= len(OPTIONS)

def main(stdscr):
    stdscr.clear()

    while True:
        print_menu(stdscr)
        user_choice = get_menu_choice(stdscr)

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
