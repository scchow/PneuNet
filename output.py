#!/usr/bin/python3
"""
    Author: Gabriel Kulp
    Created: 1/19/2017

    This module is the entry point. It's the only one that
    executes code on its own or interacts with the user directly.
"""

import serial
import platform

class Arduino:
    '''
    Gives access to an Arduino over serial.
    '''

    def __init__(self):
        self.ser = None

    def connect(self, port='', baud=9600):
        '''
        This function starts a new serial connection to an Arduino.
            :param port: is the port to try to connect with.
            :param baud: is the baudrate to connect with.
        '''
        if port == '':
            if platform.system() == 'Windows':
                port = 'COM4'
            else:
                port = '/dev/ttyS4'

        try:
            self.ser = serial.Serial(port, baud)
            return True
        except serial.SerialException:
            return False

    def disconnect(self):
        '''
        This function closes the serial connection to the Arduino.
        '''
        try:
            self.ser.write(b'a')
        except serial.SerialException:
            pass
        self.ser.close()
        return True

    def send(self, amplitudes):
        '''
        This function sends an array of amplitudes to the connected Arduino.
            :param amplitudes: is the array to send.
        '''
        msg = ''
        for i in range(0, len(amplitudes)):
            msg = msg + ' ' + str(i) + ' ' + str(int(amplitudes[i] * 25.5))

        self.ser.write(msg.encode(encoding='ascii'))
        self.ser.flush()
