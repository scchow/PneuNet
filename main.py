#!/usr/bin/python3
"""
    Author: Gabriel Kulp
    Created: 1/19/2017

    This module is the entry point. It's the only one that
    executes code on its own or interacts with the user directly.
"""
import os
import sys
import time
from core import do_cycle
from visualization import print_timeline, add_quotes
from parse import read_timeline
from output import Arduino

def start():
    """
    Starts the program. This means reading the file,
        parsing the intervals, and executing the timeline.
    """

    filename, timeline, cycle_time, multiplier = handle_argv()

    while not timeline:
        timeline, filename = choose_timeline()

    if not cycle_time:
        cycle_time = choose_cycle_time()

    if not multiplier:
        multiplier = choose_multiplier()

    execute_gaits(filename, timeline, cycle_time, multiplier)

    while True:
        print("\n\nWhat next?\n")
        print(" 1\tRun again with the same settings")
        print(" 2\tChange the amplitude multiplier")
        print(" 3\tChange the cycle speed")
        print(" 4\tOpen a new file")
        print(" 5\tQuit\n")

        menu = input("(1-5) ").strip()
        if menu == '1':
            execute_gaits(filename, timeline, cycle_time, multiplier)
            continue
        elif menu == '2':
            print("Previous:", multiplier)
            multiplier = choose_multiplier()
            execute_gaits(filename, timeline, cycle_time, multiplier)
            continue
        elif menu == '3':
            print("Previous:", cycle_time)
            cycle_time = choose_cycle_time()
            execute_gaits(filename, timeline, cycle_time, multiplier)
            continue
        elif menu == '4':
            timeline, filename = choose_timeline()
            if not timeline:
                continue
            cycle_time = choose_cycle_time()
            multiplier = choose_multiplier()
            execute_gaits(filename, timeline, cycle_time, multiplier)
            continue
        elif menu == '5':
            exit()
        else:
            print("Invalid option. Try again.")
            continue

def handle_argv():
    """
    Parses command-line input stored in sys.argv
    """

    filename, timeline, cycle_time, multiplier = None, None, None, None
    bad_input = False
    try:
        if len(sys.argv) == 2 or len(sys.argv) == 4:
            filename = sys.argv[1]
            timeline, filename = choose_timeline(filename)
            if not timeline:
                bad_input = True
            elif len(sys.argv) == 4:
                cycle_time = float(sys.argv[2])
                multiplier = float(sys.argv[3])
                if cycle_time < 0:
                    bad_input = True
        elif len(sys.argv) != 1:
            bad_input = True
    except ValueError:
        bad_input = True

    if bad_input:
        print("Argument error. Format is [filename] [cycle time] [multiplier]")
        return None, None, None, None
    else:
        return filename, timeline, cycle_time, multiplier

def choose_timeline(filename=None):
    """
    Returns a timeline from a file.
        :param filename: is an optional argument. When specified,
            this is the file used. When not, the user is prompted.
    """

    if not filename:
        filename = choose_file()
        if not filename:
            print("No valid gait files in current directory.")
            print("Make sure they have the .txt or .gait extension.")
            exit()

    verbose = input("Show extra parsing info? (y/N): ").strip().lower()
    verbose = (verbose == "y" or verbose == "yes")

    timeline = read_timeline(filename, verbose)

    if not timeline:
        print("Timeline is empty. There is nothing to do.")
        return None, None

    print_timeline(timeline)

    return timeline, filename

def choose_cycle_time():
    """
    Returns a valid cycle time from the user.
    """
    return get_positive_float("Seconds per cycle: ")

def choose_multiplier():
    """
    Returns a valid amplitude multiplier from the user.
    """
    return get_positive_float("Amplitude multiplier: ")

def choose_file():
    """
    Returns a valid filename. If more than one is available in the folder,
    it will ask the user. If no files are available, returns None.
    """
    files = []
    for file in os.listdir("."):
        if file.endswith((".txt", ".gait")):
            files.append(file)

    if not files:
        return None

    if len(files) == 1:
        return files[0]

    print("\nMultiple files are available:")

    for num, file in enumerate(files):
        print(" {}\t{}".format(num + 1, file))

    print()
    choice = 0
    while choice > len(files) or choice < 1:
        try:
            choice = int(input("which file? (1-{}): ".format(len(files))))
        except ValueError:
            pass

    return files[choice - 1]

def execute_gaits(filename, timeline, cycle_time, multiplier):
    """
    Runs through the gait until stopped by user.
        :param filename: is the path to display to display.
        :param timeline: is the gait to follow
        :param cycle_time: is how long each cycle takes.
        :param multiplier: is what to multipy amplitudes by.
    """
    board = Arduino()
    print("Attempting to connect...")
    if board.connect():
        print("Connected!")
    else:
        print("Error connecting!")
        return

    print("\nReading from", add_quotes(filename))
    print("Cycle time is", cycle_time, end='')
    print(", multiplier is", int(multiplier * 100), end='')
    input("%. Press enter to start...")
    start_time = time.time()

    try:
        cycle = 0
        while True:
            print("\nCycle #{} at time {}s".format(cycle + 1, time.time() - start_time))
            do_cycle(board, timeline, cycle_time, multiplier)
            cycle += 1
    except KeyboardInterrupt:
        print("\nStopping playback...", end='')
        board.clear()
        print("done.\n")

    board.disconnect()

def get_positive_float(message):
    """
    Reads input from the user repeatedly until valid input is provided.
        :param message: is the prompt to show the user.
    """
    while True:
        try:
            value = float(input(message))
        except ValueError:
            continue
        if value >= 0:
            return value

start()
