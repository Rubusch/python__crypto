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
# Question 3.
#
# (15 points) If instead of moving N,S,E,W, the agent moves like a knight in chess (for
# example, one step North, then two steps East, in one move), how would the value of the states
# change (run Q-learning with this new action set)? So the agent now has 8 possible moves. If an
# action would take it outside the maze, it stays where it is. The probability for moving according
# to the chosen action is 72% and 4% for each of the other 7 actions.
#
#
# Q-learning
#
# Initialize Q(s,a) arbitrarily
# Repeat (for each episode):
#     Initialize s
#     Repeat (for each step of episode):
#         Choose a from s using policy derived from Q (e.g. 72% )
#         Take action a, observe r, s'
#         Q(s,a) <- Q(s,a) + alpha * [r + gamma * max_a'(Q(s',a') - Q(s,a))]
#         s <- s'
#     until s is terminal
##

## sys.exit()
import sys

## DEBUG plotting library
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

## random number generator, randrange() or random()
import random


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
    def __init__(self,maze,gamma,alfa,ystart,xstart,ygoal,xgoal):
        self._maze=maze
        self._gamma=gamma
        self._alfa=alfa
        self._xstart=xstart
        self._ystart=ystart
        self._xgoal=xgoal
        self._ygoal=ygoal

        # movements of the agent
        #
        #   NW NE
        # WN  |  EN
        #   --A--
        # WS  |  ES
        #   SW SE
        #
        #

        # directions
        self.NW=0 # North-West
        self.NE=1
        self.EN=2
        self.ES=3
        self.SE=4
        self.SW=5
        self.WS=6
        self.WN=7

        # earned reward
        self._reward=0.0

    def print_maze(self):
        for y in range(len(self._maze)):
            for x in range(len(self._maze[y])):
#                print "%.7f\t"% maze[y][x].value(), # rounded values
                print maze[y][x],"\t", # raw values
            print ""

    def isout(self, y, x):
        if y < 0: return True
        if y >= len(self._maze): return True
        if x < 0: return True
        if x >= len(self._maze[0]): return True
        if maze[y][x].iswall(): return True
        return False

    def action(self, pos):
        ## 32% = 7*4% + 4%
        ##
        ## this means, 7*4% we go into the wrong direction, plus 4% the direction is
        ## "by chance" the desired one, the 4% will be subtracted from the 72% "on purpose",
        ## which results to 68% (just a dirty hack)
        if 32 >= random.randrange(1,101):
            ## EXPLORATION
            direction = random.randrange(0,4)
        else:
            q_vals = self.next_q(pos)
            max_q = max(q_vals)

            count = q_vals.count( max_q )
            if count > 1:
                ## equal values, randomly choose one option
                tmp_q_vals=[i for i,j in enumerate(q_vals) if j == max_q]
                direction = tmp_q_vals[random.randrange(0,len(tmp_q_vals))]

            else:
                ## EXPLOITATION - go by the highest q already learned
                direction = q_vals.index( max_q )

        ## perform action
        if direction == self.NW:   pos=self.move(pos,-2,-1)
        elif direction == self.NE: pos=self.move(pos,-2, 1)
        elif direction == self.EN: pos=self.move(pos,-1, 2)
        elif direction == self.ES: pos=self.move(pos, 1, 2)
        elif direction == self.SE: pos=self.move(pos, 2, 1)
        elif direction == self.SW: pos=self.move(pos, 2,-1)
        elif direction == self.WS: pos=self.move(pos, 1,-2)
        elif direction == self.WN: pos=self.move(pos,-1,-2)
        return pos


    ## directions 0:N, 1:E, 2:S, 3:W
    def next_q(self,pos):
        q_vals = []

        # NW
        if self.isout(pos.y()-2,pos.x()-1): q_vals.append(-1.0) # wall
        else: q_vals.append( self._maze[pos.y()-2][pos.x()-1].value() )

        # NE
        if self.isout(pos.y()-2,pos.x()+1): q_vals.append(-1.0) # wall
        else: q_vals.append( self._maze[pos.y()-2][pos.x()+1].value() )

        # EN
        if self.isout(pos.y()-1,pos.x()+2): q_vals.append(-1.0) # wall
        else: q_vals.append( self._maze[pos.y()-1][pos.x()+2].value() )

        # ES
        if self.isout(pos.y()+1,pos.x()+2): q_vals.append(-1.0) # wall
        else: q_vals.append( self._maze[pos.y()+1][pos.x()+2].value() )

        # SE
        if self.isout(pos.y()+2,pos.x()+1): q_vals.append(-1.0) # wall
        else: q_vals.append( self._maze[pos.y()+2][pos.x()+1].value() )

        # SW
        if self.isout(pos.y()+2,pos.x()-1): q_vals.append(-1.0) # wall
        else: q_vals.append( self._maze[pos.y()+2][pos.x()-1].value() )

        # WS
        if self.isout(pos.y()+1,pos.x()-2): q_vals.append(-1.0) # wall
        else: q_vals.append( self._maze[pos.y()+1][pos.x()-2].value() )

        # WN
        if self.isout(pos.y()-1,pos.x()-2): q_vals.append(-1.0) # wall
        else: q_vals.append( self._maze[pos.y()-1][pos.x()-2].value() )

        return q_vals


    def move(self,pos,dy,dx):
        if self.isout(pos.y()+dy, pos.x()+dx): return pos

        ## Q update
        q_old = pos.value()
        q_next = self._maze[pos.y()+dy][pos.x()+dx].value()
        alfa = self._alfa
        reward = pos.reward()
        gamma = self._gamma

        ## algorithm
        q_value = q_old + alfa * (reward + gamma * max(self.next_q(pos)) - q_old)

        ## store q value
        pos.setvalue(q_value)

        ## move
        pos=self._maze[pos.y()+dy][pos.x()+dx]
        return pos


    def q_learning(self):

        ## episode counts
        episodes = 0

        cnt=0
        while True:

            ## (re)start
            pos = maze[self._ystart][self._xstart]

            for idx in range(100):
                ## "...each episode ends after 100 actions or once the goal has been reached"
                pos=self.action(pos)

                if self._ygoal==pos.y() and self._xgoal==pos.x():
                    break

            ## break out, after x runs
            if 100 == cnt: break
            cnt += 1

            ## count episodes
            episodes += 1


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
    ystart=2
    xstart=2
    ygoal=5
    xgoal=7
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
            if x==xgoal and y==ygoal: pos.setreward(10)

            line += [pos]
        maze.append(line)

    ## start algorithm

    ## Exercise 3)
    print "Exercise 3)"
    gamma=0.9
    alfa=0.4
    agent=Agent(maze,gamma,alfa,ystart,xstart,ygoal,xgoal)
    agent.q_learning();
    agent.print_maze()

    agent.DEBUG_plot(10)

    print "READY."
