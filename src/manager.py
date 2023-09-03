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
        self.interval = interval
        self.amount = amount
        self.times = []

    def add_time(self, time, times):
        """
        Add time.

        Adds a time to the list of times.
        """
        self.times.append(times[time])
        times[time].add_active()

    def get_wait_time(self, times):
        """
        Get wait time.

        Gets the wait time for the next time.
        """
        current_time = time.time()
        self.sync_times(times)
        if len(self.times) >= self.amount:
            return self.times[-self.amount].time - current_time + self.interval
        if len(self.times) > 0:
            return self.times[0].time - current_time - self.interval
        return 0

    def sync_times(self, times):
        """
        Sync times.

        Syncs the times with the current time.
        """
        current_time = time.time()
        for item in self.times:
            if item.time + self.interval < current_time:
                item.remove_active()
                if times[item.time].active <= 0:
                    times.pop(item.time)
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
        self.rates = []
        self.times = {}
        self.file = file
        self.check_rates(rates)
        self.parse_rates(rates, file)

    def check_rates(self, rates):
        """
        Check rates.

        Makes sure that all the rates are positive ints.
        """
        if not isinstance(rates, dict):
            raise TypeError("Rates is not a dictionary")
        for key, value in rates.items():
            if (not all((isinstance(key, int),
                        isinstance(value, int),
                        key > 0,
                        value > 0))):
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

        sorted_times = sorted(self.times.keys())
        for newtime in sorted_times:
            for rate in self.rates:
                rate.times.append(self.times[newtime])
                self.times[newtime].add_active()
        for rate in self.rates:
            rate.sync_times(self.times)
        self.sync_file()

    def sync_file(self):
        """
        Sync file.

        Syncs the file with the current state of the program.
        """
        dump_obj = []

        for r in self.rates:
            times = []
            for t in r.times:
                times.append(t.time)
            dump_obj.append({r.interval:
                             {"amount": r.amount,
                              "times": times}})
        with open(self.file, "w") as f:
            f.write(json.dumps(dump_obj))

    def check_time(self):
        """
        Check time.

        Checks the current time and updates the rates.
        """
        wait_time = -1
        for r in self.rates:
            wait_time = max(r.get_wait_time(self.times), wait_time)
        if wait_time <= 0:
            current_time = time.time()
            self.times[current_time] = Time(current_time)
            for r in self.rates:
                r.add_time(current_time, self.times)
            return 0
        self.sync_file()
        return wait_time
