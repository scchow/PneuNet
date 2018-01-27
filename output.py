#!/usr/bin/python3
"""
    Author: Gabriel Kulp
    Created: 1/19/2017

    This module is the entry point. It's the only one that
    executes code on its own or interacts with the user directly.
"""

import platform
import serial
import serial.tools.list_ports

def choose_port():
    """
        This function returns a valid serial port. If more than one is
        available, it will ask the user.

            :returns: the port name as a string
    """
    ports = [comport.device for comport in serial.tools.list_ports.comports()]

    open_ports = []
    for port in ports:
        try:
            ser = serial.Serial(port)
            ser.close()
            open_ports.append(port)
        except serial.SerialException:
            pass

    if not open_ports:
        return False

    if len(open_ports) == 1:
        return open_ports[0]

    print("\nMultiple ports are available:")

    for num, port in enumerate(open_ports):
        print("{}\t{}".format(num + 1, port))

    print()
    choice = 0
    while choice > len(open_ports) or choice < 1:
        try:
            choice = int(input("Which port? (1-{}) ".format(len(open_ports))))
        except ValueError:
            pass

    return open_ports[choice - 1]


class Arduino:
    """
    Gives access to an Arduino over serial.
    """

    def __init__(self):
        self.ser = None

    def connect(self, port='', baud=9600):
        """
        This function starts a new serial connection to an Arduino.
            :param port: is the port to try to connect with.
            :param baud: is the baudrate to connect with.
        """
        if port == '':
            port = choose_port()

        if not port:
            return False

        try:
            self.ser = serial.Serial(port, baud)
            return True
        except serial.SerialException:
            return False

    def disconnect(self):
        """
        This function closes the serial connection to the Arduino.
        """
        try:
            self.ser.write(b'a')
        except serial.SerialException:
            pass
        self.ser.close()
        return True

    def send_raw(self, message):
        """
        This function lets you send any string to a connected Arduino.
            :param message: is the string to send.
        """
        self.ser.write(message.encode(encoding='ascii'))
        self.ser.flush()

    def send(self, amplitudes):
        """
        This function sends an array of amplitudes to the connected Arduino.
            :param amplitudes: is the array to send.
        """
        msg = ''
        for i, amplitude in enumerate(amplitudes):
            msg = msg + ' ' + str(i) + ' ' + str(int(amplitude))

        self.send_raw(msg)

    def clear(self):
        """
        This function sends the "abort" command to the connected Arduino,
        which shuts off all outputs.
        """
        self.send_raw('a')
