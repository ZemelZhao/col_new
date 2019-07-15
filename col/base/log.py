import glob
import logging
import logging.handlers as lh
import time
import os

class Log(object):
    """ DocString for Log"""

    def __init__(self, log_file_name, loglevel='debug'):
        #@todo: to be defined.
        #:log_file_name: @todo.
		#:loglevel: @todo.

        self.list_log_level = ['critical', 'error', 'warning',
                               'info', 'debug', 'unset']
        self.log_file_name = str(log_file_name)
        self.loglevel = loglevel.lower()
        self.log = logging.getLogger('MyLogger')
        try:
            index_log_level = self.list_log_level.index(self.loglevel)
        except:
            index_log_level = 0
            #raise Warning('Logging Level Given is wrong')
        finally:
            if index_log_level == 0:
                self.log.setLevel(logging.CRITICAL)
            elif index_log_level == 1:
                self.log.setLevel(logging.ERROR)
            elif index_log_level == 2:
                self.log.setLevel(logging.WARNING)
            elif index_log_level == 3:
                self.log.setLevel(logging.INFO)
            elif index_log_level == 4:
                self.log.setLevel(logging.DEBUG)
            else:
                self.log.setLevel(logging.UNSET)

        self.log_handler = lh.RotatingFileHandler(
            self.log_file_name,
            maxBytes=100000,
            backupCount=5,
        )
        self.log.addHandler(self.log_handler)

    def crit(self, run_class, data):
        """DocString for critical"""
        #@todo: to be defined.
		#:run_class: @todo.
		#:data: @todo.
        self.log.critical('[%s][CRITICAL][%s] %s' % (self.time_display(time.gmtime()), run_class.__class__.__name__, data))

    def error(self, run_class, data):
        """DocString for error"""
        #@todo: to be defined.
		#:run_class: @todo.
		#:data: @todo.
        self.log.error('[%s][ERROR][%s] %s' % (self.time_display(time.gmtime()), run_class.__class__.__name__, data))

    def warning(self, run_class, data):
        """DocString for warning"""
        #@todo: to be defined.
		#:run_class: @todo.
		#:data: @todo.
        self.log.warning('[%s][WARNING][%s] %s' % (self.time_display(time.gmtime()), run_class.__class__.__name__, data))

    def info(self, run_class, data):
        """DocString for info"""
        #@todo: to be defined.
		#:run_class: @todo.
		#:data: @todo.
        self.log.info('[%s][INFO][%s] %s' % (self.time_display(time.gmtime()), run_class.__class__.__name__, data))

    def debug(self, run_class, data):
        """DocString for debug"""
        #@todo: to be defined.
		#:run_class: @todo.
		#:data: @todop
        self.log.debug('[%s][DEBUG][%s] %s' % (self.time_display(time.gmtime()), run_class.__class__.__name__, data))

    def unset(self, run_class, data):
        """DocString for unset"""
        #@todo: to be defined.
		#:run_class: @todo.
		#:data: @todop
        self.log.unset('[%s][UNSET][%s] %s' % (self.time_display(time.gmtime()), run_class.__class__.__name__, data))

    def time_display(self, data):
        """DocString for run"""
        #@todo: to be defined.
		#:data: @todo.
        return '%04d-%02d-%02d %02d:%02d:%02d' % (data.tm_year, data.tm_mon, data.tm_mday,
                                            data.tm_hour, data.tm_min, data.tm_sec)



if __name__ == '__main__':
    log = Log(1, 'fukc')


