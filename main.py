#!/usr/bin/python3
"""
    Author: Gabriel Kulp
    Created: 1/19/2017

    This module is the entry point. It's the only one that
    executes code on its own.
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

    # Extract command line arguments
    filename, timeline, cycle_time, multiplier = handle_argv()
    # Note that this is where the program sits while the visualizer is running

    # if handle_argv() can't find some info, it's set to none.
    # This block asks for any input not specified in argv.
    if not timeline:
        print("File not specified.")
    while not timeline:
        timeline, filename = choose_timeline(verbose=False)

    if not cycle_time:
        print("Cycle time not specified.")
        cycle_time = choose_cycle_time()

    if not multiplier:
        print("Multiplier not specified.")
        multiplier = choose_multiplier()

    # Python doesn't have a do-while, so execute before entering the menu loop.
    execute_gaits(filename, timeline, cycle_time, multiplier)

    while True:
        print("\n\nWhat next?\n")
        print(" 1\tRun again with the same settings ({})".format(filename))
        print(" 2\tChange the amplitude multiplier then run ({})".format(multiplier))
        print(" 3\tChange the cycle speed then run ({})".format(cycle_time))
        print(" 4\tOpen a new file")
        print(" 5\tSwitch to editor/visualizer mode for this file")
        print(" 6\tQuit\n")

        # Python also doesn't have switch statements. Oh well.
        menu = input("(1-6) ").strip()
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
            timeline, filename = choose_timeline(verbose=False)
            continue
        elif menu == '5':
            filename, timeline = start_visualizer(filename)
            continue
        elif menu == '6':
            exit()
        else:
            print("Invalid option. Try again.")
            continue

def handle_argv():
    """
    Parses command-line input stored in sys.argv
    """

    # the first element of argv is the program name, so 1 argument means length of 2
    if len(sys.argv) >= 2:
        # check for editor switch
        if sys.argv[1] == "-e":
            # only the filename can come after the -e
            if len(sys.argv) > 3:
                print("Invalid editor/visualizer syntax. Use -e [filename]\n")
                input("Press enter to ignore...")
            # start_visualizer asks for a file if none is specified, so send None if invalid
            filename, timeline = start_visualizer(sys.argv[2] if len(sys.argv) >= 3 else None)
            # return None to set cycle_time and multiplier
            return filename, timeline, None, None

    # initialize to None so that if not set, they're declared
    filename, timeline, cycle_time, multiplier = None, None, None, None
    bad_input = False
    try:
        # only accept (filename) or (filename with both values). no need to
        # accept only cycle_time or multiplier
        if len(sys.argv) == 2 or len(sys.argv) == 4:
            filename = sys.argv[1]
            timeline, filename = choose_timeline(filename)
            # choose_timeline() can return none if the chosen file exists but is bad
            if not timeline:
                bad_input = True
                # don't bother parsing the numbers if the timeline file is bad
            elif len(sys.argv) == 4:
                cycle_time = float(sys.argv[2])
                multiplier = float(sys.argv[3])
                if cycle_time < 0:
                    bad_input = True
        # if the user didn't spcify 0, 1, or 3 arguments...
        elif len(sys.argv) != 1:
            bad_input = True
    except ValueError:
        # catches issues with parsing floats
        bad_input = True

    if bad_input:
        print("Argument error. Format is [filename] [cycle_time multiplier]")
        print("or, for editor/visualizer mode, -e [filename]\n")
        return None, None, None, None
    return filename, timeline, cycle_time, multiplier

def start_visualizer(filename=None):
    """
    Kicks off the editor/visualizer. Returns the file you where
    editing/viewing when the user presses Ctrl+C
        :param filename: is an optional parameter. When specified,
            this file is viewed. When not, the user will be prompted.
    """
    print("Choose a file to edit/visualize:")
    while True:
        timeline, filename = choose_timeline(filename, verbose=True)

        if not timeline:
            print("file not found: {}".format(add_quotes(filename)))
            continue

        print("Finished reading file: {}\n".format(add_quotes(filename)))
        print("Press enter to reload, type r to switch to run mode,")
        usr = input("type o to view a different file, or type q to quit: ").strip().lower()

        if usr == 'r':
            break
        elif usr == 'o':
            filename = None
        elif usr == 'q':
            print("\nexiting...")
            exit()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')

    print("\n")
    return filename, timeline

def choose_timeline(filename=None, folder="gaits", verbose=None):
    """
    Returns a timeline from a file.
        :param filename: is an optional argument. When specified,
            this is the file used. When not, the user is prompted.
        :param folder: is an optional argument. When specified, this
            folder is searched for gait and txt files.
        :param verbose: is an optional argument. When not None,
            the user will not be asked about verbosity and this
            value will be used.
    """
    # if the function was passed filename = None...
    if not filename:
        filename = choose_file(folder)

    # if the function was not passed verbosity, ask the user
    if verbose is None:
        verbose = input("Show extra parsing info? (y/N): ").strip().lower()
        verbose = (verbose == "y" or verbose == "yes")

    timeline, errors = read_timeline(filename, verbose)

    if errors:
        print("finished parsing with errors")
    if verbose and not errors:
        print("finished parsing with no errors")

    if not timeline:
        if verbose is None:
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

def choose_file(folder):
    """
    Returns a valid filename. If more than one is available in the folder,
    it will ask the user. If no files are available, returns None.
        :param folder: is the folder to look in. Must be at the same
            directory level as this script file. No need for ./ at the start.
    """
    # make a list of all the files the user chooses from
    files = []
    for file in os.listdir(folder):
        if file.endswith((".txt", ".gait")):
            files.append(file)

    print("\nPlease select a file from the {} folder:".format(folder))

    # print file selection list
    for num, file in enumerate(files):
        print(" {}\t{}".format(num + 1, file))

    print(" {}\t[Manually specify]\n".format(len(files) + 1))

    # get user input
    choice = 0
    while choice > len(files) + 1 or choice < 1:
        try:
            choice = int(input("which file? (1-{}): ".format(len(files) + 1)))
        except ValueError:
            pass

    # if they chose to manually specify, get and check input
    if choice == len(files) + 1:
        valid = False
        while not valid:
            file = input("File path: ")
            valid = os.path.isfile(file)
            if not valid:
                print("{} does not exist".format(file))
        return file


    return "{}/{}".format(folder, files[choice - 1])

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
    input("%. Press enter to start, then Ctrl-C to stop.")
    start_time = time.time()

    # allows catching Ctrl-C without exiting program
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

    # connection is closed when not running
    board.disconnect()

def get_positive_float(message):
    """
    Reads input from the user repeatedly until valid input is provided.
        :param message: is the prompt to show the user.
    """
    while True:
        try:
            value = float(input(message))
        # catches parsing errors
        except ValueError:
            continue
        if value >= 0:
            return value

# the actual entry point!
try:
    start()
# prints a message when quitting. not strictly necessary...
except KeyboardInterrupt:
    print("\nForce quit")
