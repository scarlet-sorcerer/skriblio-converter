#!/usr/bin/env python
import os
import re
import curses
from typing import TextIO

INPUT_FILENAME = 'castbars.txt'
OUTPUT_FILENAME = 'output.txt'

stdscr = curses.initscr()


def parse_file(filename: str) -> list[str]:
    raw_data = []
    try:
        with open(filename, 'r') as f:
            raw_data = parse_lines(f)
    except FileNotFoundError:
        raise
    return raw_data


def parse_lines(file: TextIO) -> list[str]:
    raw_data = []
    while line := file.readline():
        if line.isspace():
            continue
        raw_data.append(line.rstrip())

    return raw_data


def parse_content(raw_data: list[str]) -> dict[str, list[str]]:
    processed_data = {}
    current_key = ''

    for line in raw_data:
        if line.startswith('--'):
            current_key = line[2:]
            processed_data[current_key] = []
            continue
        processed_data[current_key].append(line)

    return processed_data


def filter_data(processed_data: dict[str, list[str]], selected_categories: str | list[str]) -> dict[str, list[str]]:
    filtered_data = {}
    for key in processed_data.keys():
        if key not in selected_categories and selected_categories != 'ALL':
            continue    
        filtered_data[key] = processed_data[key]

    return filtered_data


def join_categories(filtered_data: dict[str, list[str]]) -> str:
    joined_categories = ''
    separator = ', '
    num_categories = len(filtered_data)
    processed_count = 0

    for category in filtered_data.keys():
        joined_categories += separator.join(filtered_data[category])
        processed_count += 1
        if processed_count < num_categories:
            joined_categories += ', '

    return joined_categories


def generate_categories(processed_data: [str, list[str]]) -> list[str]:
    categories = []
    for key in processed_data.keys():
        categories.append(key)

    return categories

def parse_user_input(categories: list[str], category_states: list[int]) -> list[str]:
    selected_categories = []
    
    for i in range(len(categories)):
        if category_states[i] == 1:
            selected_categories.append(categories[i])

    return selected_categories

    
def curses_run(stdscr) -> None:
    attributes = {}
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    attributes['normal'] = curses.color_pair(1)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    attributes['highlighted'] = curses.color_pair(2)

    stdscr.clear()


    try:
        raw_data = parse_file(INPUT_FILENAME)
    except FileNotFoundError:
        raise

    processed_data = parse_content(raw_data)
    
    categories = generate_categories(processed_data)
    category_states = [0] * len(categories)
    
    # Let user select categories
    c = 0  # last character read
    option = 0  # the current option that is marked
    while True:
        stdscr.erase()
        stdscr.addstr("Select categories to include:\n", curses.A_UNDERLINE)
        
        for i in range(len(categories)):
            if i == option:
                attr = attributes['highlighted']
            else:
                attr = attributes['normal']
            stdscr.addstr(f'[{"✓" if category_states[i] == 1 else "×"}] ')
            stdscr.addstr(categories[i] + '\n', attr)
        
        stdscr.addstr('Press y to finalize your selection, a to enable all, or q to quit')
        
        c = stdscr.getch()
        if c == 113: # q
            return
        if c == 121: # y
            finalized = True
            break
        if c == 97: # a
            finalized = False 
            selected_categories = 'ALL'
            break
        
        if c == curses.KEY_UP and option > 0:
            option -= 1
        elif c == curses.KEY_DOWN and option < len(categories) - 1:
            option += 1
        elif c == 10:
            category_states[option] = (int(category_states[option]) + 1) % 2

    stdscr.erase()

    if finalized:
        selected_categories = parse_user_input(categories, category_states)
    
    filtered_data = filter_data(processed_data, selected_categories)
    final_product = join_categories(filtered_data)
    
    
    with open(OUTPUT_FILENAME, 'w') as f:
        f.write(final_product)

    stdscr.addstr(f'Selected categories: {selected_categories}\n')
    stdscr.addstr('Press any key to exit...')
    stdscr.getch()

def run():
    try:
        curses.wrapper(curses_run)
    except FileNotFoundError:
        print('Input file not found!')
        print('Ensure the input file "castbars.txt" is in the working directory before running the script!')
        input('Press any key to exit...')
        raise SystemExit


if __name__ == '__main__':
    #all_categories = 'ALL'
    #endwalker = ['Asphodelos', 'Abyssos', 'Anabaseios']
    #synthesize_final_product('test.txt', endwalker)
    run()
