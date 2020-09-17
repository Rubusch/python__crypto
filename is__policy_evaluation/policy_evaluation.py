#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# Assignment04 for Intelligent Systems
#
# author: Lothar Rubusch
# email: l.rubusch@gmx.ch
#
#
# Given:
#
#     x0123456x
#    y#########
#    0#.......#
#    1#.S#....#
#    2#.##....#
#    3#..#..#.#
#    4#.....#G#
#    y#########
#
# Figure 1: 30-State Maze. For all questions refer to this figure. The agent has
# four possible actions: North, South, East, West. When the agent takes an
# action, it goes to the adjacent state in the chosen direction with probability
# 0.70, and in one of the other directions with probability 0.30. For example,
# if the agent chooses North, then there is a 70% chance that it actually goes
# North, a 10% chance it will go South, 10% it will go West, and 10% it will go
# East. If the agent goes in a direction that will take it outside the maze
# (e.g. going South in S), it stays in the same state. The reward r is 0 for all
# state transitions, except that when entering the goal state G the reward is
# 10.0. The discount factor gamma is set to 0.9. The agent cannot leave the goal
# state. You may number the states any way you want.
#
#
# Question 1.
#
# A. (35 points) Implement Policy Evaluation. Starting with V (s) = 0, for all
# of s, and assuming a random policy (pi(s, a) = 1/4, for all of s, a), what are
# the final values, V (s), after the evaluation has converged?
#
# B. (10 points) How and why do the values change if the discount factor, gamma
# is changed to 0.7 (again starting with V (s) = 0, for all of s)?
#
#
# Policy Evaluation Algorithm
#
#     Input pi, the policy to be evaluated
#     Initialize V(s) = 0, for all s element of S+
#     Repeat
#         delta <- 0
#         For each s element of S:
#             ny <- V(s)
#             V(s) <- sum_a{ pi(s, a) sum_s, P_ss'^a, [R_ss'^a + gamma*V(s')]
#             delta <- max( delta, |ny - V(s)|)
#     until delta < theta // (theta - a small positive number)
#     Output V ~ V^pi
##

## sys.exit()
import sys

## DEBUG plotting library
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def die( msg = "" ):
    print "FATAL",
    if 0 < len(str(msg)):
        print ": " + str(msg)
    sys.exit( -1 )

class Position( object ):
    _x = 0.0
    _y = 0.0
    _reward=0.0
    _wall=False
    _value=0.0
    def __init__( self, y, x, reward=0.0, wall=False, value=0.0):
        self._x = x
        self._y = y
        self._reward=reward
        self._wall=wall
        self._value=value

    def x(self):
        return self._x

    def y(self):
        return self._y

    def setx(self, x):
        self._x = x

    def sety(self, y):
        self._y = y

    def reward(self):
        return self._reward

    def setreward(self, reward):
        self._reward=reward
        self._value=reward

    def iswall(self):
        return self._wall

    def setwall(self):
        self._wall=True
        self._value=0.0

    def value(self):
        return self._value

    def setvalue(self,value):
        self._value=value

    def __str__(self):
        return str(self._value)



class Agent(object):
    _maze=[]
    _gamma=1.0
    _convergence=0.1
    def __init__(self, maze,gamma,convergence):
        self._maze=maze
        self._gamma=gamma
        self._convergence=convergence

    def print_maze(self):
        for y in range(len(self._maze)):
            for x in range(len(self._maze[y])):
