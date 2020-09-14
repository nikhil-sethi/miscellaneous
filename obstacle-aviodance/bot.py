#TODO: geofence
#TODO: path planning

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patch
from geometry import *

xLim = 40 # //metres
yLim = 40  # //metres
fig, ax = plt.subplots()
ax.set(xlim=(-xLim, xLim), ylim=(-yLim, yLim), aspect='equal')

import particle # this needs to be after the figure definition

class Bot(particle.Particle):
    def __init__(self, position, velocity=None, acceleration=0,  animated=True):
        super().__init__(position, velocity, acceleration, animated)
        self.r = 20
        self.phi = 40
        self.sensor = patch.Wedge((self.pos[0], self.pos[1]), self.r, self.gch()-self.phi/2, self.gch()+self.phi/2,edgecolor='b', facecolor=None)

    def sense(self):
        """returns x,y coordinates of the detected object"""
        #set current sensor position
        self.sensor.set_center((self.pos[0], self.pos[1]))
        self.sensor.set_theta1(self.gch() - self.phi / 2)
        self.sensor.set_theta2(self.gch() + self.phi / 2)
        # p=all points on the map. Need to have this as a global variable
        return p[self.sensor.contains_points(p)]  #get all points within the sensor wedge

    def start(self):

        self.ell = patch.Ellipse((0,0),1,1, edgecolor='blue', facecolor='None')
        ax.add_patch(self.ell)
        # ax.plot(0,0, 'bo')
        super().start()


    def update(self, frame):
        target = self.avoid(self.sense())
        if np.any(target): #if everything is not zero in target
            self.acc += self.steer(target, 0.25)

        # self.acc += get_steer(np.array([xLim / 2, yLim / 2]) - self.pos)
        super().update(self)


    def path_opt(self):
        pass

    def avoid(self, sensordata):
        """returns an avoidance vector which is tangent to convex region"""

        if sensordata.size < 6: #need to have at least three points for an ellipse
            return np.zeros(2)  #nothing
        # create convex avoidance region
        q0, a, b, th = confidence_ellipse(sensordata[:, 0], sensordata[:, 1])
        self.ell.set_center(q0)
        self.ell.width = 2 * a
        self.ell.height = 2 * b
        self.ell.angle = 180 * th / 3.1459
        # get the two contact points from current position
        q1_p = rotmat(-th) @ (self.pos - q0)  # (x1',y1')=from rotated frame to standard ellipse at origin
        v_p = rotmat(-th) @ self.vel #rotated velocity vector
        d = b ** 2+(a*v_p[1]/v_p[0])**2-(-v_p[1]/v_p[0]*q1_p[0]+q1_p[1])**2 #discriminant
        # do nothing if velocity is outside of cone
        if d < 0: return np.zeros(2)
        m = np.roots([a ** 2 - q1_p[0] ** 2, 2 * q1_p[0] * q1_p[1],
                      b ** 2 - q1_p[1] ** 2])  # slope of the tangent from (x1',y1')
        return (rotmat(th) @ np.array([np.cos(np.arctan(m)), np.sin(np.arctan(m))])).T[0]


ax.scatter(np.random.normal(-23, xLim*np.random.rand()/2, 100), np.random.normal(30, xLim*np.random.rand()/2, 100), s=0.5)
# ax.scatter(np.random.normal(3, xLim*np.random.rand()/2, 100), np.random.normal(11, xLim*np.random.rand()/2, 100), s=0.5)
# ax.scatter(np.random.normal(-5, xLim*np.random.rand()/2, 100), np.random.normal(-17, xLim*np.random.rand()/2, 100), s=0.5)
# ax.scatter(np.random.normal(15, xLim*np.random.rand()/2, 100), np.random.normal(-7, xLim*np.random.rand()/2, 100), s=0.5)
p = ax.collections[-1].get_offsets().data
# p = np.append(p, ax.collections[-2].get_offsets().data,axis=0)
# p = np.append(p, ax.collections[-3].get_offsets().data,axis=0)
# p = np.append(p, ax.collections[-4].get_offsets().data,axis=0)

bot = Bot([0, 0], velocity=[-23, 30])
bot.start()

