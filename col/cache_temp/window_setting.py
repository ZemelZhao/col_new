#!/usr/bin/env python3
# encoding: utf-8
__author__ = 'Zemel Zhao'

from PyQt5.QtCore import Qt, QSize, QRect, QDate, QTime
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import (QWidget, QListWidget, QStackedWidget, QHBoxLayout,
                             QListWidgetItem, QLabel, QPushButton, QTabWidget,
                             QLineEdit, QRadioButton, QTextEdit, QVBoxLayout,
                             QGroupBox, QComboBox, QCheckBox, QSpinBox, QFrame,
                             QTimeEdit, QDateEdit)

class WindowOption(QWidget):
    """ DocString for WindowOption"""

    def __init__(self, ):
        #@todo: to be defined.
        super(WindowOption, self).__init__()
        self.stylesheet_list = "QListWidget{\
                                min-width:120px;\
                                max-width:120px;\
                                color:white;\
                                background:grey;}"
        self.stylesheet_groupbox = "QGroupBox{\
                                    border:None;}"
        self.initUI()

    def initUI(self):
        """DocString for initUI"""
        #@todo: to be defined.
        """# Global Widget """
        self.setWindowTitle('Option')
        self.setFixedSize(800, 450)

        self.list_option = QListWidget(self)
        self.stack_window = QStackedWidget(self)
        self.set_list_option()
        self.set_stack_window()
        self.set_layout()

    def set_list_option(self):
        """DocString for set_list_option"""
        #@todo: to be defined.
        self.list_option.setStyleSheet(self.stylesheet_list)
        self.list_option.setFrameShape(QListWidget.NoFrame)
        self.list_option.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_option.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_option.currentRowChanged.connect(self.stack_window.setCurrentIndex)

        font = QFont()
        font.setFamily('MonoxLight')
        font.setPointSize(20)

        item_lite = QListWidgetItem()
        item_lite.setFont(font)
        item_lite.setText('LITE')
        item_lite.setSizeHint(QSize(0, 60))
        item_lite.setTextAlignment(Qt.AlignCenter)
        self.list_option.addItem(item_lite)

        item_pro = QListWidgetItem()
        item_pro.setFont(font)
        item_pro.setText('PRO')
        item_pro.setSizeHint(QSize(0, 60))
        item_pro.setTextAlignment(Qt.AlignCenter)
        self.list_option.addItem(item_pro)

    def set_stack_window(self):
        """DocString for set_stack_window"""
        #@todo: to be defined.
        self.page_lite = QWidget()
        self.tab_widget_lite = QTabWidget(self.page_lite)
        self.tab_page_lite_info = QWidget(self.page_lite)
        self.tab_page_lite_opt = QWidget(self.page_lite)
        self.tab_widget_lite.addTab(self.tab_page_lite_info, 'Info')
        self.tab_widget_lite.addTab(self.tab_page_lite_opt, 'Option')

        self.page_pro = QWidget()
        self.tab_widget_pro = QTabWidget(self.page_pro)
        self.tab_page_pro_info = QWidget(self.page_pro)
        self.tab_page_pro_opt = QWidget(self.page_pro)
        self.tab_widget_pro.addTab(self.tab_page_pro_info, 'Info')
        self.tab_widget_pro.addTab(self.tab_page_pro_opt, 'Option')

        self.set_page_pro_info()
        self.set_page_pro_opt()
        self.set_page_lite_info()
        self.set_page_lite_opt()

        self.button_ok_lite = QPushButton('&Ok')
        self.button_re_lite = QPushButton('Reset')
        self.button_de_lite = QPushButton('Cancel')

        self.button_ok_pro = QPushButton('&Ok')
        self.button_re_pro = QPushButton('Reset')
        self.button_de_pro = QPushButton('Cancel')

        groupbox_button_lite = QGroupBox()
        groupbox_button_pro = QGroupBox()

        layout_groupbox_button_lite = QHBoxLayout(groupbox_button_lite)
        layout_groupbox_button_pro = QHBoxLayout(groupbox_button_pro)

        layout_groupbox_button_lite.addWidget(self.button_ok_lite)
        layout_groupbox_button_lite.addWidget(self.button_re_lite)
        layout_groupbox_button_lite.addWidget(self.button_de_lite)

        layout_groupbox_button_pro.addWidget(self.button_ok_pro)
        layout_groupbox_button_pro.addWidget(self.button_re_pro)
        layout_groupbox_button_pro.addWidget(self.button_de_pro)

        groupbox_button_lite.setLayout(layout_groupbox_button_lite)
        groupbox_button_pro.setLayout(layout_groupbox_button_pro)

        self.stack_window.addWidget(self.page_lite)
        self.stack_window.addWidget(self.page_pro)

    def set_page_pro_info(self):
        """DocString for set_page_lite_info"""
        #@todo: to be defined.
        font_pro_info = QFont()
        font_pro_info.setFamily('MonoxLight')
        font_pro_info.setPointSize(12)
        font_pro_info_bold = QFont()
        font_pro_info_bold.setFamily('MonoxRegular Bold')
        font_pro_info_bold.setPointSize(12)

        self.label_date_pro = QLabel('Date      ')
        self.label_time_pro = QLabel('Time      ')
        self.label_loc_pro = QLabel('Location  ')
        self.label_name_pro = QLabel('Name      ')
        self.label_note_pro = QLabel('Note')

        self.label_date_pro.setFont(font_pro_info)
        self.label_time_pro.setFont(font_pro_info)
        self.label_loc_pro.setFont(font_pro_info)
        self.label_name_pro.setFont(font_pro_info)
        self.label_note_pro.setFont(font_pro_info)
        self.label_gender_pro = QLabel('Gender')
        self.label_gender_pro.setFont(font_pro_info_bold)

        self.dateedit_date_pro = QDateEdit(QDate.currentDate())
        self.timeedit_time_pro = QTimeEdit(QTime.currentTime())
        self.lineedit_loc_pro = QLineEdit('Mars')
        self.lineedit_name_pro = QLineEdit('Object')
        self.radiobutton_users_gender_male_pro = QRadioButton('Male')
        self.radiobutton_users_gender_female_pro = QRadioButton('Female')
        self.radiobutton_users_gender_secret_pro = QRadioButton('Secret')
        self.textedit_note_pro = QTextEdit('Pro')

        self.dateedit_date_pro.setDisplayFormat('yyyy/MM/dd')
        self.dateedit_date_pro.setCalendarPopup(True)
        self.dateedit_date_pro.setFont(font_pro_info)
        self.timeedit_time_pro.setDisplayFormat('HH : mm')
        self.timeedit_time_pro.setFont(font_pro_info)
        self.lineedit_loc_pro.setFont(font_pro_info)
        self.lineedit_name_pro.setFont(font_pro_info)
        self.textedit_note_pro.setFont(font_pro_info)

    def set_page_pro_opt(self):
        """DocString for set_page_pro_opt"""
        #@todo: to be defined.

        pass

    def set_page_lite_info(self):
        """DocString for set_page_lite_info"""
        #@todo: to be defined.
        font_lite_info = QFont()
        font_lite_info.setFamily('MonoxLight')
        font_lite_info.setPointSize(12)
        font_lite_info_bold = QFont()
        font_lite_info_bold.setFamily('MonoxRegular Bold')
        font_lite_info_bold.setPointSize(12)

        self.label_date_lite = QLabel('Date      ')
        self.label_time_lite = QLabel('Time      ')
        self.label_loc_lite = QLabel('Location  ')
        self.label_name_lite = QLabel('Name      ')
        self.label_note_lite = QLabel('Note')

        self.label_date_lite.setFont(font_lite_info)
        self.label_time_lite.setFont(font_lite_info)
        self.label_loc_lite.setFont(font_lite_info)
        self.label_name_lite.setFont(font_lite_info)
        self.label_note_lite.setFont(font_lite_info)
        self.label_gender_lite = QLabel('Gender')
        self.label_gender_lite.setFont(font_lite_info_bold)

        self.dateedit_date_lite = QDateEdit(QDate.currentDate())
        self.timeedit_time_lite = QTimeEdit(QTime.currentTime())
        self.lineedit_loc_lite = QLineEdit('Mars')
        self.lineedit_name_lite = QLineEdit('Object')
        self.radiobutton_users_gender_male_lite = QRadioButton('Male')
        self.radiobutton_users_gender_female_lite = QRadioButton('Female')
        self.radiobutton_users_gender_secret_lite = QRadioButton('Secret')
        self.textedit_note_lite = QTextEdit('Lite')

        self.dateedit_date_lite.setDisplayFormat('yyyy/MM/dd')
        self.dateedit_date_lite.setCalendarPopup(True)
        self.dateedit_date_lite.setFont(font_lite_info)
        self.timeedit_time_lite.setDisplayFormat('HH : mm')
        self.timeedit_time_lite.setFont(font_lite_info)
        self.lineedit_loc_lite.setFont(font_lite_info)
        self.lineedit_name_lite.setFont(font_lite_info)
        self.textedit_note_lite.setFont(font_lite_info)

    def set_page_lite_opt(self):
        """DocString for set_page_lite_opt"""
        #@todo: to be defined.
        pass

    def set_layout(self):
        """DocString for set_layout"""
        #@todo: to be defined.
        """# Layout Global"""
        layout_main = QHBoxLayout(spacing=0)
        layout_main.setContentsMargins(0, 0, 0, 0)

        layout_main.addWidget(self.list_option)
        layout_main.addWidget(self.stack_window)
        self.setLayout(layout_main)

        """# Layout Stack"""
        layout_stack_window = self.set_layout_stack_window()
        layout_tab_lite_info = self.set_layout_tab_lite_info()
        layout_tab_lite_opt = self.set_layout_tab_lite_opt()
        layout_tab_pro_info = self.set_layout_tab_pro_info()
        layout_tab_pro_opt = self.set_layout_tab_pro_opt()
        self.tab_page_lite_info.setLayout(layout_tab_lite_info)
        self.tab_page_pro_info.setLayout(layout_tab_pro_info)

    def set_layout_stack_window(self):
        """DocString for set_layout_stack_window"""
        #@todo: to be defined.

        pass

    def set_layout_tab_lite_info(self):
        """DocString for set_layout_tab_lite_info"""
        #@todo: to be defined.
        layout_main = QVBoxLayout(self.tab_page_lite_info)
        layout_info_2 = QHBoxLayout()
        layout_note_2 = QVBoxLayout()
        layout_time_3 = QVBoxLayout()
        layout_user_3 = QVBoxLayout()
        layout_date_4 = QHBoxLayout()
        layout_time_4 = QHBoxLayout()
        layout_loc_4 = QHBoxLayout()
        layout_name_4 = QHBoxLayout()
        layout_gender_4 = QVBoxLayout()
        layout_gender_5 = QHBoxLayout()

        groupbox_radiobutton = QGroupBox()
        groupbox_radiobutton.setStyleSheet(self.stylesheet_groupbox)
        line_split = QFrame()
        line_split.setFrameShape(QFrame.VLine)
        line_split.setFrameShadow(QFrame.Sunken)

        layout_gender_5.addWidget(self.radiobutton_users_gender_male_lite)
        layout_gender_5.addWidget(self.radiobutton_users_gender_female_lite)
        layout_gender_5.addWidget(self.radiobutton_users_gender_secret_lite)
        groupbox_radiobutton.setLayout(layout_gender_5)

        layout_gender_4.addWidget(self.label_gender_lite)
        layout_gender_4.addWidget(groupbox_radiobutton)

        layout_name_4.setAlignment(Qt.AlignLeft)
        layout_loc_4.setAlignment(Qt.AlignLeft)
        layout_time_4.setAlignment(Qt.AlignLeft)
        layout_date_4.setAlignment(Qt.AlignLeft)

        layout_name_4.addWidget(self.label_name_lite)
        layout_name_4.addWidget(self.lineedit_name_lite)
        layout_loc_4.addWidget(self.label_loc_lite)
        layout_loc_4.addWidget(self.lineedit_loc_lite)
        layout_time_4.addWidget(self.label_time_lite)
        layout_time_4.addWidget(self.timeedit_time_lite)
        layout_date_4.addWidget(self.label_date_lite)
        layout_date_4.addWidget(self.dateedit_date_lite)

        layout_time_3.addLayout(layout_date_4)
        layout_time_3.addLayout(layout_time_4)
        layout_time_3.addLayout(layout_loc_4)
        layout_user_3.addLayout(layout_name_4)
        layout_user_3.addLayout(layout_gender_4)

        layout_info_2.addLayout(layout_time_3)
        layout_info_2.addWidget(line_split)
        layout_info_2.addLayout(layout_user_3)

        layout_note_2.addWidget(self.label_note_lite)
        layout_note_2.addWidget(self.textedit_note_lite)

        layout_main.addLayout(layout_info_2)
        layout_main.addLayout(layout_note_2)


        return layout_main




    def set_layout_tab_lite_opt(self):
        """DocString for set_layout_tab_lite_opt"""
        #@todo: to be defined.

        pass

    def set_layout_tab_pro_info(self):
        """DocString for set_layout_tab_lite_info"""
        #@todo: to be defined.
        layout_main = QVBoxLayout(self.tab_page_pro_info)
        layout_info_2 = QHBoxLayout()
        layout_note_2 = QVBoxLayout()
        layout_time_3 = QVBoxLayout()
        layout_user_3 = QVBoxLayout()
        layout_date_4 = QHBoxLayout()
        layout_time_4 = QHBoxLayout()
        layout_loc_4 = QHBoxLayout()
        layout_name_4 = QHBoxLayout()
        layout_gender_4 = QVBoxLayout()
        layout_gender_5 = QHBoxLayout()

        groupbox_radiobutton = QGroupBox()
        groupbox_radiobutton.setStyleSheet(self.stylesheet_groupbox)
        line_split = QFrame()
        line_split.setFrameShape(QFrame.VLine)
        line_split.setFrameShadow(QFrame.Sunken)

        layout_gender_5.addWidget(self.radiobutton_users_gender_male_pro)
        layout_gender_5.addWidget(self.radiobutton_users_gender_female_pro)
        layout_gender_5.addWidget(self.radiobutton_users_gender_secret_pro)
        groupbox_radiobutton.setLayout(layout_gender_5)

        layout_gender_4.addWidget(self.label_gender_pro)
        layout_gender_4.addWidget(groupbox_radiobutton)

        layout_name_4.setAlignment(Qt.AlignLeft)
        layout_loc_4.setAlignment(Qt.AlignLeft)
        layout_time_4.setAlignment(Qt.AlignLeft)
        layout_date_4.setAlignment(Qt.AlignLeft)

        layout_name_4.addWidget(self.label_name_pro)
        layout_name_4.addWidget(self.lineedit_name_pro)
        layout_loc_4.addWidget(self.label_loc_pro)
        layout_loc_4.addWidget(self.lineedit_loc_pro)
        layout_time_4.addWidget(self.label_time_pro)
        layout_time_4.addWidget(self.timeedit_time_pro)
        layout_date_4.addWidget(self.label_date_pro)
        layout_date_4.addWidget(self.dateedit_date_pro)

        layout_time_3.addLayout(layout_date_4)
        layout_time_3.addLayout(layout_time_4)
        layout_time_3.addLayout(layout_loc_4)
        layout_user_3.addLayout(layout_name_4)
        layout_user_3.addLayout(layout_gender_4)

        layout_info_2.addLayout(layout_time_3)
        layout_info_2.addWidget(line_split)
        layout_info_2.addLayout(layout_user_3)

        layout_note_2.addWidget(self.label_note_pro)
        layout_note_2.addWidget(self.textedit_note_pro)

        layout_main.addLayout(layout_info_2)
        layout_main.addLayout(layout_note_2)

        return layout_main


    def set_layout_tab_pro_opt(self):
        """DocString for set_layout_tab_pro_opt"""
        #@todo: to be defined.

        pass




if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = WindowOption()
    win.show()
    sys.exit(app.exec_())
