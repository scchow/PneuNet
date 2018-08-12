#!/usr/bin/python3
"""
    Author: Gabriel Kulp
    Created: 1/19/2017

    This module handles parsing timelines from files.
"""

from pathlib import Path
from ansicolor import red, green, blue, yellow, black, magenta, white
# install package by typing: pip install ansicolor
from core import Interval
from visualization import interval_to_string, add_quotes

# reads timeline from file. Check README.md for more details.
def read_timeline(filename, verbose=False):
    """
    Reads a timeline of intervals from a text file. Returns the timeline and if there are errors.
        :param filename: is the path to the timeline file.
        :param verbose: is an optional flag.
            When true, extra parsing information is printed to the console. Defaults to false.
    """
    # make timeline array
    timeline = []

    count, total = 0, 0

    # Yes, this is the second part where this is checked. Gotta be sure.
    if not file_exists(filename):
        if verbose:
            print(add_quotes(filename), "is not a file")
        return False

    errors = False

    with open(filename) as lines:
        for num, line in enumerate(lines):
            line = line.strip()
            if verbose:
                print("reading line {} >".format(num + 1), add_quotes(line))

            if not line:
                if verbose:
                    print(black("Skipping blank line\n", bold=True))
                continue

            if line.startswith("#"):
                if verbose:
                    print(black("Skipping comment line\n", bold=True))
                continue

            comment_pos = line.find("#")
            if comment_pos != -1:
                if verbose:
                    print(black("\tRemoving comment > ", bold=True), end='')
                    print(add_quotes(line[comment_pos:]))
                    print(black("\tParsing remaining line > ", bold=True), end='')
                    print(add_quotes(line[:comment_pos]))
                line = line[:comment_pos]

            intvs = line.split(",")
            timeline.append([])

            for intv in intvs:

                comment_pos = intv.find("#")
                if comment_pos != -1:
                    if verbose:
                        print(black("\tFound comment in segment >", bold=True), add_quotes(intv))
                        print(black("\t\tRemoving comment > ", bold=True), end='')
                        print(add_quotes(intv[comment_pos:]))
                        print(black("\t\tRemaining segment > ", bold=True), end='')
                        print(add_quotes(intv[:comment_pos]))
                    intv = intv[:comment_pos]

                intv = intv.strip()

                if not parse_check_format(intv, verbose):
                    errors = True
                    continue

                params = intv.split()

                if not parse_check_numbers(params, verbose):
                    errors = True
                    continue

                new_interval = Interval(int(params[0]), int(params[1]), int(params[2]))

                if verbose:
                    print(green("\t\tinterval >"), interval_to_string(new_interval))

                total = total + 1
                timeline[count].append(new_interval)

            if not timeline[count]:
                if verbose:
                    print(yellow("no intervals found. Skipping line."))
                del timeline[-1]
            else:
                if verbose:
                    print(green("intervals found:"), len(timeline[count]))
                count = count + 1

            if verbose:
                print() # newline

    if verbose:
        print("reached end of file.")
        print("found {} intervals across {} channels.".format(total, len(timeline)))

    return timeline, errors

def file_exists(filename):
    """
    Returns true if the filepath exists and is a file (not a folder).
        :param filename: is the file to look for
    """
    file = Path(filename)
    return file.is_file()

def parse_check_format(intv, verbose=False):
    """
    Checks if a string could contain an interval. This function just exists to
    shorten read_timeline() to something that Python won't throw warnings about.
    There's no need to call this outside that function.
        :param intv: is the string to check.
        :param verbose: is an optional flag.
            When true, extra parsing information is printed to the console. Defaults to false.
    """
    if len(intv) < 5:
        if verbose:
            print(black("\tinvalid length > ", bold=True), end='')
            print(add_quotes(intv))
        return False

    if verbose:
        print(blue("\tpossible interval > ", bold=True), end='')
        print(add_quotes(intv))
    return True

def parse_check_numbers(params, verbose=False):
    """
    Checks if a list contains interval info. This function just exists to
    shorten read_timeline() to something that Python won't throw warnings
    about. There's no need to call this outside that function.
        :param params: is the list to check.
        :param verbose: is an optional flag.
            When true, extra parsing information is printed to the console. Defaults to false.
    """

    if len(params) != 3:
        if verbose:
            print(magenta("\t\tinvalid parameter count:"), len(params))
        return False

    for param in params:
        try:
            num = int(param, 10) # 10 is the number base
        except ValueError:
            if verbose:
                print(red("\t\tinvalid integer > "), end='')
                print(add_quotes(param))
            return False
        else:
            if num < 0:
                if verbose:
                    print(red("\t\tinvalid integer range > "), end='')
                    print(add_quotes(param))
                return False
    return True

# Returns a statically-defined timeline
def get_test_timeline():
    """
    Returns a statically-defined timeline for testing purposes.
    """
    # make timeline array
    timeline = []

    # add an array of intervals to the timeline
    timeline.append([])
    # add intervals to that array
    timeline[0].append(Interval(0, 2, 2))
    timeline[0].append(Interval(4, 1, 6))
    timeline[0].append(Interval(8, 2, 8))

    # add another array of intervals to the timeline
    timeline.append([])
    # add intervals to that new interval
    timeline[1].append(Interval(3, 4, 4))
    timeline[1].append(Interval(0, 2, 2))
    timeline[1].append(Interval(4, 1, 6))
    timeline[1].append(Interval(8, 4, 8))

    # you know the drill.
    timeline.append([])
    timeline[2].append(Interval(2, 3, 1))
    timeline[2].append(Interval(6, 2, 9))

    return timeline
