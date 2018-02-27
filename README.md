# PneuNet

## Overview
This project allows for time-sensitive, repetitive, and easily-edited motion definitions for soft robots driven by soft actuators. The philosophy is like that of Guitar Hero or a MIDI tracker, with intermittent activations on several parallel timelines. This program sets the PWM outputs of an Adafruit PCA9685 to match a defined cycle to achieve some gait, grip, or other motion through the control of its PneuNet.

## Usage
Run `main.py`. If that doesn't work, try typing `python3 ./main.py` in a console. If that doesn't work, make sure Python 3.x is installed and added to the `PATH`. If you get an error when connecting, try running as admin or with sudo.

### Command line arguments
Command line arguments are optional but may improve workflow. The user will be prompted to enter any information that was not provided in the arguments, so the program retains full functionality without them. Run with the `-h` parameter to view a brief help page.

To read any file directly, specify the path (relative or absolute) as the first argument:

	./main.py ./gaits/file.gait

This will start the program with that gait file selected. The user can still open a different file from within the program; this only changes the initial state. Similarly, you can specify both the cycle time and the amplitude multiplier (in that order) after the filename to reduce initial interaction:

	./main.py ./gaits/file.gait 15 0.8

To enter the editor/visualizer mode directly, pass `-e`, optionally followed by a filename:

	./main.py -e [./gaits/file.gait]

This again only sets the initial state, so the program can open other files, switch to run mode, etc. after starting in the editor/visualizer mode.

## Editor/Visualizer Mode
Use the editor/visualizer mode to print extra parsing info alongside a matrix of amplitudes showing when and how much each actuation will be. This can help clarify what a timeline has defined or where an error is. Run the program with `main.py -e [filename]` to launch into this mode directly or select it from the main menu.

## Files
The motion file specifies intervals on channels. Use the .gait or .txt extension, and place gaits in the `gaits` folder, which is next to `main.py`. The program automatically scans only this folder when presenting the file-selection menu, but you can specify any file location if you don't mind typing the path.

### Syntax and Formatting
Each interval consists of 3 integers: start, duration, and amplitude (in that order). These are separated by spaces (or any whitespace). Each interval is separated by a comma and optional whitespace. Each channel is a single line of the file. Channels currently cannot be empty (just use `0 0 0` to ignore a channel), so if a line has no (valid) intervals, the next line is checked for the next channel. Example of standard syntax:

	1 2 3, 4 5 6
	# Comment symbol ignores this line. The line above is channel 0
	1 2 3,        7 8 9 # In-line comment. This line is channel 1

This snippet would read 2 channels with 2 intervals each. 

Comments begin at `#` and end at the end of the line:

	1 2 3 # an in-line comment, 4 5 6

This example would parse (1 2 3) and ignore the rest.

The number of steps in a timeline (how many columns are in the visualizer) can be specified before the intervals. If the step count is not specified, a default of 10 is used. The parser is looking for a line with a single number in it that isn't in a comment. Here is the recommended format for the beginning of a gait file:

	# Here is a comment saying what this gait is for
	steps: 15

	1 2 3, 4 5 6

Feel free to use spaces and tabs to help with formatting and readability; it will be ignored by the parser. If there are syntax errors, the file will still execute. Errors are soft and do not affect execution, except to potentially invalidate any numbers involved, or shifting intended channels. Pay close attention to the number matrix printed before running a gait to ensure safety. Read "Troubleshooting" -> "File isn't reading as expected" for tips on finding syntax errors.

## PWM Output
This program will set the duty cycle of the Adafruit PCA9685 as specified in a .gait file. The scale, frequency, and board count are specified in `output.py` as `OUTPUT_SCALE`, `OUTPUT_FREQUENCY`, and `BOARD_COUNT`.

The scale is the maximum duty cycle. For the Adafruit PCA9685, with 12 bits of precision, the maximum is 2048. Thus, a duty cycle of 50% would be 1024. These numbers are handled behind the scenes, but be aware that changing hardware could require changing the output scale to match.

The frequency controls how many times per second the valves open and close. The Adafruit PCA9685 has a minimum frequency generally above 30Hz, so setting it to 30 (the default already specified) will use the minimum possible. Too high of a frequency does not leave time for the valves to physically switch states.

The board count specifies how many Adafruit PCA9685 boards are chained together on the I2C bus. Note that boards must be consecutively addressed, so 2 boards must have offsets of 0 and 1, without skipping addresses in the middle. This is because `output.py` attempts connections to consecutive addresses after 0x040, so incorrectly soldered addressing pads will prevent a board from being recognized. Look up Raspberry Pi I2C wiring guides, or tutorials specific to the Adafruit PCA9685 for more information on how to properly assemble a new controller.

## Troubleshooting
### I2C devices aren't recognized
Make sure the user has access to the I2C interface. This often means being part of the `I2C` UNIX group. For a quick fix, try running the program with `sudo`. Read the "PWM Output" section for more information on other possible issues. As always, make sure no wires are disconnected, shorted, or out of place.

### File isn't reading as expected
Switch to the editor/visualizer mode and take a close look at the extra parsing info. If you use Notepad++, go to `language -> Define your language -> Import` and choose the language definition file, `NP++_Gait_Def.xml`, in the root of the repository. This will enable syntax highlighting for .gait that can help identify any mistakes. Note that this language definition isn't perfect because of the limitations of the Notepad++ definition system. For example, the requirements for properly specifying a timeline length are too complex to be properly detected except in the editor/visualizer mode.

### Colored output doesn't work properly
Make sure you have the most recent version of the `ansicolor` package installed. Your terminal must also support basic color ANSI escape sequences.

## Attribution
This repository is maintained by Oregon State University mLab, for research in soft robotics. All code developed by Gabriel Kulp (kulpga[at]oregonstate[dot]edu), except when specified differently in a file header.