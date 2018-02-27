#!/usr/bin/python3
"""
    Author: Gabriel Kulp
    Created: 1/19/2017

    This module is the entry point. It's the only one that
    executes code on its own or interacts with the user directly.

    ***This is the edited version to use the old Arduino code***
"""

# Global setting for maximum output amplitue
OUTPUT_SCALE = 2048
# Global setting for PWM output frequency
OUTPUT_FREQUENCY = 30
# Global setting for number of consecutive-addressed chained boards
BOARD_COUNT = 2

try:
    import Adafruit_PCA9685
    CAPABLE = True
except ImportError:
    print("I2C library not installed. Enabling fake output.")
    CAPABLE = False

class PWM_board:
    """
    Gives access to PWM breakout boards over I2C.
    """

    # setting to [] allows declaration of an Arduino without connecting to it
    def __init__(self):
        self.boards = []

    def connect(self):
        """
        Starts a new connection to I2C boards. Assumes addresses start at 0x040 and increment
        """
        if not CAPABLE:
            return True

        for x in range(0, BOARD_COUNT):
            try:
                self.boards.append(Adafruit_PCA9685.PCA9685(address=0x040 + x))
                self.boards[x].set_pwm_freq(OUTPUT_FREQUENCY)
            # catch connection failures
            except:
                return False
        return True

    def disconnect(self):
        """
        Sends zeros and deletes boards
        """
        if not CAPABLE:
            return True

        # try to send abort command. if it fails, move on
        try:
            self.clear()
        except:
            pass
        self.boards = []
        return True

    def send(self, amplitudes):
        """
        Sends an array of amplitudes to the connected devices.
            :param amplitudes: is the array to send.
        """
        if not CAPABLE:
            return

        for num, amplitude in enumerate(amplitudes):
            channel = num % 16
            board = (num - channel) // 16
            self.boards[int(board)].set_pwm(int(channel), 0, int(amplitude * OUTPUT_SCALE))

    def clear(self):
        """
        Shuts off all outputs.
        """
        if not CAPABLE:
            return

        for board in self.boards:
            for num in range(0,16):
                board.set_pwm(num, 0, 0)
