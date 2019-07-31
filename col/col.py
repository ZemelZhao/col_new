#!/usr/bin/env python3

import sys
import os
import multiprocessing as mp
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QMessageBox, QMdiSubWindow, QMdiArea
from PyQt5.QtGui import QCloseEvent
try:
    from windows.window_main import WindowMain
    from logic.window_graph_show_all_logic import WindowGraphShowLogic
    from logic.window_setting_logic import WindowOptionLogic
    from logic.window_tinker_logic import WindowHelpLogic, WindowAboutLogic
    from logic.window_finger_test_logic import WindowFingerTestLogic
    from base.log import Log
    from base.conf import ConfigProcess
    from base.timer import RTimer
    from base.val import GlobalConstValue as gcv
    from cal.cal import Cal
    from cal.save import Save
except ImportError:
    pass
import pyqtgraph as pg
import pyqtgraph.exporters as ep
import ctypes
import csv
import numpy as np
import socket
import time
import tempfile

__Author__ = 'Zhao Zeming'
__Version__ = 1.0

class MainWindow(WindowMain):
    signal_state = pyqtSignal(QCloseEvent)
    signal_config_refresh = pyqtSignal(bool)
    signal_pic_save = pyqtSignal([pg.graphicsItems.PlotItem.PlotItem, str])
    signal_data_process = pyqtSignal(int)
    signal_start_refresh = pyqtSignal(bool)
    def __init__(self, conf, log, shared_data_graph, shared_tcp_ip_stat, save_name):
        super(MainWindow, self).__init__()
        self.setFixedSize(self.width(), self.height())
        self.conf = conf
        self.log = log
        self.myFolder = os.path.split(os.path.realpath(__file__))[0]

        self.save_name = save_name
        self.dir_save = os.path.join(self.myFolder, 'save', self.save_name)
        self.shared_data_graph = shared_data_graph
        self.shared_tcp_ip_stat = shared_tcp_ip_stat
        self.value_record_stat = self.shared_tcp_ip_stat.value
        self.initial_setting()
        self.timer_clear_status = QTimer()
        self.timer_stat_monit = QTimer()
        self.timer_stat_monit.timeout.connect(self.show_warning)
        self.timer_clear_status.timeout.connect(self.slot_status_bar_clear)
        self.timer_stat_monit.start(1000)
        self.start = False

        self.judge_collect_stat = True

        self.timer_tcp_monit = QTimer()
        self.timer_tcp_monit.timeout.connect(self.tcp_ip_monit)
        self.timer_tcp_monit.start(1000)

        self.started = False

    def keyPressEvent(self, event):
        """DocString for KeyPressEvent"""
        #@todo: to be defined.
        if event.key() == Qt.Key_T:
            self.slot_make_trigger()
        if event.key() == Qt.Key_S:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.file_save()
            else:
                self.start_restart()
        if event.key() == Qt.Key_G:
            try:
                if self.window_graph_show.isClosed():
                    self.graph_show()
                else:
                    self.pic_save()
            except:
                self.graph_show()
        if event.key() == Qt.Key_O:
            self.main_option()

        if event.key() == Qt.Key_Q:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.close()
            else:
                try:
                    judge = False
                    try:
                        if not self.window_graph_show.isClosed():
                            self.window_graph_show.close()
                            judge = True
                    except:
                        pass
                    try:
                        if not self.window_finger_test.isClosed():
                            self.window_finger_test.close()
                            judge = True
                    except:
                        pass
                    if judge:
                        self.mdi.close()
                except:
                    print('fuckhere')
        if event.key() == Qt.Key_A:
            self.start_analysis()
        if event.key() == Qt.Key_F:
            try:
                if self.window_finger_test.isClosed():
                    self.finger_test()
            except:
                self.finger_test()

    def initial_setting(self):
        self.slot_refresh_config()

    def closeEvent(self, item):
        self.signal_state.emit(item)

    def main_option(self):
        if not self.start:
            self.window_main_option = WindowOptionLogic(self.conf, self.log, self)
            if self.window_main_option.isClosed():
                self.signal_state.connect(self.window_main_option.close)
                self.window_main_option.pushbutton_ok_page1.clicked.connect(self.slot_refresh_config)
                self.window_main_option.show()



    def graph_show(self):
        dict_conf = self.conf.config_read()
        test_judge = int(dict_conf['Test']['test'])
        if test_judge:
            return False
        try:
            if not self.window_finger_test.isClosed():
                self.window_finger_test.close()
        except:
            pass
        try:
            if self.window_graph_show.isClosed():
                judge = True
            else:
                judge = False
        except:
            judge = True
        finally:
            if judge:
                self.window_graph_show = WindowGraphShowLogic(self.conf, self.log, self, self.dir_save, self.shared_data_graph)
                self.window_graph_show.startTimer(0)
                sub = QMdiSubWindow()
                sub.setWidget(self.window_graph_show)
                self.mdi = QMdiArea()
                self.setCentralWidget(self.mdi)
                self.mdi.addSubWindow(sub)
                self.signal_config_refresh.connect(self.window_graph_show.update_config)
                self.signal_start_refresh.connect(self.window_graph_show.update_lcd)
                self.window_graph_show.signal_file_save.connect(self.file_save)
                self.window_graph_show.signal_pic_save.connect(self.pic_save)
                self.window_graph_show.signal_trigger.connect(self.slot_graph_emit)
                #self.window_graph_show.signal_trigger.connect(self.)
                self.window_graph_show.show()

    def finger_test(self):
        """DocString for finger_test"""
        #@todo: to be defined.
        dict_conf = self.conf.config_read()
        judge_test = int(dict_conf['Test']['test'])
        if not judge_test:
            return False
        try:
            if not self.window_graph_show.isClosed():
                self.window_graph_show.close()
        except:
            pass
        try:
            if self.window_finger_test.isClosed():
                judge = True
            else:
                judge = False
        except:
            judge = True
        finally:
            if judge:
                self.window_finger_test = WindowFingerTestLogic(self.conf, self.log)
                self.window_finger_test.startTimer(0)
                sub = QMdiSubWindow()
                sub.setWidget(self.window_finger_test)
                self.mdi = QMdiArea()
                self.setCentralWidget(self.mdi)
                self.mdi.addSubWindow(sub)
                self.signal_start_refresh.connect(self.window_finger_test.update_lcd)
                self.window_finger_test.show()

    def prog_about(self):
        self.window_prog_about = WindowAboutLogic(self.log, self)
        self.signal_state.connect(self.window_prog_about.close)
        self.window_prog_about.show()

    def prog_help(self):
        self.window_prog_help = WindowHelpLogic(self.log, self)
        self.signal_state.connect(self.window_prog_help.close)
        self.window_prog_help.show()

    def pic_save(self):
        self.signal_data_process.emit(2)
        self.slot_status_bar_changed('Picture Saved Successfully')

    def file_save(self):
        """DocString for file_save"""
        self.signal_data_process.emit(3)
        self.close()

    def start_restart(self):
        """DocString for start_restart"""
        #@todo: to be defined.
        self.start = True
        self.slot_status_bar_changed('Start Record Data')
        self.window_graph_show.startTimer(1)
        self.window_finger_test.startTimer(1)
        self.signal_start_refresh.emit(True)
        dict_config = self.conf.config_read()
        bool_auto_start = int(dict_config['Data']['auto_res_able'])
        if self.started:
            if not bool_auto_start:
                self.signal_data_process.emit(1)
        else:
            self.started = True
            self.signal_data_process.emit(1)

    def start_analysis(self):
        self.slot_status_bar_changed('Waiting...')
        self.file_save()

    def slot_make_trigger(self):
        """DocString for make_trigger"""
        #@todo: to be defined.
        self.signal_data_process.emit(4)
        self.slot_status_bar_changed('Tiggered')

    def slot_refresh_config(self):
        dict_config = self.conf.config_read()
        self.channel_num = int(dict_config['Data']['channel_num'])
        self.signal_config_refresh.emit(True)

    @pyqtSlot(str)
    def slot_status_bar_changed(self, e):
        self.statusBar().showMessage(e)
        self.timer_clear_status.start(1500)

    @pyqtSlot(int)
    def slot_graph_emit(self, e):
        """DocString for slot_graph_emit"""
        #@todo: to be defined.
        self.signal_data_process.emit(e)


    def slot_status_bar_clear(self):
        self.statusBar().clearMessage()
        self.timer_clear_status.stop()

    def tcp_ip_monit(self):
        """DocString for tcp_ip_monit"""
        #@todo: to be defined.
        if self.shared_tcp_ip_stat.value != 1:
            self.file_save()


    def show_warning(self):
        """DocString for show_warning"""
        #@todo: to be defined.
        if self.shared_tcp_ip_stat.value == self.value_record_stat:
            return 0
        if self.shared_tcp_ip_stat.value == 1:
            self.slot_status_bar_changed('TCP CONNECTED')
            self.value_record_stat = self.shared_tcp_ip_stat.value
        elif self.shared_tcp_ip_stat.value == -1:
            self.slot_status_bar_changed('TCP DISCONNECT')
            self.close()
        else:
            pass

