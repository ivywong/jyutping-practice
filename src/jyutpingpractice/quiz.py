from enum import Enum
import curses
import random
from time import sleep

from .utils import get_user_choice, play_audio, get_matching_audio, get_random_audio

class QuizType(Enum):
    TONE = ['1', '2', '3', '4', '5', '6']
    INITIAL = ['b','p','m','f',
               'd','t','n','l',
               'g','k','ng','h',
               'gw','kw','w',
               'z','c','s','j']
    FINAL = [
        'aa', 'aai', 'aau', 'aam', 'aan', 'aang', 'aap', 'aat', 'aak',
        'a', 'ai', 'au', 'am', 'an', 'ang', 'ap', 'at', 'ak',
        'e', 'ei', 'eu', 'em', 'eng', 'ep', 'ek',
        'i', 'iu', 'im', 'in', 'ing', 'ip', 'it', 'ik',
        'o', 'oi', 'ou', 'on', 'ong', 'ot', 'ok',
        'u', 'ui', 'un', 'ung', 'ut', 'uk',
        'eoi', 'eon', 'eot',
        'oe', 'oeng', 'oet', 'oek',
        'yu', 'yun', 'yut',
        'm', 'ng']
    ALL = []

SUPPORTED_TYPES = [QuizType.TONE, QuizType.INITIAL]
REPLAY_AUDIO_KEY = 'R'

def pick_syllables(quiz_type: QuizType, n: int) -> tuple[list, list]:
    if quiz_type == QuizType.ALL:
        sounds = get_random_audio(n)
        return sounds, sounds

    answers = random.choices(quiz_type.value, k=n)

    if quiz_type == QuizType.TONE:
        syllables = [ f"maa{ans}" for ans in answers ]
    elif quiz_type == QuizType.INITIAL:
        syllables = [ f"{ans}aa1" for ans in answers ]
    elif quiz_type == QuizType.FINAL:
        syllables = []
        for i, _ in enumerate(answers):
            # TODO: make this more efficient
            while len(valid_syllables := get_matching_audio(answers[i])) == 0:
                answers[i] = random.choice(quiz_type.value)
            syllables.append(random.choice(valid_syllables))

    return answers, syllables

def quiz_mode(stdscr, type: QuizType):
    quiz_title = type.name.title()
    answer_type = type.name.lower()
    
    stdscr.clear()
    stdscr.addstr(0, 0, f"{quiz_title} Quiz", curses.A_UNDERLINE)

    stdscr.addstr(2, 0, f"For this quiz, please listen to the audio and input what {answer_type} you believe is playing.")
    stdscr.addstr(4, 0, "Press any key to start.")
    stdscr.refresh()
    stdscr.getch()

    num_questions = 5
    curr_question = 1

    answers, syllables = pick_syllables(quiz_type=type, n=num_questions)
    num_correct = 0
    while (curr_question <= num_questions):
        stdscr.clear()
        stdscr.addstr(0, 0, f"{quiz_title} Quiz: [{curr_question}/{num_questions}]")

        answer = answers[curr_question - 1]
        syllable = syllables[curr_question - 1]
        
        play_audio(syllable)

        quiz_prompt = f"What {answer_type} is playing? Enter your answer, or type '{REPLAY_AUDIO_KEY}' to replay: "
        stdscr.addstr(2, 0, quiz_prompt)
        stdscr.move(2, len(quiz_prompt))
        user_input = get_user_choice(stdscr=stdscr, cursor_row=2, cursor_col=len(quiz_prompt), num_chars=5, choice_type=str)

        if user_input == REPLAY_AUDIO_KEY:
            pass
        elif user_input == answer:
            num_correct += 1
            stdscr.addstr(4, 0, "Correct! Press any key to continue.")
            stdscr.getch()
            curr_question += 1
        else:
            stdscr.addstr(4, 0, f"Wrong! The audio was {syllable}, and the correct answer was '{answer}'. Press any key to continue.")
            stdscr.getch()
            curr_question += 1
    
    stdscr.clear()
    stdscr.addstr(f"You got {num_correct} out of {num_questions} right!")
    stdscr.refresh()
