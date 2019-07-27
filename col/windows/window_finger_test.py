#!/usr/bin/env python3
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QPushButton,
                             QVBoxLayout, QLCDNumber, )
import sys
import os

myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(myFolder, os.path.pardir, 'base'))
from widget_diy import FingerTest

class WindowFingerTest(QWidget):
    """ DocString for WindowFingerTest"""

    def __init__(self, ):
        #@todo: to be defined.
        super(WindowFingerTest, self).__init__()
        self.order_finger = True
        self.list_finger_value = [72, 72, 72, 72, 72]
        self.initUI()

    def initUI(self, ):
        """DocString for initUI"""
        #@todo: to be defined.

        lcd_number_style = 'QLCDNumber{\
                            min-width: 150px;\
                            max-width: 150px;\
                            min-height: 80px;\
                            max-height: 80px;\
                            }'
        pushbutton_style = 'QPushButton{\
                            min-width: 150px;\
                            max-width: 150ox;\
                            min-height: 80px;\
                            max-height: 80px;\
                            }'


        self.setWindowTitle('Test')
        self.setFixedSize(700, 800)

        self.list_test_widget = [FingerTest(), FingerTest(),
                                 FingerTest(), FingerTest(),
                                 FingerTest()]

        size = (100, 775)
        for i in range(len(self.list_finger_value)):
            self.list_test_widget[i].setText('', False)

        for i in range(5):
            self.list_test_widget[i].setSize(size, False)

        layout_main = QHBoxLayout()
        layout_finger_test = QHBoxLayout()
        layout_control = QVBoxLayout()

        for i in range(5):
            layout_finger_test.addWidget(self.list_test_widget[i])

        self.setLayout(layout_main)

        self.lcdnumber_countdown = QLCDNumber()
        self.lcdnumber_countdown.setDigitCount(4)
        self.lcdnumber_countdown.setMode(QLCDNumber.Dec)
        self.lcdnumber_countdown.setSegmentStyle(QLCDNumber.Flat)
        self.lcdnumber_countdown.setStyleSheet(lcd_number_style)
        self.lcdnumber_countdown_num = QLCDNumber()
        self.lcdnumber_countdown_num.setDigitCount(4)
        self.lcdnumber_countdown_num.setMode(QLCDNumber.Dec)
        self.lcdnumber_countdown_num.setSegmentStyle(QLCDNumber.Flat)
        self.lcdnumber_countdown_num.setStyleSheet(lcd_number_style)

        self.pushbutton_change_hand = QPushButton('Change hand')
        self.pushbutton_change_hand.setStyleSheet(pushbutton_style)
        self.pushbutton_start = QPushButton('Start')
        self.pushbutton_start.setStyleSheet(pushbutton_style)

        widget = QWidget()
        widget.setMinimumSize(20, 300)

        layout_control.addWidget(widget)
        layout_control.addWidget(self.lcdnumber_countdown)
        layout_control.addWidget(self.lcdnumber_countdown_num)
        layout_control.addWidget(widget)
        layout_control.addWidget(self.pushbutton_change_hand)
        layout_control.addWidget(self.pushbutton_start)

        layout_main.addLayout(layout_finger_test)
        layout_main.addLayout(layout_control)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = WindowFingerTest()
    win.show()
    sys.exit(app.exec_())

