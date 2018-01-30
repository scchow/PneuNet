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
    Returns a valid serial port. If more than one is
    available, it will ask the user.

        :returns: the port name as a string
    """
    ports = [comport.device for comport in serial.tools.list_ports.comports()]

    open_ports = []
    for port in ports:
        if port.find("AMA") != -1:
             continue
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
        print(" {}\t{}".format(num + 1, port))

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
        Starts a new serial connection to an Arduino.
            :param port: is the port to try to connect with.
            :param baud: is the baudrate to connect with.
        """
        if port == '':
            port = choose_port()

        if not port:
            return False

        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            return True
        except serial.SerialException:
            return False

    def disconnect(self):
        """
        Closes the serial connection to the Arduino.
        """
        try:
            self.ser.write(b'a')
        except serial.SerialException:
            pass
        self.ser.close()
        return True

    def send_raw(self, message):
        """
        Lets you send any string to a connected Arduino.
            :param message: is the string to send.
        """
        self.ser.write(message.encode(encoding='ascii'))
        self.ser.flush()
        try:
            self.ser.read(1)
        except serial.SerialException:
            pass

    def send(self, amplitudes):
        """
        Sends an array of amplitudes to the connected Arduino.
            :param amplitudes: is the array to send.
        """
        msg = ''
        for amplitude in amplitudes:
            msg = msg + ' ' + str(int(amplitude))

        self.send_raw(msg)

    def clear(self):
        """
        Sends the "abort" command to the connected Arduino,
        which shuts off all outputs.
        """
        self.send_raw('a')
