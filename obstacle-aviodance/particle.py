from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from methods.geometry import unit_vector
import numpy as np

class Particle:
    def __init__(self, position, velocity=None, acceleration=np.zeros(2), animated=True):

        if velocity is None:
            velocity = [0,0]
        self.pos = np.array(position, dtype=float)
        self.vel = np.array(velocity, dtype=float)
        self.acc = acceleration
        self.vmax = 0.1
        self.animated = animated

    # animation functions
    def start(self, fig=plt.gcf(), ax=plt.gca(), interval=100):
        if self.animated:
            self.ln, = ax.plot([], [], 'ro')
        self.ani = FuncAnimation(fig, self.update, interval=interval)

    def update(self, frame):
        self.vel += self.acc
        self.vel = self.vmax * unit_vector(self.vel)
        self.pos += self.vel
        self.acc = np.zeros(2)
        if self.animated:
            self.ln.set_data(self.pos[0], self.pos[1])

    # control methods
    def push(self, force, maxForce: float):
        """apply a force in give direction on the particle"""

    def steer(self, steer, maxForce):
        steer = self.vmax * unit_vector(steer)  # normalise
        steer -= self.vel  # this is the actual steering vector. The above one is the target direction
        steer *= maxForce  # sensitivity
        return steer


    def pause(self):
        self.ani.event_source.stop()
    def play(self):
        self.ani.event_source.start()

    # setter methods
    def sch(self, heading: int):
        heading = np.deg2rad(heading)
        self.vel = self.vmax*np.array([np.cos(heading), np.sin(heading)])

    def scv(self, vx, vy):
        self.vel = np.array([vx, vy], dtype=float)
    def scp(self, x, y):
        self.pos = np.array([x, y], dtype=float)

    #getters
    def gch(self):
        """return absolute heading from x axis"""
        return np.arctan2(self.vel[1], self.vel[0])*180/np.pi+360


