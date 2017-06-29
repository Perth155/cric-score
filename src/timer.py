'''
A thread that executes a function after a specified interval has passed.
'''

from threading import Timer

class RepeatTimer(object):
    def __init__(self, interval, function, *args):
        self._timer     = None
        self.function   = function
        self.interval   = interval
        self.args       = args
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
