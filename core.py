#!/usr/bin/python3
"""
    Author: Gabriel Kulp
    Created: 1/19/2017

    This module holds global variables and the functions
    most fundamental to this program.
"""

import time
from collections import namedtuple

# Make data structure used for each interval in the timeline
Interval = namedtuple("Interval", "start duration amplitude")

# Global setting for time granularity
STEPS_IN_TIMELINE = 4
# Global setting for amplitude granularity
STEPS_IN_AMPLITUDE = 10
# Global setting for output device granularity
STEPS_IN_OUTPUT = 100

# runs through one cycle of the timeline
def do_cycle(device, timeline, total_time, multiplier):
    """
    Runs through one cycle of the gait.
        :param device: is the output device
        :param timeline: is the 2D array of intervals to read.
        :param total_time: is the time it should take to complete the cycle.
        :param multiplier: is the maximum amplitude outputted.
    """

    # set the index on each channel to 0
    curr_index = [0] * len(timeline)

    # run through timeline
    for curr_time in range(0, STEPS_IN_TIMELINE):
        # start row with time stamp
        print(curr_time, "\t", sep='', end='')

        amplitudes = []

        # find value of each channel
        for chan in range(0, len(timeline)):
            # return value and update channel's current index
            amp, curr_index[chan] = read_channel(timeline, chan, curr_index[chan], curr_time)
            amplitudes.append(amp)

        # set all values at once
        write_out(device, amplitudes, multiplier)

        time.sleep(total_time/STEPS_IN_TIMELINE)


# return value on the selected channel given the time
def read_channel(timeline, channel_id, curr_index, curr_time):
    """
    Returns the current amplitude specified in the timeline.
        :param timeline: is the 2D array of intervals to read.
        :param channel_id: is the ID number of the pneumatic valve channel.
        :param curr_index: is the index in the timeline to start reading from.
        :param curr_time: is the time on the timeline to evaluate.
    """
    # while not past last interval
    while curr_index < len(timeline[channel_id]):

        # get interval to check
        curr_interval = timeline[channel_id][curr_index]

        # if we're past the starting point
        if curr_time >= curr_interval.start:
            # if currently in the interval's duration
            if curr_time - curr_interval.start < curr_interval.duration:

                # return the interval's amplitude and index (since it might have incremented)
                return (curr_interval.amplitude, curr_index)

            else: # not in duration

                # finished one interval; check next interval
                curr_index = curr_index + 1

                # start at the top of the while loop again,
                # but fetching a different interval to test
                continue
        else: # not past the starting point
            # between intervals
            return 0, curr_index

    # after last interval in timeline
    return 0, curr_index

def write_out(device, values, multiplier):
    """
    Prints stuff to the console and writes to device pins if available.
        :param device: is the device to output to.
        :param values: the stuff to print.
        :param multiplier: scales the output values, but only to the device. Unscaled
            numbers are printed to the screen.
    """
    print(values)
    scaled_values = []
    # re-scales data from internal representation to external input representation.
    for value in values:
        value = float(value) * float(multiplier) * float(STEPS_IN_OUTPUT) / float(STEPS_IN_TIMELINE)
        scaled_values.append(value)
    device.send(scaled_values)
