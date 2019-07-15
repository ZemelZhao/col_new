import pyqtgraph as pg
import numpy as np

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
