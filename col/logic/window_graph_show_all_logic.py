#!/usr/bin/env python3

import sys
import os
try:
    myFolder = os.path.split(os.path.realpath(__file__))[0]
    sys.path.append(os.path.join(myFolder, os.path.pardir))
    from windows.window_graph_show_all import WindowGraphShow
    from base.log import Log
    from base.conf import ConfigProcess
    from base.val import GlobalConstValue
except ImportError:
    pass
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QTimer

import pyqtgraph as pg
import os
import pyqtgraph.exporters as ep

import numpy as np
import time

__Author__ = 'Zhao Zeming'
__Version__ = 1.0

class WindowGraphShowLogic(WindowGraphShow):
    signal_pic_save = pyqtSignal(bool)
    signal_file_save = pyqtSignal(bool)
    signal_set_done = pyqtSignal(bool)
    signal_trigger = pyqtSignal(int)
    def __init__(self, conf, log, parent=None, dir_save=None, shared_data_graph=None):
        self.gui_val = GlobalConstValue()
        self.conf = conf
        self.log = log
        self.data_per_line = self.gui_val.gui_show_num_all
        self.parent = parent
        self.shared_data_graph = shared_data_graph
        self.timer_graph  = QTimer()
        self.timer_lcd = QTimer()
        self.judge_close = True
        self.timer_graph.timeout.connect(self.update_graph)
        self.timer_lcd.timeout.connect(self.update_lcd)
        self.lcd_shown = False
        self.lcd_num_show_record = 0
        self.lcd_auto_record = False
        super(WindowGraphShowLogic, self).__init__()

    def show(self, *arg, **kwarg):
        super(WindowGraphShowLogic, self).show(*arg, **kwarg)
        self.judge_close = False
        self.log.debug(self, 'Open Window')

    def initUI(self):
        super(WindowGraphShowLogic, self).initUI()
        self.update_config()
        self.pushbutton_graph_save.clicked.connect(self.graph_save)
        self.pushbutton_data_save.clicked.connect(self.data_save)

    def config_read(self):
        dict_data = self.conf.config_read()['Data']
        self.channel_num = int(dict_data['channel_num'])
        self.restart_auto = int(dict_data['auto_res_able'])
        self.restart_time = int(dict_data['auto_res_time'])
        self.period_time = int(dict_data['set_time'])
        self.set_number = int(dict_data['set_number'])
        self.train_pass_all = self.period_time + (self.set_number - 1)*(self.period_time + self.restart_time)
        self.time_period = self.period_time + self.restart_time
        self.log.debug(self, 'Read Config')

    def isClosed(self):
        return self.judge_close

    def closeEvent(self, e):
        self.stopTimer()
        super(WindowGraphShow, self).closeEvent(e)
        self.judge_close = True
        self.log.debug(self, 'Close Window')

    def graph_save(self):
        self.signal_pic_save.emit(True)
        self.log.debug(self, 'Save Picture')

    def data_save(self):
        self.signal_file_save.emit(True)
        self.log.debug(self, 'Save Data')

    def update_graph(self):
        data = np.frombuffer(self.shared_data_graph.get_obj())
        data = data[:self.data_all_num]
        data = data.reshape(-1, self.channel_num).T
        x_data = np.array(self.data_per_line)
        for i in range(self.channel_num):
            self.list_curve[i].setData(y=data[i, :self.data_per_line] + i + 1, pen=(0x00, 0x00, 0x00))
        time.sleep(0.04)

    def update_lcd(self):
        self.lcd_control()
        self.lcdnumber_countdown.display(self.lcd_time_show)
        self.lcdnumber_countdown_num.display(self.lcd_num_show)

    def startTimer(self, e):
        if e:
            self.timer_lcd.start(100)
        else:
            self.timer_graph.start(20)

    def stopTimer(self):
        self.timer_graph.stop()
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
        show_time = self.gui_val.gui_show_second
        pointspersecond = self.data_per_line // show_time
        self.config_read()
        self.scroll_area_widget.setMinimumSize(798, self.channel_num*12)
        self.scroll_area_widget.setMaximumSize(798, self.channel_num*12)
        self.graph_show.setRange(yRange=[0.3, self.channel_num+0.7], xRange=(-0.01*pointspersecond, (show_time+0.1)*pointspersecond), padding=0)
        self.graph_show.clear()
        self.data_all_num = self.gui_val.gui_show_num_all * self.channel_num
        axis_x = self.graph_show.getAxis('bottom')
        axis_y = self.graph_show.getAxis('left')
        xticks = range(pointspersecond, show_time*pointspersecond + 1, pointspersecond)
        yticks = range(1, self.channel_num+1)
        axis_x.setTicks([[(i, str(i//pointspersecond)) for i in xticks]])
        axis_y.setTicks([[(i, str(i)) for i in yticks]])
        self.graph_show.invertY()
        for i in range(self.channel_num+1):
            self.graph_show.addLine(y=i+0.5, pen='k')
        for i in range(pointspersecond, show_time*pointspersecond, pointspersecond):
            self.graph_show.addLine(x=i, pen='k')
        self.list_curve = []
        for i in range(self.channel_num):
            self.list_curve.append(self.graph_show.plot())
            self.list_curve[i].setClipToView(True)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    config_ini_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, 'config', 'config.ini')
    config_temp_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, '.temp', 'config.ini')
    log = Log(os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, 'log', 'log.out'))
    conf = ConfigProcess(config_ini_path, config_temp_path, log)
    win = WindowGraphShowLogic(conf, log)
    win.show()
    sys.exit(app.exec_())

