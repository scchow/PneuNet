# PneuNet

## Overview
This project allows for time-sensitive, repetative, and easily-edited motion definitions of soft robots driven by soft actuators. The philosophy is similar to that of a MIDI tracker, with intetmittent activations on several parallel timelines. This program sets a Raspberry Pi's (or Arduino's) PWM outputs to match a defined cycle to achieve some gait, grip, or other motion through the control of its PneuNet.

## Usage
Run `main.py`. If that doesn't work, try typing `python3 main.py` in a console. If that doesn't work, make sure Python 3.x is installed and added to the `PATH`.

## PWM Output
When run on a Raspberry Pi, this program will set the duty cycle of PWM pins as specified in the motion config file. This is the main purpose of this program. It can also be run with a serial connection to an Arduino to use its PWM pins. Look up the PWM-capable pins and change `PINS` and `PIN_COUNT` in `arduino.ino` accordingly before compiling for your particular Arduino board.

## Files
The motion file specifies intervals on channels. Each interval consists of 3 integers: start, duration, and amplitude (in that order). These are separated by spaces. Each interval is separated by a comma. Each channel is a single line of the file. Channels currently cannot be empty, so if a line has no (valid) intervals, the next line is checked for the next channel. Example of standard syntax:

	1 2 3, 4 5 6
	Comment that is ignored
	1 2 3,        7 8 9

This file would read 2 channels with 2 intervals each.

The parsing function is very resiliant to errors, so feel free to use spaces, tabs, etc. to help with formatting for readability; it will be ignored by the parser. Also, feel free to add comments. If you want a comment in-line with an interval, be sure to separate it from the good numbers with commas so it isn't seen as extra invalid parameters for a neighboring interval, like so:

	1 2 3, 	4 5   6, this is a comment, 7 8 9, and 1 2 3 this is another.

This example would parse as (1 2 3) (4 5 6) (7 8 9) and ignore the rest.


## Troubleshooting
### Arduino isn't connecting
Press the reset button or power cycle the Arduino. Make sure you have the correct `arduino.ino` code on the Arduino and that it's connected and powered. Check your `COM` (Windows) or `tty` (*nix) ports and make sure the computer sees the Arduino and nothing else is using the port.

### Motion definitions (timelines) seem wrong
The `print_timeline()` function prints a matrix of characters showing the amplitude at each channel at each time. This can help clarify what a timeline has defined.

### File is not reading correctly
If you can't figure out why your file is being parsed the way it is, run `read_Timeline()` with the second argument `verbose = true` and it will print a detailed walkthrough of its interpretation of the specified file.

### Colored output doesn't work properly
You must use a console that supports ANSI color escape sequences. This means CMD and Powershell on Windows won't work. Also make sure the `ansicolor` Python package is installed.
