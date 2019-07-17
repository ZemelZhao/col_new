#!/usr/bin/env python3

import sys
import os
import configparser
from PyQt5.QtCore import Qt
try:
    myFolder = os.path.split(os.path.realpath(__file__))[0]
    sys.path.append(os.path.join(myFolder, os.path.pardir))
    from windows.window_setting import WindowOption
    from base.log import Log
    from base.conf import ConfigProcess
except ImportError:
    pass

import time

__Author__ = 'Zhao Zeming'
__Version__ = 1.0

class WindowOptionLogic(WindowOption):
    def __init__(self, conf, log, parent=None):
        self.parent = parent
        self.cache_notch_filter = {50: 0, 60: 1}
        self.cache_bandpass_high = {1: 0, 5: 1, 10: 2, 20: 3}
        self.cache_bandpass_low = {50: 0, 100: 1, 200: 2, 450: 3}
        self.cache_sampling_freq = {250: 0, 500: 1, 1000: 2, 2000: 3}
        self.cache_channel_num = {64: 0, 128: 1, 192: 2}
        self.myFile = os.path.split(os.path.realpath(__file__))[0]
        self.log_path = os.path.join(self.myFile, os.pardir, 'log', 'log.out')
        self.config_ini_path = os.path.join(self.myFile, os.pardir, 'config', 'config.ini')
        self.config_temp_path = os.path.join(self.myFile, os.pardir, '.temp', 'config.ini')
        self.conf = conf
        self.log = log
        super(WindowOptionLogic, self).__init__()
        self.judge_close = True

    def keyReleaseEvent(self, event):
        """DocString for pressKeyEwent"""
        #@todo: to be defined.
        if event.key() == Qt.Key_D:
            self.list_option.setCurrentRow(0)
            self.stack_window.setCurrentIndex(0)

        if event.key() == Qt.Key_P:
            self.list_option.setCurrentRow(1)
            self.stack_window.setCurrentIndex(1)

        if event.key() == Qt.Key_O:
            if self.stack_window.currentIndex() == 1:
                self.tabwidget_page1.setCurrentIndex(1)
            else:
                self.tabwidget_page0.setCurrentIndex(1)

        if event.key() == Qt.Key_I:
            if self.stack_window.currentIndex() == 1:
                self.tabwidget_page1.setCurrentIndex(0)
            else:
                self.tabwidget_page0.setCurrentIndex(0)

        if event.key() == Qt.Key_Return:
            if self.stack_window.currentIndex() == 1:
                self.pushbutton_ok_page1.click()
            else:
                self.pushbutton_ok_page0.click()

        if event.key() == Qt.Key_R:
            if self.stack_window.currentIndex() == 1:
                self.pushbutton_re_page1.click()
            else:
                self.pushbutton_re_page0.click()

        if event.key() == Qt.Key_Q:
            self.close()



    def show(self, *arg, **kwarg):
        """DocString for show"""
        #@todo: to be defined.
        super(WindowOptionLogic, self).show(*arg, **kwarg)
        self.judge_close = False
        self.log.debug(self, 'Open Window')

    def closeEvent(self, *arg, **kwarg):
        """DocString for closeEvent"""
        #@todo: to be defined.
        super(WindowOptionLogic, self).closeEvent(*arg, **kwarg)
        self.judge_close = True
        self.log.debug(self, 'Close Window')

    def isClosed(self):
        """DocString for isClosed"""
        #@todo: to be defined.

        return self.judge_close

    def initUI(self):
        super(WindowOptionLogic, self).initUI()
        self.config_ini_read()
        self.pushbutton_ok_page0.clicked.connect(self.action_pushbutton_ok_page0)
        self.pushbutton_re_page0.clicked.connect(self.action_pushbutton_re_page0)
        self.pushbutton_de_page0.clicked.connect(self.action_pushbutton_de_page0)
        self.pushbutton_ok_page1.clicked.connect(self.action_pushbutton_ok_page1)
        self.pushbutton_re_page1.clicked.connect(self.action_pushbutton_re_page1)
        self.pushbutton_de_page1.clicked.connect(self.action_pushbutton_de_page1)

        self.checkbox_notch_filter.stateChanged.connect(self.action_notch_filter_change)
        self.checkbox_bandpass_filter.stateChanged.connect(self.action_bandpass_filter_change)
        self.radiobutton_restart_auto.toggled.connect(self.action_auto_press_change)
        self.radiobutton_users_gender_secret_page1.setChecked(True)

        self.display_initial()

    def config_ini_read(self):
        self.dict_conf = self.conf.config_read_ini()

    def display_initial(self):
        self.dict_conf = self.conf.config_read()
        dict_filter = self.dict_conf['Filter']
        dict_data = self.dict_conf['Data']
        dict_sock = self.dict_conf['Socket']
        self.checkbox_notch_filter.setChecked(int(dict_filter['filter_notch_able']))
        self.checkbox_bandpass_filter.setChecked(int(dict_filter['filter_band_able']))
        self.combobox_notch_filter.setCurrentIndex(self.cache_notch_filter[int(dict_filter['filter_notch'])])
        self.combobox_bandpass_high.setCurrentIndex(self.cache_bandpass_high[int(dict_filter['filter_band_high'])])
        self.combobox_bandpass_low.setCurrentIndex(self.cache_bandpass_low[int(dict_filter['filter_band_low'])])
        self.combobox_sampling_freq.setCurrentIndex(self.cache_sampling_freq[int(dict_filter['sampling_freq'])])

        self.combobox_channel_num.setCurrentIndex(self.cache_channel_num[int(dict_data['channel_num'])])
        self.spinbox_set_num.setValue(int(dict_data['set_number']))
        self.spinbox_set_time.setValue(int(dict_data['set_time']))
        self.spinbox_restart_auto.setValue(int(dict_data['auto_res_time']))
        self.radiobutton_restart_auto.setChecked(int(dict_data['auto_res_able']))
        self.radiobutton_restart_press.setChecked(not int(dict_data['auto_res_able']))
        self.combobox_filetype_save.setCurrentIndex(int(dict_data['filetype_save']))

        self.lineedit_tcp_address.setText(dict_sock['tcp_address'])
        self.lineedit_tcp_port.setText(dict_sock['tcp_port'])

        self.combobox_notch_filter.setEnabled(self.checkbox_notch_filter.isChecked())
        self.combobox_bandpass_high.setEnabled(self.checkbox_bandpass_filter.isChecked())
        self.combobox_bandpass_low.setEnabled(self.checkbox_bandpass_filter.isChecked())
        self.spinbox_restart_auto.setEnabled(self.radiobutton_restart_auto.isChecked())

    def action_pushbutton_ok_page0(self):
        self.close()

    def action_pushbutton_de_page0(self):
        self.close()

    def action_pushbutton_ok_page1(self):
        self.dict_conf['Filter']['filter_notch_able'] = str(int(self.checkbox_notch_filter.isChecked()))
        self.dict_conf['Filter']['filter_band_able'] = int(self.checkbox_bandpass_filter.isChecked())
        self.dict_conf['Filter']['filter_notch'] = int(self.combobox_notch_filter.currentText())
        self.dict_conf['Filter']['filter_band_high'] = int(self.combobox_bandpass_high.currentText())
        self.dict_conf['Filter']['filter_band_low'] = int(self.combobox_bandpass_low.currentText())
        self.dict_conf['Filter']['sampling_freq'] = int(self.combobox_sampling_freq.currentText())

        self.dict_conf['Data']['channel_num'] = int(self.combobox_channel_num.currentText())
        self.dict_conf['Data']['set_number'] = int(self.spinbox_set_num.value())
        self.dict_conf['Data']['set_time'] = int(self.spinbox_set_time.value())
        self.dict_conf['Data']['auto_res_able'] = int(self.radiobutton_restart_auto.isChecked())
        self.dict_conf['Data']['auto_res_time'] = int(self.spinbox_restart_auto.value())
        self.dict_conf['Data']['filetype_save'] = int(self.combobox_filetype_save.currentIndex())

        self.dict_conf['Socket']['tcp_address'] = self.lineedit_tcp_address.text()
        self.dict_conf['Socket']['tcp_port'] = self.lineedit_tcp_port.text()

        self.conf.config_write(self.dict_conf)
        self.log.debug(self, 'Close Window Saved')

        self.close()

    def action_pushbutton_de_page1(self):
        self.log.debug(self, 'Close Window without Save')
        self.close()

    def action_pushbutton_re_page0(self):
        pass

    def action_pushbutton_re_page1(self):
        self.dict_conf = self.conf.config_read()
        self.display_initial()
        self.log.debug(self, 'Reset All Config')

    def action_notch_filter_change(self):
        self.combobox_notch_filter.setEnabled(self.checkbox_notch_filter.isChecked())

    def action_bandpass_filter_change(self):
        self.combobox_bandpass_high.setEnabled(self.checkbox_bandpass_filter.isChecked())
        self.combobox_bandpass_low.setEnabled(self.checkbox_bandpass_filter.isChecked())

    def action_auto_press_change(self):
        self.spinbox_restart_auto.setEnabled(self.radiobutton_restart_auto.isChecked())


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    config_ini_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, 'config', 'config.ini')
    config_temp_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, '.temp', 'config.ini')
    log = Log(os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, 'log', 'log.out'))
    conf = ConfigProcess(config_ini_path, config_temp_path, log)

    app = QApplication(sys.argv)
    win = WindowOptionLogic(conf, log)
    win.show()
    sys.exit(app.exec_())