class MainCom(QObject, mp.Process):
    state_tcp_ip = pyqtSignal(int)
    def __init__(self, conf, log, shared_data_graph,
                 config_status_change, status_change,
                 data_save, shared_tcp_ip_stat,
                 save_name, local_tcp_ip):
        super(MainCom, self).__init__()
        self.save_name = save_name
        self.shared_data_graph = shared_data_graph
        self.not_change  = config_status_change
        self.start_ornot = status_change
        self.data_save = data_save
        self.conf = conf
        self.log = log
        self.cal = Cal(self.conf, self.log)
        self.global_val = gcv()
        self.data_per_line = self.global_val.gui_show_num_all
        self.data_show_second = self.global_val.gui_show_second
        self.shared_tcp_ip_stat = shared_tcp_ip_stat
        self.temp_file = tempfile.TemporaryFile()
        self.flag = gcv.flag_trigger
        self.new = True
        self.iter_send = 1
        self.cache_data = []
        self.judge_tcp_ip = local_tcp_ip
        self.path_dir_save = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'save')
        self.path_dir_save_name = os.path.join(self.path_dir_save, self.save_name)

        self.timer_tcp_ip = RTimer(1, self.tcp_ip_monit)
        self.timer_tcp_ip.start()

    def tcp_ip_monit(self):
        """DocString for tcp_ip_monit"""
        #@todo: to be defined.
        if self.judge_tcp_ip.value:
            self.shared_tcp_ip_stat.value = 1
        else:
            self.shared_tcp_ip_stat.value = -1
        self.judge_tcp_ip.value = False

    def cal_tcp_ip_bag(self, freq, channel_num):
        num_section = channel_num*16 // 8 + 6
        freq_max = freq // 250 * 3
        if num_section * freq_max >= 1448:
            return num_section*(1448 // num_section)
        else:
            return num_section*freq_max

    def run(self):
        data_clear = 256*self.data_per_line*[0]
        show_freq = 250
        graph_filter = False
        while True:
            time.sleep(0.001)
            self.not_change.value = True
            self.shared_data_graph[:] = data_clear[:]
            dict_conf = self.conf.config_read()
            channel_num = int(dict_conf['Data']['channel_num'])
            freq_sample = int(dict_conf['Filter']['sampling_freq'])
            num_bag = self.cal_tcp_ip_bag(freq_sample, channel_num)
            address = (dict_conf['Socket']['tcp_address'], int(dict_conf['Socket']['tcp_port']))
            upload_config = self.cal.change_status(test=not(graph_filter), hardware_filter=False, command_default=True)
            cache_max_length = 5*channel_num*show_freq*self.data_show_second
            cache_min_length = channel_num*show_freq*self.data_show_second
            self.cache_data = np.array(cache_min_length*[0])
            iter_list = np.linspace(0, show_freq*self.data_show_second-1, self.data_per_line, dtype=np.int)
            iter_send = self.iter_send
            num_show = channel_num * self.data_per_line
            self.temp_file.write(self.flag[4])
            if self.new:
                self.new = False
            else:
                self.sock.close()
                time.sleep(0.4)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_judge = False
            try:
                self.sock.connect(address)
                self.shared_tcp_ip_stat.value = 1
            except:
                temp_judge = True
                self.shared_tcp_ip_stat.value = -1
            if temp_judge:
                continue
            self.sock.sendall(upload_config)
            temp_data = b''
            self.iter_num_ini = 1
            iter_num = self.iter_num_ini
            while self.not_change.value:
                data = self.sock.recv(num_bag)
                self.judge_tcp_ip.value = True
                if self.data_save.value:
                    self.temp_file.write(self.flag[self.data_save.value-1])
                    self.data_save.value = 0
                    self.temp_file.write(temp_data)
                    temp_data = b''
                    iter_num = self.iter_num_ini
                if iter_num == 0:
                    temp_data += data
                    iter_num = self.iter_num_ini
                    self.temp_file.write(temp_data)
                    temp_data = b''
                else:
                    temp_data += data
                    iter_num -= 1
                data = self.cal.run(data)
                self.cache_data = np.hstack((self.cache_data, data))
                data_show = self.cache_data[-cache_min_length : ]
                if len(self.cache_data) > cache_max_length:
                    self.cache_data = self.cache_data[-cache_min_length : ]
                if iter_send > 0:
                    iter_send -= 1
                else:
                    iter_send = self.iter_send
                    data_show = self.cache_data[ -cache_min_length : ]
                    data_show = data_show.reshape(-1, channel_num)
                    data_show = data_show[iter_list, :].reshape(1, -1)
                    data_show = data_show[0]

                    if graph_filter:
                        rule_max = 200
                        rule_min = 0
                        line = 0

                        data_show[np.abs(data_show)>(line+rule_max)] = 0
                        data_show[np.abs(data_show)<(line+rule_min)] = 0
                        data_show = -np.abs(data_show -line) / 100
                    else:
                        data_show = (data_show-32768)/2000
                        #data_show = self.tick_data(data_show)
                    try:
                        self.shared_data_graph[: num_show] = data_show[:]
                    except ValueError:
                        print('fuck')
                time.sleep(0.0001)

    def statusChange(self):
        self.not_change.value = False

    def make_file_save(self, ):
        """DocString for make_file_save"""
        #@todo: to be defined.
        try:
            dict_res = self.conf.config_read()
            save_type = int(dict_res['Data']['filetype_save'])
            self.temp_file.seek(0)
            data = self.temp_file.read()
            self.save_all = Save(self.conf, self.log, self.path_dir_save_name, self.path_dir_save_name,
                                save_loc=1, filt=1, save_type=save_type)
            self.save_all.run(data)
            self.log.info(self, 'Save Done')
        except:
            self.log.warning(self, 'Save Failed')

    def graph_stat_change(self, e):
        """DocString for graph_stat_change"""
        #@todo: to be defined.
		#:e: @todo.
        if e == 1:
            if self.data_save.value == 0:
                self.data_save.value = 1
        if e == 2:
            if self.data_save.value == 0:
                self.data_save.value = 2
        if e == 3:
            if self.data_save.value == 0:
                self.data_save.value = 3
        if e == 4:
            if self.data_save.value == 0:
                self.data_save.value = 4

    def closeEvent(self, e):
        if self.data_save.value == 3:
            self.make_file_save()
        self.timer_tcp_ip.cancel()
        self.terminate()

class ProcessMonitor(QObject, mp.Process):
    def __init__(self):
        super(ProcessMonitor, self).__init__()

    def run(self):
        while True:
            time.sleep(0.5)

    def closeEvent(self, e):
        self.terminate()

class ProcessSave(QObject, mp.Process):
    signal_state_save = pyqtSignal(str)
    def __init__(self, queue):
        super(ProcessSave, self).__init__()
        self.list_action = mp.Manager().list()
        self.graph_no = 0

    def run(self):
        while True:
            time.sleep(5)

    def closeEvent(self, e):
        self.terminate()

    @pyqtSlot(pg.graphicsItems.PlotItem.PlotItem, str)
    def save_pic(self, e0, e1):
        try:
            exporter = ep.ImageExporter(e0.plotItem)
            if exporter.parameters()['height'] < 800:
                exporter.parameters()['height'] = 800
            exporter.export(os.path.join(e1, 'temp%d.png'% self.graph_no))
            self.graph_no += 1
            self.signal_state_save.emit('Picture Saved Successfully')
        except:
            self.signal_state_save.emit('Picture Saved Failed')

if __name__ == '__main__': # Entry
    from PyQt5.QtWidgets import QApplication
    val = gcv()
    shared_data_graph = mp.Array('d', np.array(256*val.gui_show_num_all*[0]))
    shared_config_change = mp.Value('b', False)
    shared_status_change = mp.Value('b', False)
    shared_data_save = mp.Value('i', 0)
    shared_tcp_ip_status = mp.Value('i', 0)
    shared_show_graph_filter = mp.Value('b', False)
    local_com_tcp_ip = mp.Value('b', False)
    time_cache = time.localtime(time.time())
    save_name = '%4d%02d%02d%02d%02d%02d' % (time_cache[0], time_cache[1], time_cache[2],
                                            time_cache[3], time_cache[4], time_cache[5])

    queue_save = mp.Queue(maxsize=100)

    config_ini_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'config', 'config.ini')
    config_temp_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], '.temp', 'config.ini')
    log = Log(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'log', 'log.out'))
    conf = ConfigProcess(config_ini_path, config_temp_path, log)

    com = MainCom(conf, log, shared_data_graph, shared_config_change,
                  shared_status_change, shared_data_save,
                  shared_tcp_ip_status, save_name, local_com_tcp_ip)
    mon = ProcessMonitor()
    sav = ProcessSave(queue_save)
    app = QApplication(sys.argv)
    win = MainWindow(conf, log, shared_data_graph, shared_tcp_ip_status, save_name)

    win.signal_state.connect(com.closeEvent)
    win.signal_state.connect(mon.closeEvent)
    win.signal_state.connect(sav.closeEvent)
    win.signal_pic_save.connect(sav.save_pic)
    win.signal_data_process.connect(com.graph_stat_change)
    win.signal_config_refresh.connect(com.statusChange)
    sav.signal_state_save.connect(win.slot_status_bar_changed)

    win.show()
    com.start()
    mon.start()
    sav.start()
    sys.exit(app.exec_())
