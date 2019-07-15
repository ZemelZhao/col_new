from log import Log

class Fuck(object):
    """ DocString for Fuck"""

    def __init__(self, name):
        #@todo: to be defined.
        #:name: @todo.

        self.name = name

        log = Log(self.name)

        log.error(self, 'fuck')

if __name__ == '__main__':
    fu = Fuck('log.out')
