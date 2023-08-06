import wx
import numpy as np
import matplotlib
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

class ImageShowPanel(wx.Panel):

    def __init__(self, parent, title, ID=wx.ID_ANY, dpi=100):
        wx.Panel.__init__(self, parent, ID)

        self.dpi = dpi
        self.fig = Figure((4.5, 3.5), dpi=self.dpi, facecolor='lightgray')
        self.canvas = FigCanvas(self, -1, self.fig)

        self.axes = self.fig.add_subplot(111)

        if callable(getattr(self.axes, 'set_facecolor', None)):
            self.axes.set_facecolor('white')
        else:
            self.axes.set_axis_bgcolor('white')

        self.axes.grid(True, color='black')
        if title:
            self.axes.set_title(title, size=10)
        #self.toolbar = NavigationToolbar(self.canvas)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, flag=wx.ALL | wx.GROW)
        #self.sizer.Add(self.toolbar, 0, flag=wx.ALL | wx.GROW)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

        self.images = []
        self.meshes = []
        #self.animator = animation.FuncAnimation(self.fig, self.__update_func, interval=100, blit=True)
        self.colorbar = None

    class Image:
        def __init__(self, axes, x, y):
            self.x = x
            self.y = y
            self.data_provider = None
            self.data = np.array([np.nan for i in range(len(x)*len(y))])
            X = self.__mesh_from_range(x)
            Y = self.__mesh_from_range(y)
            axes.set_xlim(left=min(X), right=max(X))
            axes.set_ylim(bottom=min(Y), top=max(Y))
            X, Y = np.meshgrid(np.array(X), np.array(Y))
            self.mesh = axes.pcolormesh(X, Y, np.zeros((len(y),len(x))),cmap='inferno')
            self.cmap = matplotlib.cm.get_cmap('inferno')

        @staticmethod
        def __mesh_from_range(x):
            x_new = [float((x[i]+x[i+1])/2) for i in range(len(x)-1)]
            x_new.insert(0, float(x[0]-(x[1]-x[0])/2))
            x_new.append(float(x[-1]+(x[-1]-x[-2])/2))
            return x_new

        def update(self, colorbar):
            zdata = self.data_provider.get_data()
            for i in range(len(zdata)):
                curve = zdata[i].read_data()
                start = i * len(self.x)
                if zdata[i].write_data() == self.x:
                    self.data[start:(start+len(curve))] = curve
                elif start+len(self.x)-len(curve)-1 >= 0:
                    self.data[(start+len(self.x)-1):(start+len(self.x)-len(curve)-1):-1] = curve
                else:
                    self.data[(start+len(self.x)-1)::-1] = curve
            new_data = np.ma.masked_invalid(np.atleast_2d(self.data))
            self.cmap.set_bad('black', 1)
            if not new_data.min() is np.ma.masked:
                norm = matplotlib.colors.Normalize(vmin=new_data.min(), vmax=new_data.max())
                colorbar.set_clim(vmin=new_data.min(), vmax=new_data.max())
                colorbar.set_ticks(np.linspace(new_data.min(), new_data.max(), num=11, endpoint=True))
                colorbar.draw_all()
                new_color = self.cmap(norm(new_data.T.ravel()))
                self.mesh.update({'facecolors':new_color})

        def set_data(self, data_provider):
            self.data_provider = data_provider

    def add_image(self, x, y):
        for img in self.images:
            img.mesh.remove()
        self.images = []
        self.meshes = []
        image = ImageShowPanel.Image(self.axes, x, y)
        self.images.append(image)
        self.meshes = [x.mesh for x in self.images]
        if self.colorbar == None:
            self.colorbar = self.fig.colorbar(image.mesh)
        self.canvas.draw()
        return image

    def update_image(self, image):
        image.update(self.colorbar)
        self.canvas.draw()

    def __update_func(self, *args):
        return self.meshes
