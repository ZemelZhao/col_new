#!/usr/bin/env python3

from threading import Timer, Event

class RTimer(Timer):
    """ DocString for RTimer"""

    def __init__(self, interval, function, args=[], kwargs={}):
        #@todo: to be defined.
        #:interval: @todo.
		#:function: @todo.
		#:args=[]: @todo.
		#:kwargs={}: @todo.
        super(RTimer, self).__init__(args, kwargs)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.need = True
        self.finished = Event()

    def run(self):
        """DocString for run"""
        #@todo: to be defined.
        while self.need:
            self.finished.wait(self.interval)
            if not self.finished.is_set():
                self.function(*self.args, **self.kwargs)

    def cancel(self):
        """DocString for cancel"""
        #@todo: to be defined.
        self.need = False


def hello():
    """DocString for hello"""
    #@todo: to be defined.

    print('here')


if __name__ == '__main__':
    t = RTimer(1, hello)
    t.start()


