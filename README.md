# PneuNet

## Overview
This project allows for time-sensitive, repetitive, and easily-edited motion definitions of soft robots driven by soft actuators. The philosophy is similar to that of a MIDI tracker, with intermittent activations on several parallel timelines. This program sets an Arduino's PWM outputs to match a defined cycle to achieve some gait, grip, or other motion through the control of its PneuNet.

## Usage
Run `main.py`. If that doesn't work, try typing `python3 ./main.py` in a console. If that doesn't work, make sure Python 3.x is installed and added to the `PATH`. If you get an error when connecting, try running as admin or with sudo. To read in any file directly, specify the path (relative or absolute) as a command line argument:

	sudo ./main.py ./gait_file.abc

This will run the program with that gait file until the user specifies that they want to use a different file. Similarly, you can specify both the cycle time and the amplitude multiplier after the filename to reduce interaction:

	sudo ./main.py ../gait_file.abc 15 0.8

To enter the editor/visualizer mode directly, pass `-e`:

	./main.py -e [../gait_file.abs]

You can optionally specify a gait file after. If none is specified, the user will be prompted to choose as normal.

## PWM Output
This program will set the duty cycle of Arduino PWM pins as specified in the motion config file. This is the main purpose of this program. Look up the PWM-capable pins and change `PINS` and `PIN_COUNT` in `arduino.ino` accordingly before compiling for your particular Arduino board. See the "Arduino" section for details on the protocol used for the serial connection.

## Editor/Visualizer Mode
Use the editor/visualizer mode to print extra parsing info alongside a matrix of amplitudes showing when and how much each actuation will be. This can help clarify what a timeline has defined or where an error is. Run the program with `main.py -e [filename]` to launch into this mode, or select it from the main menu.

## Files
The motion file specifies intervals on channels. Use the .gait or .txt extension, and place gaits in the `gaits` folder, which is next to `main.py`. The program only automatically scans this folder when presenting the file-selection menu, but you can specify any file location if you don't mind typing it.

Each interval consists of 3 integers: start, duration, and amplitude (in that order). These are separated by spaces. Each interval is separated by a comma. Each channel is a single line of the file. Channels currently cannot be empty (just use `0 0 0` to ignore it), so if a line has no (valid) intervals, the next line is checked for the next channel. Example of standard syntax:

	1 2 3, 4 5 6
	# Comment symbol ignores this line
	1 2 3,        7 8 9 # In-line syntax

This file would read 2 channels with 2 intervals each. 

Comments begin at `#` and end at the end of the line:

	1 2 3 # an in-line comment, 4 5 6

This example would parse (1 2 3) and ignore the rest. 

Feel free to use spaces and tabs to help with formatting and readability; it will be ignored by the parser. If there are syntax errors, the file will still execute. Errors are soft and do not affect execution, except to potentially invalidate any numbers involved. Read "Troubleshooting" -> "File isn't reading as expected" for tips on finding syntax mistakes.

## Troubleshooting
### Arduino isn't connecting
Press the reset button or power cycle the Arduino. Make sure you have the correct `arduino.ino` code on the Arduino (check the "PWM Output" section for notes on this) and that it's connected and powered. Check your `COM` (Windows) or `tty` (*nix) ports and make sure the computer sees the Arduino and (if using Windows) nothing else is using the port. Also be sure you have permission to access serial ports. This might mean using sudo or running as an admin.

### File isn't reading as expected
Switch to the editor/visualizer mode and take a close look at the extra parsing info. If you use Notepad++, go to `language -> Define your language -> Import` and choose the language definition file, `NP++_Gait_Def.xml`, in the root of the repository. This will enable syntax highlighting that can help in identify mistakes.

### Colored output doesn't work properly
You must use a console that supports ANSI color escape sequences. This means CMD and PowerShell on Windows won't work. If you're using Windows, try installing WSL by searching for "Ubuntu" on the Windows Store and following the instructions.

## Arduino
The Arduino connects with ASCII encoding and 9600 baud over whatever serial connection is available on the host. The commands are effectively time-delimited. The format of each command is numbers separated by spaces. Numbers specify the desired duty cycle within the range [0, 255]. The first number is for pin 0 (as specified at the top of `arduino.ino`), the second for pin 1, etc. until the input buffer is empty. Any pins not changed are set to 0, and any extra pins specified are ignored. Sending 'a' aborts operation by setting all duty cycles to 0. After any command, the Arduino sends 'r' in response to acknowledge it has read the command.

## Attribution
This repository is maintained by Oregon State University mLab, for research in soft robotics. All code developed by Gabriel Kulp: kulpga[at]oregonstate[dot]edu.