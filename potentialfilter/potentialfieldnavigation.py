#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01
#
# REMARK: the solution is not printed in a graph, but only the coordinates of
# the path are printed on screen
# (did this implementation in the train w/o internet access to lookup the coorect
# function name)

#import math
from math import *
import sys

## 3D plotting
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

## globals

## size of robot = 7
#XSIZE=300 / 7
XSIZE=43
#YSIZE=200 / 7
YSIZE=29
XMAX=XSIZE-1
YMAX=YSIZE-1

## [ y x ]
GOAL=[YMAX, XMAX]
START=[0, 0]

## init matrix
def get_matrix():
    M = []
    M += [[0 for x in range(XSIZE)] for y in range(YSIZE)]
    return M

## distance
def distance( pktsrc, pktdst ):
    dist = 0
    dists=[]
    try:
        for elem in pktdst:
            dy = pktsrc[0] - elem[0]
            dx = pktsrc[1] - elem[1]
            dists += [sqrt(dx**2 + dy**2)]
        dist = min(dists[:])
    except TypeError:
        dy = int(pktsrc[0]) - int(pktdst[0])
        dx = int(pktsrc[1]) - int(pktdst[1])
        dist = sqrt(dx**2 + dy**2)
    return dist

## normalize
def normalize( M ):
    maxvals = []
    maxval = -1
    for y in range( len(M) ):
        maxvals += [max([elem for elem in M[y]])]
    maxval = max( maxvals[:] )
    try:
        for y in range( len(M) ):
            for x in range( len(M[0]) ):
                M[y][x] = M[y][x] / maxval
    except ZeroDivisionError:
        print "ERROR: maxval was zero: ", maxval
        sys.exit( -1 )

## visualization of results
def visualize( Z, solution=[]):
    Y = np.arange(0,YSIZE,1)
    X = np.arange(0,XSIZE,1)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(X, Y)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    if 0 < len( solution) :
        # TODO plot line not implemented - which function again?
        Axes3D.plot(X, Y, solution)    
    ax.set_zlim(0.0, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

## obstacle
def obstacle( M, obs ):
    k_rep = 5
    rho_zero = 20
    U_rep = 0
    U_obs = 0
    for y in range( len(M) ):
        for x in range( len(M[0]) ):
            dobs = distance( [y, x], obs )
            if 0 == dobs:
                U_rep = float(k_rep)
            else:
                U_rep = float(M[y][x]) + 0.5 * float(k_rep) * (1.0 / float(dobs) - 1.0 / float(rho_zero) )**2
                if k_rep < U_rep: U_rep = k_rep
            M[y][x] = U_rep

## repulsive_potential_field
def repulsive_potential_field( M ):
    obstcs = [[10,10],[10,20],[10,30],[10,40],  [20,10],[20,20],[20,30],[20,40], [15,35]]
    for obs in obstcs:
        obsy = obs[0]
        obsx = obs[1]
        obstacle( M, [ [obsy,obsx-1], [obsy-1,obsx], [obsy,obsx], [obsy+1,obsx], [obsy,obsx+1] ] )

## attractive_potential_field
def attractive_potential_field( M ):
    k_att = 2
    dist = 0
    for y in range( len(M) ):
        for x in range( len(M[0]) ):
            dist = distance( [y, x], GOAL )
            M[y][x] = 0.5 * float(k_att) * float(dist)**2
    return M

## merge both potential fields
def merge_potential_fields( A, B):
    ymax = min(len(A), len(B))
    xmax = min(len(A[0]), len(B[0]))
    M = get_matrix()
    for y in range( ymax ):
        for x in range( xmax ):
            M[y][x] = A[y][x] + B[y][x]
    return M


## fcn solver - backtrack
def solve( M ):
    ymax = len( M )
    xmax = len( M[0] )
    solution = [START];
    movments = {}
    while True:
        movements = {}
        y = solution[-1][0]
        x = solution[-1][1]

        ## up
        if ymax-1 > y and [y+1,x] not in solution:
            movements.update({M[y+1][x]:[y+1, x]})

        ## down
        if 0 < y and [y-1,x] not in solution:
            movements.update({M[y-1][x]:[y-1, x]})

        ## left
        if 0 < x and [y,x-1] not in solution:
            movements.update({M[y][x-1]:[y, x-1]})

        ## right
        if xmax-1 > x and [y,x+1] not in solution:
            movements.update({M[y][x+1]:[y, x+1]})

        U_next = min( movements.keys() )
        solution += [ movements.get(U_next ) ]

        if solution[-1] == GOAL:
            break

    return solution



                                                                                
## DEBUG
def DB_print( M ):
    for y in range( len(M) ):
        for x in range( len(M[0]) ):
            print "\t%.2f"%M[y][x],
        print ""

## START                                                                        
if __name__ == '__main__':
    ## attractive potential field
    U_att = get_matrix()
    attractive_potential_field( U_att )
    normalize( U_att )
    visualize( U_att )

    ## repulsing potential field
    U_rep = get_matrix()
    repulsive_potential_field( U_rep )
    normalize( U_rep )
    visualize( U_rep )

    U_merge = merge_potential_fields( U_att, U_rep)
    normalize( U_merge )
    visualize( U_merge )

    U_solution = solve( U_merge )
    ## well... 
    print "one possible solution path, following the potentials:"
    print U_solution   
#    visualize( U_merge, solution=U_solution )

#    DB_print( U_merge )   

    print "READY.",

