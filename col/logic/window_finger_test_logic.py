#!/usr/bin/env python3
from PyQt5.QtCore import (Qt, QSize, QRect, pyqtSlot, QTimer,
                          pyqtSignal)
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QPushButton,
                             QVBoxLayout, QLCDNumber, )

import sys
import os

try:
    myFolder = os.path.split(os.path.realpath(__file__))[0]
    sys.path.append(os.path.join(myFolder, os.path.pardir))
    from windows.window_finger_test import WindowFingerTest
    from base.log import Log
    from base.conf import ConfigProcess
    from base.val import GlobalConstValue
except:
    pass

import numpy as np
import time

class WindowFingerTestLogic(WindowFingerTest):
    """ DocString for WindowFingerTestLogic"""
    signal_set_done = pyqtSignal(bool)
    signal_trigger = pyqtSignal(int)
    def __init__(self, conf, log):
        #@todo: to be defined.
        self.gui_val = GlobalConstValue()
        self.conf = conf
        self.log = log
        self.timer_lcd = QTimer()
        self.timer_lcd.timeout.connect(self.update_lcd)
        self.lcd_shown = False
        self.lcd_num_show_record = 0
        self.lcd_auto_record = False
        self.list_finger_name = ['THUMB', 'INDEX', 'MIDDLE', 'RING', 'LITTLE']
        self.judge_close = True
        super(WindowFingerTestLogic, self).__init__()

    def show(self, *arg, **kwarg):
        """DocString for show"""
        #@todo: to be defined.
        super(WindowFingerTestLogic, self).show(*arg, **kwarg)
        self.judge_close = False
        self.log.debug(self, 'Open Window')

    def initUI(self):
        """DocString for initUI"""
        #@todo: to be defined.
        super(WindowFingerTestLogic, self).initUI()
        self.update_config()
        self.pushbutton_start.clicked.connect(self.action_start)
        self.pushbutton_change_hand.clicked.connect(self.change_hand)
        self.change_hand()

    def config_read(self):
        dict_data = self.conf.config_read()['Data']
        self.restart_auto = int(dict_data['auto_res_able'])
        self.restart_time = int(dict_data['auto_res_time'])
        self.period_time = int(dict_data['set_time'])
        self.set_number = int(dict_data['set_number'])
        self.train_pass_all = self.period_time + (self.set_number - 1)*(self.period_time + self.restart_time)
        self.time_period = self.period_time + self.restart_time
        self.log.debug(self, 'Read Config')

    def isClosed(self):
        return self.judge_close

    def keyReleaseEvent(self, event):
        """DocString for pressKeyEvent"""
        #@todo: to be defined.
		#:event: @todo.
        if event.key() == Qt.Key_Q:
            self.close()
        if event.key() == Qt.Key_C:
            self.change_hand()

    def update_lcd(self):
        self.lcd_control()
        self.lcdnumber_countdown.display(self.lcd_time_show)
        self.lcdnumber_countdown_num.display(self.lcd_num_show)

    def startTimer(self, e):
        if e:
            self.timer_lcd.start(100)

    def stopTimer(self):
        self.timer_lcd.stop()

    def lcd_control(self):
        if self.restart_auto:
            if not self.lcd_shown:
                self.time_start = time.time()
                self.lcd_shown = True
            time_pass = time.time() - self.time_start
            if time_pass > self.train_pass_all:
                self.lcd_time_show = int(time_pass - self.train_pass_all)
                self.lcd_num_show = 0
            else:
                time_pass = int(time_pass)
                lcd_time = (time_pass) % self.time_period
                if lcd_time > self.period_time:
                    self.lcd_time_show = lcd_time - self.period_time + 1
                    if self.lcd_auto_record:
                        self.signal_trigger.emit(1)
                        self.lcd_auto_record = False
                else:
                    self.lcd_time_show = self.period_time - lcd_time
                    self.lcd_auto_record = True
                self.lcd_num_show = (time_pass) // self.time_period + 1
        else:
            if not self.lcd_shown:
                self.time_start = time.time()
                self.lcd_shown = True
            time_pass = time.time() - self.time_start
            if self.set_number > 0:
                if time_pass > self.period_time:
                    self.lcd_shown = False
                    self.set_number -= 1
                    self.lcd_time_show = 0
                    self.timer_lcd.stop()
                else:
                    self.lcd_time_show = int(self.period_time - time_pass)
                    self.lcd_num_show = self.set_number
            else:
                self.lcd_time_show = int(time_pass)
                self.lcd_num_show = 0
        if self.lcd_num_show != self.lcd_num_show_record:
            self.signal_trigger.emit(1)
            self.lcd_num_show_record = self.lcd_num_show
        if self.lcd_num_show == 0:
            self.lcd_num_show = 'ES'

    @pyqtSlot(bool)
    def update_config(self, *arg):
        self.config_read()

    def isClosed(self):
        return self.judge_close

    def closeEvent(self, e):
        self.stopTimer()
        super(WindowFingerTestLogic, self).closeEvent(e)
        self.judge_close = True
        self.log.debug(self, 'Close Window')

    def action_start(self):
        """DocString for runstart"""
        self.startTimer(1)

    def change_value(self, data=''):
        """DocString for change_hand"""
        #@todo: to be defined.
        if data == '':
            self.list_finger_value[0], self.list_finger_value[4] = self.list_finger_value[4], self.list_finger_value[0]
            self.list_finger_value[1], self.list_finger_value[3] = self.list_finger_value[3], self.list_finger_value[1]
        else:
            for i in range(len(data)):
                self.list_finger_value[i] = data[i]

        if self.order_finger:
            for i in range(len(self.list_finger_value)):
                self.list_test_widget[i].setValue(self.list_finger_value[i])
        else:
             for i in range(len(self.list_finger_value)):
                self.list_test_widget[i].setValue(self.list_finger_value[i])

    def change_hand(self):
        """DocString for change_hand"""
        #@todo: to be defined.
        self.order_finger = not self.order_finger
        if self.order_finger:
            for i in range(5):
                self.list_test_widget[i].setText(self.list_finger_name[i], )
        else:
            for i in range(5):
                self.list_test_widget[i].setText(self.list_finger_name[-(i+1)], )

        self.change_value()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    config_ini_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, 'config', 'config.ini')
    config_temp_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, '.temp', 'config.ini')
    log = Log(os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, 'log', 'log.out'))
    conf = ConfigProcess(config_ini_path, config_temp_path, log)
    win = WindowFingerTestLogic(conf, log)
    win.change_value([15, 27, 49, 79, 3])
    win.show()
    sys.exit(app.exec_())


