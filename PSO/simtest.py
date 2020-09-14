import threading
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial import distance

x_bound = 1000
y_bound = 1000
V = 15
crit_dist = 0.5
time_step = 0.05  # not technically a time step. smaller it is more position will be plotted along the paths (accuracy)


class PositionClass:
    def __init__(self, current_pos, target_pos):
        self.current_pos = current_pos
        self.target_pos = target_pos

class MyPlotClass:
    def __init__(self, posClass):
        self._posClass = posClass
        self.hLine, = plt.plot(0, 0, marker='o')
        plt.xlim(0, x_bound)
        plt.ylim(0, y_bound)
        self.ani = FuncAnimation(plt.gcf(), self.run, interval=1000 * time_step,
                                 repeat=True)  # a live plotting function which listens to change in the variables

    def run(self, i):
        posf = self._posClass.target_pos
        posi = self._posClass.current_pos
        # print("plotting data")
        if distance.euclidean(posi, posf) > crit_dist:
            self.hLine.set_data(posi[0], posi[1])


class particle(threading.Thread):
    def __init__(self, posClass):
        threading.Thread.__init__(self)
        self._posClass = posClass
        if not self.is_alive():
            self.start()
        print('%s started' % self.getName())

    def run(self, lastime=time.time()):
        # print("updating data")
        posf = self._posClass.target_pos
        posi = self._posClass.current_pos
        plt.plot(posi[0], posi[1], marker='x', color='r')
        plt.plot(posf[0], posf[1], marker='x', color='r')
        print('target=%s for %s ' % (posf, self.getName()))
        checktime = time.time()
        while distance.euclidean(posi, posf) > crit_dist:
            posi = posi + ((posf - posi) / distance.euclidean(posi, posf)) * V * (time.time() - lastime)
            lastime = time.time()
            if lastime-checktime > 5:
                print('current position=%s for %s' % (posi, self.getName()))     #print position every five seconds
                checktime = time.time()
            # Update position in PositionClass
            self._posClass.current_pos = posi
            time.sleep(time_step)



positions1 = PositionClass(x_bound * np.random.rand(2), x_bound * np.random.rand(2))
positions2 = PositionClass(x_bound * np.random.rand(2), x_bound * np.random.rand(2))
plotter1 = MyPlotClass(positions1)
plotter2 = MyPlotClass(positions2)

fetcher1 = particle(positions1)     #starts a thread for calculation
fetcher2 = particle(positions2)
plt.show()
# fetcher1.join()
# fetcher2.join()


class a:
    def