import wx
import matplotlib
import numpy as np
import pylab
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas

class SimpleAxisPanel(wx.Panel):
    """A simple panel, containing a single line graph"""

    def __init__(self, parent, ID=wx.ID_ANY, dpi=80):
        wx.Panel.__init__(self, parent, ID)

        self.dpi = dpi
        self.fig = Figure((4.0, 2.25), dpi=self.dpi)

        self.axes = self.fig.add_subplot(111)
        if callable(getattr(self.axes, 'set_facecolor', None)):
            self.axes.set_facecolor('black')
        else:
            self.axes.set_axis_bgcolor('black')
        self.axes.grid(True, color='gray')

        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        self.plot_data = self.axes.plot([], linewidth=1, color=(1, 1, 0))[0]
    
        self.canvas = FigCanvas(self, -1, self.fig)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, flag=wx.ALL | wx.GROW)    
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

    def plot(self, x, y):
        if len(x) > 1:
            self.axes.set_xbound(lower=min(x), upper=max(x))
            self.axes.set_ybound(lower=min(y), upper=max(y))
        
        self.plot_data.set_xdata(np.array(x))
        self.plot_data.set_ydata(np.array(y))
        self.canvas.draw()