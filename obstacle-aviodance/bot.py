#TODO: geofence
#TODO: path planning
import time

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patch
from geometry import *


xLim = 40 # //metres
yLim = 40  # //metres
fig, ax = plt.subplots()

fig.set_size_inches(8,8)
# plt.show(block=False)

ax.set(xlim=(-xLim, xLim), ylim=(-yLim, yLim), aspect='equal')

import particle # this needs to be after the figure definition

class Bot(particle.Particle):
    def __init__(self, position, velocity=None, acceleration=0,  animated=True):
        super().__init__(position, velocity, acceleration, animated)
        self.r = 15
        self.phi = 50
        self.sensor = patch.Wedge((self.pos[0], self.pos[1]), self.r, self.gch()-self.phi/2, self.gch()+self.phi/2,edgecolor='k', facecolor=None, fill=False)
        # self.sensor= patch.Circle((self.pos[0], self.pos[1]), self.r,edgecolor='r', facecolor=None, fill=False)
        ax.add_patch(self.sensor)

        self.target_point, = ax.plot(0,0,'bo')
        self.goal = np.array([35,35])
        ax.plot(*self.goal, 'go', markersize=15)
        self.trail, = ax.plot(self.pos, 'ro', markersize=5)

    def sense(self):
        """returns x,y coordinates of the detected object"""
        #set current sensor position
        self.sensor.set_center((self.pos[0], self.pos[1]))
        self.sensor.set_theta1(self.gch() - self.phi / 2)
        self.sensor.set_theta2(self.gch() + self.phi / 2)
        # p=all points on the map. Need to have this as a global variable

        return p[self.sensor.contains_points(ax.transData.transform(p))]  #get all points within the sensor wedge

    def start(self):

        self.ell = patch.Ellipse((0,0),1,1, edgecolor='blue', facecolor='None')
        time.sleep(3)
        # ax.add_patch(self.sensor)
        ax.add_patch(self.ell)
        # ax.plot(0,0, 'bo')
        super().start(fig, ax)


    def update(self, frame):
        self.acc += self.steer(self.goal-self.pos, 0.05)
        target = self.avoid(self.sense())

        if np.any(target): #if everything is not zero in target
            try:
                self.acc += self.steer(target, 0.25)
            except:
                pass
            # self.target_point.set_data(target)
        # self.acc += get_steer(np.array([xLim / 2, yLim / 2]) - self.pos)
        super().update(self)
        if self.current_step%4:
            ax.plot(*self.pos, 'ro', markersize=1)
        # if self.pos
        # self.trail.set_data(self.pos)


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
        t_1 = tangentPointFromSlope(m[0], q1_p, a, b)     # gives tangent point to ellipse from an outside point
        t_2 = tangentPointFromSlope(m[1], q1_p, a, b)

        target_pt = t_1
        if t_2.dot(v_p) > 0:
            target_pt = t_2

        target_vec = rotmat(th)@(target_pt-q1_p)
        # target_vec = (rotmat(th) @ np.array([np.cos(np.arctan(m)), np.sin(np.arctan(m))])).T[0]
        target_trans = target_vec
        self.target_point.set_data(rotmat(th) @ target_pt + q0)
        return target_vec

# sd = xLim*np.random.rand()/2
sd = 2
seed = 49#np.random.randint(0,50)
print(seed)
np.random.seed(seed)
def randrange(a,b):
    val = a +(b-a)*np.random.rand()
    return val

# randrange(-40,40)
ax.scatter(np.random.normal(-24.55807058579893, sd, 100), np.random.normal(-28.673405296968895, sd, 100), s=3)
ax.scatter(np.random.normal(-16.366784971313884, sd, 100), np.random.normal(-8.861671508910575, sd, 100), s=3)
ax.scatter(np.random.normal(20, sd, 100), np.random.normal(28, sd, 100), s=2)
ax.scatter(np.random.normal(30, sd, 100), np.random.normal(-25, sd, 100),s=2)
p = ax.collections[-1].get_offsets().data
p = np.append(p, ax.collections[-2].get_offsets().data,axis=0)
p = np.append(p, ax.collections[-3].get_offsets().data,axis=0)
p = np.append(p, ax.collections[-4].get_offsets().data,axis=0)

vel = np.array([1,1])#-1+2*np.random.random(2)
bot = Bot([-40, -40], velocity=vel)
bot.start()
# bot.ani.save('ani.mp4', bot.writer)