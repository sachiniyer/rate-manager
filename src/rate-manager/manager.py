"""
Manager file.

Contains the rate manager.
"""

import json
import os
import time


class Time:
    """
    Time class.

    Contains the time and the rate.
    """

    def __init__(self, time):
        """
        Init function.

        Defines the time and the rate.
        """
        self.time = time
        self.active = 0

    def add_active(self):
        """
        Set active.

        Sets the active value.
        """
        self.active += 1

    def remove_active(self):
        """
        Remove active.

        Removes the active value.
        """
        self.active -= 1


class Rate:
    """
    Rate class.

    Contains the rate and the times.
    """

    def __init__(self, interval, amount):
        """
        Init function.

        Defines the rate and the times.
        """
        self.inteval = interval
        self.amount = amount
        self.times = []

    def add_time(self, time):
        """
        Add time.

        Adds a time to the list of times.
        """
        self.times.append(time)

    def get_time(self, time):
        """
        Get time.

        Gets the time from the list of times.
        """
        for item in self.times:
            if item.time == time:
                return item
        return None

    def sync_times(self):
        """
        Sync times.

        Syncs the times with the current time.
        """
        current_time = time.time()
        for item in self.times:
            if item.time < current_time:
                item.remove_active()
                self.times.remove(item)
            else:
                break


class Manager:
    """
    Manager class.

    Contains all the high level methods for the Manager.
    """

    def __init__(self, rates, file="log.txt"):
        """
        Init function.

        Defines the rates, and optionally reads from files.
        """
        self.check_rates(rates)
        self.rates = []
        self.times = {}

    def check_rates(rates):
        """
        Check rates.

        Makes sure that all the rates are positive ints.
        """
        if not isinstance(rates, dict):
            raise TypeError("Rates is not a dictionary")
        for key, value in rates.items():
            if (not all(isinstance(key, int),
                        isinstance(value, int),
                        key > 0,
                        value > 0)):
                raise ValueError("Rates and Times must be positive integer"
                                 f"values: {key}: {value}")

    def parse_rates(self, rates, file):
        """
        Parse rates.

        Parses the rates into a queue.
        """
        contents = []
        if os.path.exists(file):
            with open(file, "r") as f:
                contents = f.read()
                contents = json.loads(contents)

        for key, value in rates.items():
            if key in contents:
                add_rate = Rate(key, value)
                for newtime in contents[key].times:
                    if newtime not in self.times:
                        self.times[newtime] = Time(newtime)
                self.rates.append(add_rate)
            else:
                self.rates.append(Rate(key, value))

        sorted_times = self.times.keys().sort()
        for newtime in sorted_times:
            for rate in self.rates:
                rate.times.append(self.times[newtime])
                self.times[newtime].add_active()
        for rate in self.rates:
            rate.sync_times()
