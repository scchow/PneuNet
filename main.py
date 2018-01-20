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

def start():
    """
    Starts the program. This means reading the file,
        parsing the intervals, and executing the timeline.
    """

    if len(sys.argv) != 2:
        filename = input("Path to gait file: ")
    else:
        filename = sys.argv[1]

    verbose = input("Verbose mode? (y/N): ").strip().lower()
    verbose = (verbose == "y" or verbose == "yes")

    timeline = read_timeline(filename, verbose)

    if not timeline:
        print("Timeline is empty. Exiting")
        exit()

    print_timeline(timeline)

    try:
        cycle_time = get_input("Seconds per cycle: ")
        cycle_count = int(get_input("Number of cycles (-1 for indefinite): "))
    except ValueError:
        exit()

    input("\nPress enter to run {} cycles at {} seconds each...".format(cycle_count, cycle_time))

    cycle = 0
    while cycle != cycle_count:
        print("\nCycle {}:".format(cycle + 1))
        do_cycle(timeline, cycle_time)
        cycle += 1

def get_input(message):
    """
    Reads input from the user repeatedly until numerical input is provided.
        :param message: is the prompt to show the user.
    """
    while True:
        try:
            return float(input(message))
        except ValueError:
            continue

start()
