# simple particle swarm implementation

import random
import importlib
import numpy as np
from scipy.spatial import distance
from matplotlib import pyplot as plt

# parameters
NMax = 5  # number of uavs
GMax = 200  # max PSO iterations
x_bound = 100  # Max geofence abscissa
y_bound = 100  # Max geofence ordinate
c1 = 2  # local best weight
c2 = 2  # global best weight
w = 0.729  # Inertia weight
wdamp=0.99
fitness_list = [0] * (GMax + 1)

# initialise human locations
import humans  # import humans.py file as a library
importlib.reload(humans)  #reflect any changes in the library


def ObjFun(current_pos, human_pos):
    fitness = particles[n].fitness
    dist = distance.euclidean(current_pos, human_pos)
    if dist < 20 and i not in particles[n].checklist:
        fitness = fitness + 1
        print('particle:', n, 'near', 'loc', i, fitness)
        particles[n].checklist.append(i)
        print(particles[n].checklist)
    return fitness
def testFun(current_pos):
    return -((current_pos[0]-x_bound/2)**2+(current_pos[1]-y_bound/2)**2)

def plotHumans():
    plt.xlim(0, x_bound)
    plt.ylim(0, y_bound)
    for pos in humans.locations:
        plt.plot(pos[0], pos[1], 'x', color='r')

class particle(object):
    def __init__(self, position):
        self.position = position
        self.checklist = []  # define a default empty checklist attribute for each instance call
    fitness = 0
    velocity = np.array([0])


# initialise population
particles = [0] * (NMax + 1)
GlobalBest = particle(0)  # Create global best object (has the same attributes as a particle)
GlobalBest.fitness = float('-inf')  # Initial fitness has to be the worst case

plotHumans()
for n in range(1, NMax + 1):
    particles[n] = particle(np.array([x_bound * random.random(), y_bound * random.random()]))
    #for i, human_pos in enumerate(humans.locations):
     #   particles[n].fitness = ObjFun(particles[n].position, human_pos)
    particles[n].fitness=testFun(particles[n].position)
    # update personal best
    particles[n].best = particle(particles[n].position)  # create a personal best object as an attribute of the respective particle
    particles[n].best.fitness = particles[n].fitness  # same fitnesses as particle initially

    plt.plot(particles[n].position[0], particles[n].position[1], 'o', color='b')
    plt.annotate(n, (particles[n].position[0], particles[n].position[1]))

    # Update global best
    #GlobalBest.newfitness = sum([particles[n].best.fitness for n in range(1,NMax+1)])
    if particles[n].best.fitness > GlobalBest.fitness:
        GlobalBest = particles[n].best
plt.pause(0.01)
plt.cla()

# Main PSO loop
for G in range(1, GMax + 1):
    plotHumans()
    for n in range(1, NMax + 1):
        particles[n].velocity = w * particles[n].velocity + \
                                c1 * random.random() * (particles[n].best.position - particles[n].position) + \
                                c2 * random.random() * (GlobalBest.position - particles[n].position)
        particles[n].position = particles[n].position + particles[n].velocity


        #for i, human_pos in enumerate(humans.locations):
         #   particles[n].fitness = ObjFun(particles[n].position, human_pos)  # calculate new fitness at new position
        particles[n].fitness = testFun(particles[n].position)
        if particles[n].fitness > particles[n].best.fitness:
            particles[n].best.fitness = particles[n].fitness  # replace the personalbest of the particle if new fitness is better than best
            particles[n].best.position = particles[n].position

            if particles[n].best.fitness > GlobalBest.fitness:
                GlobalBest = particles[n].best  # Make the global best the same as a personalbest if latter is better

        plt.plot(particles[n].position[0], particles[n].position[1], 'o', color='b')
        plt.annotate(n, (particles[n].position[0], particles[n].position[1]))
    print('Globalbest', GlobalBest.fitness)
    fitness_list[G] = GlobalBest.fitness
    w = w*wdamp
    plt.pause(0.01)
    plt.cla()
# plt.plot(fitness_list,G)