#                print "%.7f\t"% maze[y][x].value(), # rounded values
                print maze[y][x],"\t", # raw values
            print ""

    def isout(self, y, x):
        if maze[y][x].iswall(): return True
        return False

    def direction(self,pos,dy,dx,pdir,delta,value):
        gamma = self._gamma

        ## check if s' is out
        if self.isout( pos.y()+dy, pos.x()+dx): return delta,value
        ny = pos.value()
        reward = pos.reward()
        nextValue = maze[pos.y()+dy][pos.x()+dx].value()
        value += 0.25 * pdir * (reward + gamma * nextValue)
        return delta,value


    def updatestate(self,pos,dy,dx,delta,value):
        ## 2. permutation by probability towards a specified direction
        if 0 == dy and 1 == dx: delta,value=self.direction(pos,dy,dx,0.7,delta,value)
        else: delta,value=self.direction(pos,dy,dx,0.1,delta,value)

        if 1 == dy and 0 == dx: delta,value=self.direction(pos,dy,dx,0.7,delta,value)
        else: delta,value=self.direction(pos,dy,dx,0.1,delta,value)

        if 0 == dy and -1 == dx: delta,value=self.direction(pos,dy,dx,0.7,delta,value)
        else: delta,value=self.direction(pos,dy,dx,0.1,delta,value)

        if -1 == dy and 0 == dx: delta,value=self.direction(pos,dy,dx,0.7,delta,value)
        else: delta,value=self.direction(pos,dy,dx,0.1,delta,value)
        return delta,value

    def policy_evolution(self):
        cnt=0
        while True:
            ## init delta per round
            delta = 0

            ## foreach position s element of S
            for y in range(len(self._maze)):
                for x in range(len(self._maze[y])):

                    ## load value for next round
                    value = 0

                    ## check if s is out
                    if self.isout(y,x): continue

                    ## 1. permutation by possible directions
                    delta,value=self.updatestate(maze[y][x], 0, 1, delta,value)
                    delta,value=self.updatestate(maze[y][x], 0,-1, delta,value)
                    delta,value=self.updatestate(maze[y][x], 1, 0, delta,value)
                    delta,value=self.updatestate(maze[y][x],-1, 0, delta,value)

                    ## compare differences after 4 x 4 permuted additions
                    ny = maze[y][x].value()
                    delta = max(delta, abs(ny-value)) # max( delta, | ny - value | )

                    ## store resulting value
                    maze[y][x].setvalue(value)

            ## check delta
            print "%d. iteration, delta: %.7f > %.7f" % (cnt,delta,self._convergence)
            if delta < self._convergence:
                print "STOP"
                break

            ## increment loop iteration
            cnt+=1

        ## // while


## DEBUG printouts
    ## boundary - cuts off very high values
    def DEBUG_plot(self,boundary=1.0):
        xs = []; xb = []
        ys = []; yb = []
        zs = []; zb = []
        for y in range(len(self._maze)):
            for x in range(len(self._maze[y])):
                if self.isout(y,x):
                    xb.append(x)
                    yb.append(-y)
                    zb.append(0.0)
                else:
                    val = str(maze[y][x])
                    if float(val) >= boundary:
                        zs.append( boundary )
                    else:
                        zs.append( float(val) ) ## take default  by Position str()
                    xs.append(x)
                    ys.append(-y)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(xs,ys,zs,s=50,c="#FFD700") # values, yellow
        ax.scatter(xb,yb,zb,s=100,c="#838B8B") # boundary

        ## log scale does not work, strange
#        ax.set_yscale('log')
#        plt.yscale('log')

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.show()
## // DEBUG printouts
        



if __name__ == '__main__':

    ymax = 5 + 2
    xmax = 7 + 2
    LIMIT = 7 #digits

    ## initialize V(s)=0 for all elements of S(maze)
    maze=[]
    for y in range(ymax):
        line=[]
        for x in range(xmax):
            pos = Position(y,x)

            ## set boundaries
            if y == 0 or y == ymax-1: pos.setwall()
            if x == 0 or x == xmax-1: pos.setwall()

            ## set inside borders
            if x==3 and y==2: pos.setwall()
            if x==2 and y==3: pos.setwall()
            if x==3 and y==3: pos.setwall()
            if x==3 and y==4: pos.setwall()
            if x==6 and y==4: pos.setwall()
            if x==6 and y==5: pos.setwall()

            ## goal
            if x==7 and y==5: pos.setreward(10)

            line += [pos]
        maze.append(line)

    ## start algorithm

    ## Exercise 1a)
    print "Exercise 1a) gamma=0.9"
    gamma = 0.9
    agent=Agent(maze, gamma, 0.1**LIMIT)
    agent.policy_evolution()
    agent.print_maze()

    agent.DEBUG_plot(1.0) # for plotting, uncomment imports on top   

    ## Exercise 1b)
    print "Exercise 1b) gamma=0.7"
    gamma = 0.7
    agent=Agent(maze, gamma, 0.1**LIMIT)
    agent.policy_evolution()
    agent.print_maze()

    agent.DEBUG_plot(1.0)  

    print "READY."
