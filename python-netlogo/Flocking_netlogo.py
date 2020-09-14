import nl4py, math
import numpy as np

nl4py.startServer("D:/Softwares/NetLogo 6.1.0")
nl = nl4py.NetLogoApp()

nl.openModel("D:/Nikhil/Projects/python_netlogo/Template.nlogo")
nl.command('set-patch-size 2.8')
N = 8
vMax = 2  # m/s
delT = 0.1  # seconds
maxSepTurn = 10
maxAvoidTurn = 10
maxAlignTurn = 20
minSepDist = 5
flockVision = 20
flockAngle = 25


def spawn(Nuavs):
    nl.command('clear-all')
    for i in range(Nuavs):
        nl.command(
            'crt 1[setxy {0} {1} set heading {2} set size 8] ask turtles [set label who]'.format(uav_pos[i][0],
                                                                                                 uav_pos[i][1],
                                                                                                 float(uav_head[i])))

def relheading(headb, heada):
    """relative heading of b with respect to a"""
    delH = headb - heada
    if abs(delH) >= 180:
        if headb >= heada:
            return delH - 360
        elif headb <= heada:
            return 360 - abs(delH)
    if abs(delH) < 180:
        return delH


def turn_towards(headb, heada, maxTurn):
    """Turn heading of 'a' towards vector 'b' with a maximum value"""
    relhead=relheading(headb, heada)
    heada = heada + [max(relhead, -maxTurn) if relhead < 0 else min(relhead, maxTurn)]
    return heada


def turnAndSlowDown(velocity, angle, k):
    # if relhead > 90:
    #     heading = uav_head[i] - angle
    # elif relhead < 90:
    heading = uav_head[i] + angle
    velocity = velocity * k
    return velocity, heading


def abs_heading(vector):
    """returns the absolute heading of vector from the Yaxis"""
    head = math.degrees(
        math.atan2(vector[0], vector[1]))  # angle in degrees from y axis, atan2 returns the correct quadrant
    if head < 0:
        return head + 360
    return head


def separate(flockmates):
    avg_diff = np.zeros(2)
    for k in flockmates:
        delS = uav_pos[k] - uav_pos[i]  # relative distance vector S
        delSMag = np.linalg.norm(delS)
        diff = -delS / delSMag
        # relhead = relheading(uav_head[i], uav_head[j])
        headS = abs_heading(delS)
        if abs(relheading(headS, uav_head[i])) < flockAngle / 2 and delSMag < minSepDist:
            print('separating')
            avg_diff += diff
    avg_diff /= len(flockmates)
    if np.any(avg_diff > 0):
        uav_head[i] = turn_towards(abs_heading(avg_diff), uav_head[i], maxSepTurn)
    # print('flag1')

def align(avg_head):
    '''for all uavs in flock get heading and turn by maxalign towards that heading'''
    # print('align')
    uav_head[i] = turn_towards(avg_head, uav_head[i], maxAlignTurn)
    # uav_head[i] = uav_head[i] + [ +maxAlignTurn if relhead > 0 else uav_head[i] -maxAlignTurn]

xMax = nl.report('max-pxcor')  # metres
yMax = nl.report('max-pycor')  # metres
xMin = nl.report('min-pxcor')  # metres
yMin = nl.report('min-pycor')  # metres
uav_pos = xMin + (xMax - xMin) * np.random.rand(N, 2)  # origin at center of area
uav_head = 360 * np.random.rand(N, 1)

spawn(N)
t = 0;
nl.command('reset-ticks')
ticks = 500
# reporters = ['[(list xcor ycor)] of reduce turtle-set sort turtles']   #get sorted position array of all turtles. Reduce converts the list back to an agentset
# nl.scheduleReportersAndRun(reporters, 0, 1, 100,"go")
# uav_pos = nl.getScheduledReporterResults()
while t < ticks:
    flockmates = [[] for i in range(N)]
    uav_vel = vMax * np.ones(shape=(N, 1))
    for i in range(N):
        for j in range(N):
            if i == j: continue  # avoiding computation of self distance
            delS = uav_pos[j] - uav_pos[i]  # relative distance vector S
            delSMag = np.linalg.norm(delS)

            if delSMag < flockVision:
                flockmates[i].append(j)

    for i in range(N):
        avg_head = 0
        if np.any(abs(uav_pos[i]) > 0.85 * xMax):   #obstacle avoidance
            uav_head[i] = turn_towards(abs_heading(-uav_pos[i]), uav_head[i], maxAvoidTurn)
        elif flockmates[i]:
            # print(i, flockmates[i])
            separate(flockmates[i])
            for k in flockmates[i]:
                avg_head += uav_head[k]
            avg_head /= len(flockmates[i])
            if uav_head[i] != avg_head:
                align(avg_head)

            # if delSMag < flockVision and uav_head[i] is not np.round(uav_head[j]):
        #     print("2", delSMag)
        #     align()
        # cohere()

            # [uav_vel[i], uav_head[i]] = turnAndSlowDown(uav_vel[i], maxAvoidTurn, 0.5)
        uav_headvec = np.array([np.sin(math.radians(uav_head[i])), np.cos(math.radians(uav_head[i]))])
        # v_cap = np.array([0, 1])
        uav_pos[i] = uav_pos[i] + uav_headvec * uav_vel[i]
        nl.command('ask turtle {0} [setxy {1} {2} set heading {3}]'.format(i, uav_pos[i][0], uav_pos[i][1],
                                                                           float(uav_head[i])))
    nl.command('tick')
    t = t + 1

    # time.sleep(0.05)
    # print(nl.report('[list xcor ycor] of turtle 0'))

''' PSEDUCODE
initialise i random uavs
for i upto iterations
    for i upto uavs
        move forward
        seperate
        align
        cohere

def seperate
    if distance<min seperate
        turn heading by max seperate turn

def cohere
    calc COM_flock
    move heading by max cohere turn

def align
    get average heading of flock
    turn by max algin turn in thi direction
    '''
