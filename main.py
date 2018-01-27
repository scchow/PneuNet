#!/usr/bin/python3
"""
    Author: Gabriel Kulp
    Created: 1/19/2017

    This module is the entry point. It's the only one that
    executes code on its own or interacts with the user directly.
"""
import sys
from core import do_cycle
from visualization import print_timeline
from parse import read_timeline
from output import Arduino

def start():
    """
    Starts the program. This means reading the file,
        parsing the intervals, and executing the timeline.
    """

    if len(sys.argv) != 2:
        timeline = choose_timeline()
    else:
        timeline = choose_timeline(sys.argv[1])

    cycle_time = get_positive_float("Seconds per cycle: ")
    multiplier = get_positive_float("Amplitude multiplier: ")

    execute_gaits(timeline, cycle_time, multiplier)

    while True:
        print("\n\nWhat next?\n")
        print("1\tChoose a new file")
        print("2\tChange the amplitude multiplier")
        print("3\tChange the cycle speed\n")
        
        menu = input("(1,2,3) ").strip()
        if menu == '1':
            timeline = choose_timeline()
            cycle_time = get_positive_float("Seconds per cycle: ")
            multiplier = get_positive_float("Amplitude multiplier: ")
            execute_gaits(timeline, cycle_time, multiplier)
            continue
        elif menu == '2':
            print("Previous:", multiplier)
            multiplier = get_positive_float("Amplitude multiplier: ")
            execute_gaits(timeline, cycle_time, multiplier)
            continue
        elif menu == '3':
            print("Previous:", cycle_time)
            cycle_time = get_positive_float("Seconds per cycle: ")
            execute_gaits(timeline, cycle_time, multiplier)
            continue
        else:
            print("Invalid option. Try again.")
            continue


def choose_timeline(filename=None):
    """
    This function returns a timeline from a file.
        :param filename: is an optional argument. When specified,
            this is the file used. When not, the user is prompted.
    """
    if not filename:
        filename = input("Path to gait file: ")
    else:
        filename = sys.argv[1]

    verbose = input("Verbose parsing? (y/N): ").strip().lower()
    verbose = (verbose == "y" or verbose == "yes")

    timeline = read_timeline(filename, verbose)

    if not timeline:
        print("Timeline is empty. There is nothing to do.")
        return None

    print_timeline(timeline)

    return timeline

def execute_gaits(timeline, cycle_time, multiplier):
    """
    Runs through the gait until stopped by user.
        :param filename: is the timeline to execute.
        :param cycle_time: is how long each cycle takes.
        :param multiplier: is what to multipy amplitudes by.
    """
    board = Arduino()
    print("Attempting to connect...")
    if board.connect():
        print("Connected!")
    else:
        print("Error connecting!")
        exit()

    input("\nPress enter to start...")

    try:
        cycle = 0
        while True:
            print("\nCycle #{} at {}%".format(cycle + 1, int(multiplier * 100)))
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
