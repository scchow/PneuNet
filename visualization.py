#!/usr/bin/python3
"""
    Author: Gabriel Kulp
    Created: 1/19/2017

    This module has functions to help with visualizing timelines.
"""

from ansicolor import black # install package by typing: pip install ansicolor
from core import STEPS_IN_TIMELINE, read_channel

def print_timeline(timeline):
    """
    Prints a graphical representation of the timeline to the console.
        :param timeline: is the 2D array of intervals to read.
    """
    print() # newline

    pad_length = len(str(len(timeline)))

    for channel in range(0, len(timeline)):
        current_index = 0
        amp = 0
        print(str(channel).zfill(pad_length), " >  ", sep='', end='')
        for current_time in range(0, STEPS_IN_TIMELINE):
            (amp, current_index) = read_channel(timeline, channel, current_index, current_time)
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

    nums = str(interval.start) + " " + str(interval.duration) + " " + str(interval.amplitude)

    bracket_nums = black("[", bold=True) + nums + black("]", bold=True)

    return bracket_nums

def add_quotes(message):
    """
    Adds grey quotes around text.
        :param message: is the string to put quotes around.
    """
    return black("\"", bold=True) + str(message) + black("\"", bold=True)
