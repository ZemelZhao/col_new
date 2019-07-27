import pyqtgraph as pg
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QFont
import random


class CustomAxis(pg.AxisItem):
    def __init__(self, ydict, *arg, **kwarg):
        super(CustomAxis, self).__init__(*arg, **kwarg)
        self.y_values = np.asarray(ydict.keys())
        self.y_string = ydict.values()

    def tickStrings(self, values, scale, spacing):
        res = super(CustomAxis, self).tickStrings(values, scale, spacing)
        return res

class PlotWidgetCol(pg.PlotWidget):
    def __init__(self, *arg, **kwarg):
        super(PlotWidgetCol, self).__init__(*arg, **kwarg)

    def mouseMoveEvent(self, e):
        pass

    def mousePressEvent(self, e):
        pass

    def mouseReleaseEvent(self, e):
        pass

    def wheelEvent(self, e):
        pass

class FingerTest(QWidget):
    """ DocString for FingerTest"""

    def __init__(self, text='TESTZ', value=72, size=(100, 100)):
        #@todo: to be defined.
        super(FingerTest, self).__init__()
        self.list_color = [QColor(247, 201, 120), QColor(247, 198, 119), QColor(247, 196, 118), QColor(246, 193, 117), QColor(246, 190, 116),
                           QColor(246, 187, 114), QColor(245, 185, 114), QColor(245, 182, 112), QColor(245, 179, 111), QColor(244, 176, 110),
                           QColor(244, 174, 109), QColor(244, 171, 108), QColor(244, 168, 107), QColor(243, 165, 106), QColor(243, 163, 106),
                           QColor(243, 160, 106), QColor(243, 157, 107), QColor(243, 155, 107), QColor(243, 152, 108), QColor(242, 149, 109),
                           QColor(242, 147, 110), QColor(242, 144, 110), QColor(242, 141, 111), QColor(242, 138, 111), QColor(242, 136, 112),
                           QColor(241, 133, 112), QColor(241, 130, 113), QColor(238, 128, 115), QColor(236, 127, 118), QColor(233, 125, 120),
                           QColor(230, 124, 122), QColor(227, 122, 124), QColor(225, 120, 126), QColor(222, 118, 128), QColor(219, 117, 131),
                           QColor(216, 115, 132), QColor(214, 113, 135), QColor(211, 111, 137), QColor(208, 110, 139), QColor(205, 108, 141),
                           QColor(203, 107, 143), QColor(200, 107, 145), QColor(197, 107, 147), QColor(194, 107, 148), QColor(191, 107, 150),
                           QColor(188, 107, 152), QColor(186, 107, 154), QColor(183, 106, 155), QColor(180, 107, 157), QColor(177, 106, 159),
                           QColor(174, 107, 161), QColor(171, 106, 162), QColor(168, 106, 164), QColor(166, 106, 165), QColor(164, 106, 166),
                           QColor(162, 106, 166), QColor(160, 106, 167), QColor(158, 106, 168), QColor(156, 106, 169), QColor(154, 106, 170),
                           QColor(152, 106, 171), QColor(150, 106, 171), QColor(148, 106, 172), QColor(146, 106, 173), QColor(144, 106, 174),
                           QColor(142, 106, 174), QColor(141, 105, 174), QColor(139, 104, 174), QColor(138, 103, 174), QColor(136, 102, 173),
                           QColor(135, 102, 173), QColor(133, 101, 173), QColor(132, 100, 173), QColor(131, 99, 173), QColor(129, 99, 173),
                           QColor(128, 97, 172), QColor(126, 97, 173), QColor(125, 96, 172), QColor(123, 95, 172), QColor(120, 94, 172),
                           QColor(118, 94, 173), QColor(115, 93, 173), QColor(113, 92, 173), QColor(110, 91, 173), QColor(108, 91, 173),
                           QColor(105, 89, 173), QColor(102, 89, 174), QColor(99, 88, 174), QColor(97, 87, 174), QColor(94, 86, 174),
                           QColor(92, 86, 174), QColor(89, 85, 174), QColor(87, 85, 175), QColor(85, 84, 175), QColor(83, 84, 175),
                           QColor(81, 84, 175), QColor(79, 84, 175), QColor(77, 83, 175), QColor(75, 83, 176), QColor(73, 83, 176),
                           QColor(71, 82, 176)]
        self.text = text
        self.value = value
        self.size = size
        self.initUI()

    def color_show(self, data):
        """DocString for color_show"""
        return self.list_color[data]


    def initUI(self, ):
        """DocString for initUI"""
        #@todo: to be defined.
        pass


    def setValue(self, data, re=True):
        """DocString for change_percent"""
        #@todo: to be defined.
        self.value = data
        if re:
            self.repaint()

    def setSize(self, data, re=True):
        """DocString for change_size"""
        #@todo: to be defined.
        self.size = data
        if re:
            self.repaint()

    def setText(self, data, re=True):
        """DocString for change_text"""
        #@todo: to be defined.
        self.text = data
        if re:
            self.repaint()

    def paintEvent(self, event):
        """DocString for paintEvent"""
        #@todo: to be defined.
        		#:event: @todo.
        qp = QPainter()
        qp.begin(self)
        self.draw_widget(qp)
        qp.end()


    def draw_widget(self, qp):
        """DocString for draw_widget"""
        #@todo: to be defined.
		#:parent: @todo.
        w = self.size[0]
        h = self.size[1]
        qp.setPen(self.color_show(self.value))
        qp.setBrush(self.color_show(self.value))
        qp.drawRect(0, 0, w, h)

        font = QFont()
        font.setFamily('MonoxLight')
        font.setPointSize(20)
        qp.setFont(font)

        if self.value < 50:
            qp.setPen(QColor(0x00, 0x00, 0x00))
            qp.setBrush(QColor(0x00, 0x00, 0x00))
        else:
            qp.setPen(QColor(0xFF, 0xFF, 0xFF))
            qp.setBrush(QColor(0xFF, 0xFF, 0xFF))

        metric = qp.fontMetrics()
        show_value = str('%d%%' % self.value)
        fwv = metric.width(show_value)
        fhv = metric.height()
        show_text = str(self.text)
        metric_text = qp.fontMetrics()
        fwt = metric.width(show_text)
        fht = metric.height()

        qp.drawText(w/2-fwv/2, h, show_value)
        qp.drawText(w/2-fwt/2, h/2+fht/2, show_text)

class WindowMain(QWidget):
    """ DocString for WindowMain"""
    def __init__(self, ):
        #@todo: to be defined.

        super(WindowMain, self).__init__()
        self.initUI()

    def initUI(self):
        """DocString for initUI"""
        #@todo: to be defined.
        self.setWindowTitle('Test')
        self.setFixedSize(1000, 800)

        self.test_widget = FingerTest(size=(100, 700), text='TEST')

        layout_main = QHBoxLayout(self)
        self.setLayout(layout_main)
        layout_main.addWidget(self.test_widget)

    def keyPressEvent(self, event):
        """DocString for keyReleaseEvent"""
        #@todo: to be defined.
		#:event: @todo.
        if event.key() == Qt.Key_Q:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.close()

        if event.key() == Qt.Key_C:
            self.test_widget.setValue(random.randint(0, 100))



if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = WindowMain()
    win.show()
    sys.exit(app.exec_())


