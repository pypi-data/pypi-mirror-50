"""
Timerr Module for Python
~~~~~~~~~~~~~~~~~~~

A basic timer that counts down from
the time desired. Its pretty good.

(c) 2019 ItzAfroBoy. 
MIT License
"""

__title__ = 'timerr'
__author__ = 'ItzAfroBoy'
__license__ = 'MIT License'
__copyright__ = 'Copyright 2019 ItzAfroBoy'
__version__ = '1.0.4'

import chalk
import time
import os


class Timer():
    def __init__(self, hours=1, mins=0, secs=0, log=None):
        """
        The args are integers so make sure to pass
        ONLY integers (whole numbers)

        The only exception is the log arg which is a string
        """
        self.hours = hours
        self.mins = mins
        self.secs = secs
        self.log = log

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def time(self):
        if self.log == 'log':
            Timer.cls(self)
            print(f'{self.hours:02d}:{self.mins:02d}:{self.secs:02d}', end='\r')
        else:
            return

    def timer(self):
        go = 'true'
        while go != 'false':
            Timer.time(self)
            time.sleep(1)
            if self.hours == 0 and self.mins == 0 and self.secs == 0:
                go = 'false'
                Timer.cls(self)
            if self.hours == 0 and self.mins == 1 and self.secs == 0:
                self.mins -= 1
                self.secs += 60
            if self.hours != 0 and self.mins == 0 and self.secs == 0:
                self.hours -= 1
                self.mins += 59
                self.secs += 60
            if self.secs == 0:
                self.mins -= 1
                self.secs += 60
            self.secs -= 1

        time.sleep(1)
        print('Done')
        time.sleep(1)
        exit
