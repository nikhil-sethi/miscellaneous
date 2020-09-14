# simple particle swarm implementation

import random
import importlib
import numpy as np
from scipy.spatial import distance
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import time

# parameters
NMax = 20  # number of uavs
GMax = 0  # max PSO iterations
x_bound = 500  # Max geofence abscissa
y_bound = 500  # Max geofence ordinate
c1 = 2  # local best weight
c2 = 2  # global best weight
w = 0.729  # Inertia weight
wdamp = 0.85
fitness_list = [0] * (GMax + 1)
V = 20
crit_dist = 3
niche_radius=40
time_step = 0.05  # not technically a time step. smaller it is more position will be plotted along the paths (accuracy)
particle = [0] * (NMax + 1)
thread = [0] * (NMax + 1)
plotter = [0] * (NMax + 1)
dist = np.zeros(shape=(NMax+1,NMax+1))


# global GlobalBest

# initialise human locations
import humans  # import humans.py file as a library

importlib.reload(humans)  # reflect any changes in the library


# def ObjFun(current_pos, human_pos):
#     fitness = particles[n].fitness
#     dist = distance.euclidean(current_pos, human_pos)
#     if dist < 20 and i not in particles[n].checklist:
#         fitness = fitness + 1
#         print('particle:', n, 'near', 'loc', i, fitness)
#         particles[n].checklist.append(i)
#         print(particles[n].checklist)
#     return fitness
def testFun(current_pos):
    return -((current_pos[0] - x_bound / 2) ** 2 + (current_pos[1] - y_bound / 2) ** 2)


# def plotHumans():
#     plt.xlim(0, x_bound)
#     plt.ylim(0, y_bound)
#     for pos in humans.locations:
#         plt.plot(pos[0], pos[1], 'x', color='r')
class MyPlotClass:
    def __init__(self, particleClass,index):
        self._particleClass = particleClass
        self.n=index
        self.plot, = plt.plot(0,0, marker='o', color='b')
        self.annotation = plt.annotate(self.n, (0,0))
        plt.xlim(0, x_bound)
        plt.ylim(0, y_bound)
        self.ani = FuncAnimation(plt.gcf(), self.run, interval=1000 * time_step,
                                 repeat=True)  # a live plotting function which listens to change in the variables

    def run(self, i):
        # target_pos = self._particleClass.target_pos
        current_pos = self._particleClass.current_pos
        # print("plotting data")
        # if distance.euclidean(current_pos, target_pos) > crit_dist:
        self.plot.set_data(current_pos[0], current_pos[1])
        self.annotation.set_x(current_pos[0])
        self.annotation.set_y(current_pos[1])

class ThreadClass(threading.Thread):
    def __init__(self, particleClass, globalBestClass,index):
        threading.Thread.__init__(self)
        self._particleClass = particleClass
        self._globalClass = globalBestClass
        self.n=index
        if not self.is_alive():
            self.start()
        # print('%s started' % self.getName())

    def run(self, lastime=time.time()):
        global w
        current_pos = self._particleClass.current_pos
        deltaDMax = [0.5 * x_bound, 0.5 * y_bound]
        deltaD = 0
        for G in range(1, GMax + 1):
            deltaD = w * deltaD + c1 * random.random() * (
                        self._particleClass.best.current_pos - current_pos) + c2 * random.random() * (
                                 self._globalClass.current_pos - current_pos)
            deltaD[0] = min(deltaD[0], deltaDMax[0]); deltaD[1] = min(deltaD[1], deltaDMax[1]);
            deltaD[0] = max(deltaD[0], -deltaDMax[0]); deltaD[1] = max(deltaD[1], -deltaDMax[1]);
            print(deltaD, self.n)
            target_pos = current_pos + deltaD
            target_pos[0] = min(target_pos[0], x_bound); target_pos[1] = min(target_pos[1], y_bound);
            target_pos[0] = max(target_pos[0], -x_bound); target_pos[1] = max(target_pos[1], -y_bound);

            self._particleClass.target_pos = target_pos

            # print(G,self.getName())
            # print(current_pos)
            # print("updating data")
            print('target=%s for particle %s ' % (target_pos, self.n))
            checktime = time.time()
            while distance.euclidean(current_pos, target_pos) > crit_dist:
                current_pos = current_pos + (deltaD / distance.euclidean([0, 0], deltaD)) * V * (time.time() - lastime)
                lastime = time.time()
                if lastime - checktime > 1:
                    print('current_postion=%s for particle %s' % (
                    current_pos, self.n))  # print current_postion every five seconds
                    checktime = time.time()
                # Update current_postion in current_postionClass

                self._particleClass.fitness = testFun(current_pos)
                if self._particleClass.fitness > self._particleClass.best.fitness:
                    self._particleClass.best.fitness = self._particleClass.fitness  # replace the personalbest of the particle if new fitness is better than best
                    self._particleClass.best.current_pos = self._particleClass.current_pos
                    # print('ch1')
                    if self._particleClass.best.fitness > self._globalClass.fitness:
                        # print('ch2')
                        self._globalClass.current_pos = self._particleClass.best.current_pos  # Make the global best the same as a personalbest if latter is better
                        self._globalClass.fitness = self._particleClass.best.fitness
                        print('Globalbest ', self._globalClass.current_pos, self.n)

                self._particleClass.current_pos = current_pos

                time.sleep(time_step)

            w = w * wdamp


class ParticleClass:
    def __init__(self, current_pos):
        self.current_pos = current_pos
        self.neighbour = []

# initialise population
GlobalBest = ParticleClass(0)  # Create global best object (has the same attributes as a particle)
GlobalBest.fitness = float('-inf')  # Initial fitness has to be the worst case
for n in range(1, NMax + 1):
    particle[n] = ParticleClass(max(x_bound, y_bound) * np.random.rand(2))

for n in range(1,NMax+1):
    # for i, human_pos in enumerate(humans.locations):
    #   particles[n].fitness = ObjFun(particles[n].current_postion, human_pos)
    particle[n].fitness = testFun(particle[n].current_pos)
    # update personal best
    particle[n].best = ParticleClass(
        particle[n].current_pos)  # create a personal best object as an attribute of the respective particle
    particle[n].best.fitness = particle[n].fitness  # same fitnesses as particle initially

    # plt.annotate(n, (particles[n].current_postion[0], particles[n].current_postion[1]))

    # Update global best
    # GlobalBest.newfitness = sum([particles[n].best.fitness for n in range(1,NMax+1)])
    if particle[n].best.fitness > GlobalBest.fitness:
        GlobalBest = particle[n].best
        # print('globalbest', GlobalBest.current_pos)
    for j in range(1,NMax+1):
        dist[n][j] = distance.euclidean(particle[n].current_pos, particle[j].current_pos)
        if niche_radius > dist[n][j] > 0:
            particle[n].neighbour.append(j)

for n in range(1, NMax + 1):
    thread[n] = ThreadClass(particle[n], GlobalBest,n)
    plotter[n] = MyPlotClass(particle[n],n)
    plt.show()
