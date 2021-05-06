import matplotlib.pyplot as plt

import matplotlib.patches as patch
import numpy as np

ax = plt.gca()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
# plt.show(block=True)
class Shape(object):
    '''This class creates an object with mouse input and has relevant features of objects as getter
    supported shapes:
    -rectangle
    -ellipse

    supported features:
    -area
    -function of boundary
    '''

    def __init__(self, shape, ls='dashed', fc='None', ec='red'):
        # self.ax = plt.gca()

        if shape is 'rectangle':
            self.obj = patch.Rectangle((0, 0), 1, 1, linestyle=ls, facecolor=fc, edgecolor=ec)
        elif shape is 'ellipse':
            self.obj = patch.Ellipse((0, 0), 1, 1, linestyle=ls, facecolor=fc, edgecolor=ec)

        self.start = None
        self.end = None
        ax.add_patch(self.obj)
        self.flag = False
        self.cidpress = ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.is_disconnected=False


    def on_press(self, event):
        self.start = np.array([event.xdata, event.ydata]).astype('int')
        self.flag = True

    def on_motion(self, event):
        if self.flag is False: return
        self.end = np.array([event.xdata, event.ydata]).astype('int')
        try:
            self.obj.set_width(self.end[0] - self.start[0])
            self.obj.set_height(self.end[1] - self.start[1])
            self.obj.set_xy((self.start[0], self.start[1]))
        except:
            setattr(self.obj, "width", self.end[0] - self.start[0])
            setattr(self.obj, "height", self.end[1] - self.start[1])
            setattr(self.obj, "center", (self.start[0], self.start[1]))
        ax.figure.canvas.draw_idle()

    def on_release(self, *args):
        self.obj.set_linestyle('solid')
        ax.figure.canvas.draw()
        self.disconnect()
        self.flag = False

    def disconnect(self):
        ax.figure.canvas.mpl_disconnect(self.cidpress)
        ax.figure.canvas.mpl_disconnect(self.cidmotion)
        ax.figure.canvas.mpl_disconnect(self.cidrelease)
        self.is_disconnected=True

def bound_func():
    pass


def area():
    pass


def draw(shape, num=1, ls='dashed', fc='None', ec='red'):
    objlist = [Shape(shape, ls, fc, ec)]
    while len(objlist)<num:
        if objlist[-1].is_disconnected:
            objlist.append(Shape(shape, ls, fc, ec))

    return objlist
    # plt.show(block=False)



# draw('ellipse', num=3)