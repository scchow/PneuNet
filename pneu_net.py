#!/usr/bin/python3
"""
    Makes a pneu-net follow a gait specified in a file.
        :param file: is the path to the gait file.
"""

from collections import namedtuple
import time

#
# Core
#

# Make data structure used for each interval in the timeline
Interval = namedtuple("Interval", "start duration amplitude")
STEPS_IN_TIMELINE = 10

# runs through one cycle of the timeline
def do_cycle(timeline, total_time):
    """
    Runs through one cycle of the gait.
        :param timeline: is the 2D array of intervals to read.
        :param total_time: is the time it should take to complete the cycle.
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
        write_out(amplitudes)

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

# will eventually change PWM pin values
def write_out(value):
    """
    Prints stuff to the console and writes to Arduino pins if one is connected.
        :param value: the stuff to print.
    """
    print(value, sep='')

#
# Visualization
#
def print_timeline(timeline, use_color=True):
    """
    Prints a graphical representation of the timeline to the console.
        :param timeline: is the 2D array of intervals to read.
        :param use_color: is an optional flag.
            When true, prints with ANSI colors. Defaults to true.
    """

    pad_length = len(str(len(timeline)))

    for channel in range(0, len(timeline)):
        current_index = 0
        amp = 0
        print(str(channel).zfill(pad_length), " > ", sep='', end='')
        for current_time in range(0, STEPS_IN_TIMELINE):
            (amp, current_index) = read_channel(timeline, channel, current_index, current_time)
            if use_color and amp == 0:
                print("\033[30;1m", amp, " \033[0m", sep='', end='')
            else:
                print(amp, " ", sep='', end='')
        print(sep='')

def interval_to_string(interval):
    """
    Returns a string representation of an interval.
        :param interval: is the interval to evaluate.
    """
    components = ["[", str(interval.start), " ",
                  str(interval.duration), " ", str(interval.amplitude), "]"]
    return ''.join(components)


#
# Input
#

# reads timeline from file. Check README.md for more details.
def read_timeline(filename, verbose=False):
    """
    Reads a timeline of intervals from a text file.
        :param filename: is the path to the timeline file.
        :param verbose: is an optional flag.
            When true, extra parsing information is printed to the console. Defaults to false.
    """
    # make timeline array
    timeline = []

    count, total = 0, 0

    with open(filename) as lines:
        for line in lines:
            line = line.strip()
            if verbose:
                print("reading line > \"", line, "\"", sep='')

            intvs = line.split(",")
            timeline.append([])

            for intv in intvs:
                intv = intv.strip()

                if len(intv) < 5:
                    if verbose:
                        print("\033[30;1m    invalid length > \033[0m", end='')
                        print("\"", intv, "\"", sep='')
                    continue

                if verbose:
                    print("\033[36m    possible interval > \033[0m", end='')
                    print("\"", intv, "\"", sep='')

                params = intv.split(" ")

                if len(params) != 3:
                    if verbose:
                        print("\033[35;1m        invalid parameter count\033[0m")
                    continue

                bad = False
                for param in params:
                    try:
                        num = int(param, 10) # 10 is the number base
                    except ValueError:
                        if verbose:
                            print("\033[31m        invalid integer > \033[0m", end='')
                            print("\"", param, "\"", sep='')
                        bad = True
                        break
                    else:
                        if num < 0:
                            if verbose:
                                print("\033[31m        invalid integer range > \033[0m", end='')
                                print("\"", param, "\"", sep='')
                            bad = True
                            break

                if bad:
                    continue

                new_interval = Interval(int(params[0]), int(params[1]), int(params[2]))

                if verbose:
                    print("\033[32m        interval > \033[0m", end='')
                    print("\"", interval_to_string(new_interval), "\"", sep='')

                total = total + 1
                timeline[count].append(new_interval)

            if not timeline[count]:
                if verbose:
                    print("\033[33mno intervals found. Skipping line.\033[0m")
                del timeline[-1]
            else:
                count = count + 1

            if verbose:
                print(sep='')

    if verbose:
        print("reached end of file.")
        print("found", total, "intervals across", len(timeline), "channels.")

    return timeline

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


#
# Main
#

def start():
    """
    Starts the program. This means reading the file,
        parsing the intervals, and executing the timeline.
    """
    timeline = read_timeline("mynums.txt", True)
    print_timeline(timeline)
    print(sep='')

    # choose how long to spend on one cycle, in seconds
    cycle_time = 1
    cycle_count = 2

    for cycle in range(0, cycle_count):
        print("Cycle ", cycle, ":", sep='')
        do_cycle(timeline, cycle_time)
        # extra time is approximately constant,
        #  independent of the cycle length.

start()
