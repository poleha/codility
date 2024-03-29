import time
from collections import OrderedDict


def measure(func):
    key = func.__name__
    if key not in measure.wrappers:
        measure.timers[key] = 0
        measure.calls[key] = 0

        def wrapper(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            end = time.time()
            measure.timers[key] += end - start
            measure.calls[key] += 1
            return res
        measure.wrappers[key] = wrapper
    return measure.wrappers[key]

measure.timers = OrderedDict()
measure.calls = OrderedDict()
measure.wrappers = OrderedDict()


class MeasureBlock:
    def __init__(self, frag_name):
        self.frag_name = frag_name
        self.timer = 0
        self.calls = 0
        self.start_time = None

    def start(self):
        self.start_time = time.time()
        self.calls += 1

    def end(self):
        e = time.time()
        self.timer += e - self.start_time

    def __str__(self):
        return '{} - {} - {}'.format(self.frag_name, self.timer, self.calls)


#************************************
# Backward compatibility

def create_measure(timers):
    def measure(timer_name = None):
        def dec(func):
            key = timer_name if timer_name else func.__name__
            timers[key] = 0
            def wrapper(*args, **kwargs):
                start = time.time()
                res = func(*args, **kwargs)
                end = time.time()
                timers[key] += end - start
                return res
            return wrapper
        return dec
    return measure