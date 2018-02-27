#!/usr/bin/python3
"""
    Author: Gabriel Kulp
    Created: 1/19/2017

    This module has functions to help with visualizing timelines.
"""

from ansicolor import black # install package by typing: pip install ansicolor
from core import read_channel

def print_timeline(timeline, steps):
    """
    Prints a graphical representation of the timeline to the console.
        :param timeline: is the 2D array of intervals to read.
    """

    print() # newline

    # count number of digits of left column to align numbers
    pad_length = len(str(len(timeline)))

    # print the row
    for channel in range(0, len(timeline)):
        current_index = 0
        amp = 0
        print(str(channel).zfill(pad_length), " >  ", sep='', end='')
        # print the columns
        for current_time in range(0, steps):
            (amp, current_index) = read_channel(timeline, channel, current_index, current_time)
            # make the zeros stand out. easier to look at that way
            if amp == 0:
                print(black(str(amp), bold=True), " ", sep='', end='')
            else:
                print(amp, " ", sep='', end='')
        print() # newline
    print() # newline

def interval_to_string(interval):
    """
    Returns a string representation of an interval.
        :param interval: is the interval to evaluate.
    """
    # turn numbers into a single string
    nums = str(interval.start) + " " + str(interval.duration) + " " + str(interval.amplitude)

    # put brackets on the ends
    bracket_nums = black("[", bold=True) + nums + black("]", bold=True)

    return bracket_nums

def add_quotes(message):
    """
    Adds grey quotes around text.
        :param message: is the string to put quotes around.
    """
    return black("\"", bold=True) + str(message) + black("\"", bold=True)
