#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# Code to train a single-layer neural network
# Assignment01 for Intelligent Systems
#

# (60+5 points total) Write code to train the two-layer feed-forward neural network
# with the architecture depicted in fig 2.

# The training set consists of the following data points:
#   Class 1 (t = 1): (4,2), (4,4), (5,3), (5,1), (7,2)
#   Class 2 (t = -1): (1,2), (2,1), (3,1), (6,5), (3,6), (6,7), (4,6), (7,6)
# The accompanying test set is:
#   Class 1 (t = 1): (4,1), (5,2), (3,4), (5,4), (6,1), (7,1)
#   Class 2 (t = -1): (3,2), (8,7), (4,7), (7,5), (2,3), (2,5)
# This network uses sigmoidal activation function (i.e. the logistic function) for the
# hidden layer and linear activation for the output layer. Also, don't forget the biases
# (even though they are not shown in the image). The weights (and biases) should
# be randomly initialized from a uniform distribution in the range [-0.1, 0.1].
# (a) (5 points) Plot the data. Would the network be able to solve this task if it
# had linear neurons only? Explain why.
# (b) (30 points) Implement and apply backpropagation (with nu = 1/30) until all
# examples are correctly classified. (This might take a few thousand epochs)
# (c) (10 points) Perform 10 runs with different random initializations of the weights,
# and plot the training and test error for each epoch averaged across the 10
# runs. How many epochs does it take, on average, to correctly classify all
# points. What do you notice?
# (d) (15 points) Try different learning rates nu = [1, 1/3, 1/10, 1/30, 1/100, 1/300, 1/1000]
# and plot the training error over 1000 epochs. What is the effect of varying
# the learning rate?
# (e) (Bonus: 5 points) Vary the number of hidden units (from 1 to 10) and run
# each network with 10 different random initializations. Plot the average train
# and test errors. Explain the effect of varying the number of hidden units.
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-Sep-27


## sys.exit()
import sys

## random number, random() and randrange()
import random
## e.g. use as random.randrange( -1000, 1000 ) / 1000 

## plotting library
import matplotlib.pyplot as plt

## exponent, e.g. e**val
#from math import exp
import math



def die( msg = "" ):
    print "FATAL",
    if 0 < len(str(msg)):
        print ": " + str(msg)
    sys.exit( -1 )

DEBUG = 0
#DEBUG = 1   

class Perceptron( object ):
## TODO biggest mistake, was / is not to have an explicit initialization of all
## weight matrices available with precalculated intermedeate results to check
## automated as reference if A) the implementation actually "really" works, and
## B) if and overall C) where something is broken, when working on the code


    ## overview
    _weight1matrix = [] # weights, 1st thru 2nd layer
    _weight2matrix = [] # weights, 2nd thru net layer
    _dwhistory = []     # printable history of dw
    _hiddendata = []    # hidden data
    _trainingdata = []  # training data (class 1 and 2)
    _training_targetdata = []   # targets (size of class 1 + 2)
    _testdata = []      # test set
    _test_targetdata = []
    _learningrate = [] # provided

    def __init__( self ):
        ## training set
        ##
        ## target
        ## bias
        ## x1
        ## x2

        self._trainingdata = [ [1.0, 4.0, 2.0]
                             , [1.0, 4.0, 4.0]
                             , [1.0, 5.0, 3.0]
                             , [1.0, 5.0, 1.0]
                             , [1.0, 7.0, 2.0]
                             , [1.0, 1.0, 2.0]
                             , [1.0, 2.0, 1.0]
                             , [1.0, 3.0, 1.0]
                             , [1.0, 6.0, 5.0]
                             , [1.0, 3.0, 6.0]
                             , [1.0, 6.0, 7.0]
                             , [1.0, 4.0, 6.0]
                             , [1.0, 7.0, 6.0] ]

        self._training_targetdata = [[1.0]
                                   ,[1.0]
                                   ,[1.0]
                                   ,[1.0]
                                   ,[1.0]
                                   ,[-1.0]
                                   ,[-1.0]
                                   ,[-1.0]
                                   ,[-1.0]
                                   ,[-1.0]
                                   ,[-1.0]
                                   ,[-1.0]
                                   ,[-1.0]]

        self._testdata         = [[1.0, 4.0, 1.0]
                                  , [1.0, 5.0, 2.0]
                                  , [1.0, 3.0, 4.0]
                                  , [1.0, 5.0, 4.0]
                                  , [1.0, 6.0, 1.0]
                                  , [1.0, 7.0, 1.0]
                                  , [1.0, 3.0, 2.0]
                                  , [1.0, 8.0, 7.0]
                                  , [1.0, 4.0, 7.0]
                                  , [1.0, 7.0, 5.0]
                                  , [1.0, 2.0, 3.0]
                                  , [1.0, 2.0, 5.0]]


        self._test_targetdata     = self._training_targetdata

        self._hiddendata = [[0.0, 0.0, 0.0]] ## original
#        self._hiddendata = [[0.0, 0.0, 0.0, 0.0]] ## 4 hidden nodes  
#        self._hiddendata = [[0.0, 0.0, 0.0, 0.0, 0.0]] ## 5 hidden nodes  
#        self._hiddendata = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]] ## 10 hidden nodes  


        ## 1. layer weights
        nhidden = len(self._hiddendata[0])
        ninput = len(self._trainingdata[0])
        self._weight1matrix = self._initweights( ninput, nhidden)
        self._weight1matrix = self.mat_transpose( self._weight1matrix )

        ## 2. layer weights
        nhidden = len(self._hiddendata[0])
        ny = 1
        self._weight2matrix = self._initweights( nhidden, ny)

        ## learningrate nu
        ## 1.0, 1.0/3.0, 1.0/10.0, 1.0/30.0, 1.0/100.0, 1.0/300.0, 1.0/1000.0
#        self._learningrate = 1.0
#        self._learningrate = 1.0/3.0
#        self._learningrate = 1.0/10.0
        self._learningrate = 1.0/30.0
#        self._learningrate = 1.0/100.0
#        self._learningrate = 1.0/300.0
#        self._learningrate = 1.0/1000.0

        ## history per weight entry
        self._dwhistory = []

        for y in range(0, len(self._weight1matrix)):
            for x in range(0, len(self._weight1matrix[0])):
                self._dwhistory.append( [self._weight1matrix[y][x]] )

        for y in range(0, len(self._weight2matrix)):
            for x in range(0, len(self._weight2matrix[0])):
                self._dwhistory.append( [self._weight2matrix[y][x]] )


    def snapshot( self ):
        ## class data: dots
        class1x = self._trainingset[1][:6]
        class1y = self._trainingset[2][:6]
        plt.plot( class1x, class1y, 'ro' )
        class2x = self._trainingset[1][6:]
        class2y = self._trainingset[2][6:]
        plt.plot( class2x, class2y, 'bo' )

        xAxisMax = max(class1x + class2x)+1
        xAxisMin = min(class1x + class2x)-1
        yAxisMax = max(class1y + class2y)+1
        yAxisMin = min(class1y + class2y)-1
        plt.axis( [xAxisMin, xAxisMax, yAxisMin, yAxisMax] )

        plt.xlabel('X1')
        plt.ylabel('X2')
        plt.show()


    def snapshot_learning( self ):
        for idx in range(0, len(self._dwhistory)):
#            print "plot " + str(idx) ## debugging  
            plt.plot( self._dwhistory[idx] )
#            plt.show() ## debugging  
#        return ## debugging  
        plt.xlabel('time')
        plt.ylabel('error')
        plt.show()


    def _initweights( self, nsource, ntarget):
        weightmatrix = []
        for h in range(0, nsource):
#        for h in range(0, ntarget): 
            tmp = []
            for x in range(0, ntarget):
#            for x in range(0, nsource): 
                tmp += [random.randrange(-100, 100) / 1000.0]
            weightmatrix.append(tmp)
        return weightmatrix


    def sigma( self, mat ):
        if 1 == DEBUG: print ""
        if 1 == DEBUG: self.mat_show( mat )
        if 1 == DEBUG: print "sigma"
        res = []
        for y in range(0, len(mat)):
            tmp = []
            for x in range(0, len(mat[0])):
                tmp += [1/(1 + math.exp(mat[y][x]))]
            res.append(tmp)
        if 1 == DEBUG: print "="
        if 1 == DEBUG: self.mat_show( res )
        return res

    def revsigma( self, mat ):
        if 1 == DEBUG: print ""
        if 1 == DEBUG: self.mat_show( mat )
        if 1 == DEBUG: print "revsigma"
        ## revsigma = sigma(x) * (1 - sigma(x))
        sigmat = self.sigma(mat)
        ## sigma*sigma
        res = []
        for y in range(0,len(sigmat)):
            tmp = []
            for x in range(0, len(sigmat[0])):
                tmp += [sigmat[y][x] * sigmat[y][x]]
            res.append(tmp)

        ## -(sigma*sigma)
        res = self.mat_factorize( -1, res )
        ## sigma - (sigma*sigma) == sigma * (1 - sigma)
        if 1 == DEBUG: print "="
        if 1 == DEBUG: self.mat_addition( sigmat, res )
        return res

    def mat_multiplication( self, a, b ):
        if 1 == DEBUG: print ""
        if 1 == DEBUG: self.mat_show( a )
        if 1 == DEBUG: print "x"
        if 1 == DEBUG: self.mat_show( b )

        aylen = len( a )
        axlen = len( a[0] )

        bylen = len( b )
        bxlen = len( b[0] )

        ## safety
        if axlen != bylen: raise Exception("matrix multiplication: nonconformat arguments")

        cylen = aylen
        cxlen = bxlen

        ## init c
        c = []
        for y in range(0, cylen):
            row = []
            for x in range(0, cxlen):
                row += [0]
            c.append( row )

        ## matrix matrix multiplication, brute force
        for ay in range(0,aylen):

            for bx in range(0,bxlen):
                tmp = 0
                for xy in range(0,bylen):
                    tmp += a[ay][xy] * b[xy][bx]
                c[ay][bx] = tmp

        if 1 == DEBUG: print "="
        if 1 == DEBUG: self.mat_show( c )
        return c

    def mat_factor_multiplication( self, a, b):
        if 1 == DEBUG: print ""
        if 1 == DEBUG: self.mat_show( a )
        if 1 == DEBUG: print "factor-multiplication"
        if 1 == DEBUG: self.mat_show( b )
        if len(a) != len(b): raise Exception("mat_factor_multiplication - different y lenghts")
        if len(a[0]) != len(b[0]): raise Exception( "mat_factor_multiplication - different x lengths")
        res = []
        for y in range(0, len(a)):
            tmp = []
            for x in range(0, len(a[0])):
                tmp += [a[y][x] * b[y][x]]
            res.append(tmp)
        if 1 == DEBUG: print "="
        if 1 == DEBUG: self.mat_show( res )
        return res

    def mat_transpose( self, mat ):
        if 1 == DEBUG: print ""
        if 1 == DEBUG: self.mat_show( mat )
        if 1 == DEBUG: print "transpose"
        trans = []
        for y in range(0, len(mat[0])):
            tmp = []
            for x in range(0, len(mat)):
                tmp += [mat[x][y]]
            trans.append(tmp)
        if 1 == DEBUG: self.mat_show( trans )
        return trans

    def mat_addx( self, a, b ):
        if 1 == DEBUG: print ""
        if 1 == DEBUG: self.mat_show( a )
        if 1 == DEBUG: print "addx"
        if 1 == DEBUG: self.mat_show( b )
        if len(a) != len(b): raise Exception("mat_addx failed, different sizes")
        c = []
        for y in range(0,len(a)):
            c.append( a[y] + b[y] )
        if 1 == DEBUG: print "="
        if 1 == DEBUG: self.mat_show( c )
        return c

    def mat_addy( self, a, b ):
        if 1 == DEBUG: print ""
        if 1 == DEBUG: self.mat_show( a )
        if 1 == DEBUG: print "addy"
        if 1 == DEBUG: self.mat_show( b )
        if len(a[0]) != len(b[0]): raise Exception("mat_addy failed: different sizes")
        c = [i for i in a]
        c += [i for i in b]
        if 1 == DEBUG: print "="
        if 1 == DEBUG: self.mat_show( c )
        return c

    def mat_addition( self, a, b ):
        if 1 == DEBUG: print ""
        if 1 == DEBUG: self.mat_show( a )
        if 1 == DEBUG: print "addition"
        if 1 == DEBUG: self.mat_show( b )
        if len(a) != len(b): raise Exception("mat_addition failed: not implemented for different sizes")
        c = []
        for y in range(0, len(a)):
            tmp = []
            for x in range(0, len(a[0])):
                tmp += [a[y][x] + b[y][x]]
            c.append(tmp)
        if 1 == DEBUG: print "="
        if 1 == DEBUG: self.mat_show( c )
        return c

    def mat_factorize( self, fact, mat ):
        if 1 == DEBUG: print ""
        if 1 == DEBUG: print fact
        if 1 == DEBUG: print "*"
        if 1 == DEBUG: self.mat_show( mat )
        res = []
        for y in range(0, len(mat)):
            tmp = []
            for x in range(0, len(mat[0])):
                tmp += [fact * mat[y][x]]
            res.append( tmp )
        if 1 == DEBUG: print "="
        if 1 == DEBUG: self.mat_show( res )
        return res

    def mat_avg( self, old, new):
        if 1 == DEBUG: print ""
        if 1 == DEBUG: self.mat_show( old )
        if 1 == DEBUG: print "avg"
        if 1 == DEBUG: self.mat_show( new )
        if 0 == len(old): return [i for i in new]
        res = []
        for y in range(0,len(new)):
            tmp = []
            for x in range(0,len(new[0])):
                tmp += [ (old[y][x] + new[y][x]) / 2 ]
            res.append(tmp)
        if 1 == DEBUG: print "="
        if 1 == DEBUG: self.mat_show( res )
        return res

    def mat_show( self, mat ):
        for y in range(0,len(mat)):
            for x in range(0,len(mat[y])):
                print mat[y][x],
            print ""

    def update_history( self ):
        idx = 0
        for y in range(0, len(self._weight1matrix)):
            for x in range(0, len(self._weight1matrix[0])):
                self._dwhistory[idx] += [self._weight1matrix[y][x]]
                idx +=1

        for y in range(0, len(self._weight2matrix)):
            for x in range(0, len(self._weight2matrix[0])):
                self._dwhistory[idx] += [self._weight2matrix[y][x]]
                idx +=1



    def training( self ):
## init, no bias in dwlist1 connections
        current_data = self._trainingdata
        current_targetdata = self._training_targetdata

        dw1data = []
        for y in self._weight1matrix:  
            tmp=[]
            for x in self._weight1matrix[0]:  
                tmp += [0.0]
            dw1data.append(tmp)
        dw1data_history = []

        dw2data = []
        for y in self._weight2matrix[0]:
            tmp = []
            for x in self._weight2matrix:
                tmp += [0.0]
            dw2data.append( tmp )
        dw2data_history = []


## calculating net epochs
#        MAXTIME = 100
        MAXTIME = 1000    
#        MAXTIME = 2000    
#        MAXTIME = 3000    
        for epoch in range(0, MAXTIME):
            total = 0

            if MAXTIME == epoch:
                current_data = self._testdata
                current_targetdata = self._test_targetdata

## forward pass (linear)
            for idxVal in range(0, len(current_data)):
                current_input = [current_data[idxVal]]
                total += 1

## forward - layer 1
                ## hidden = sigma(input * weights1)
                self._hiddendata = self.mat_multiplication( current_input, self.mat_transpose(self._weight1matrix))
                self._hiddendata = self.sigma( self._hiddendata )

## forward - layer 2
                ## net = hidden * weights2
                net = self.mat_multiplication( self._hiddendata, self._weight2matrix )

## backward - layer 2
                ## dw2 =  delta(target - net) * learningrate * outputvalue
                delta = current_targetdata[idxVal][0] - net[0][0]
                delta *= self._learningrate
                dw2data = self.mat_factorize( delta, self._hiddendata )

## backward - layer 1
                ## dw1 = revsigma(delta_net) * learningrate * weights1
                ## multiplication with original input value can be omited (?)
                dw1tmp = self.revsigma( dw2data )
                dw1tmp = self.mat_factorize( self._learningrate, dw1tmp )
                dw1tmp = self.mat_multiplication( dw1tmp, self._weight1matrix )

                ## making a 3 x len( hidden ) matrix out of 3 value vector
                dw1matrix = self.mat_addy( dw1tmp, dw1tmp )
                for matcol in range(2, len( self._hiddendata[0])):
                    dw1matrix = self.mat_addy( dw1tmp, dw1matrix )
                dw1tmp = dw1matrix

                dw1tmp = self.mat_factor_multiplication( dw1tmp, self._weight1matrix)
                dw1data = self.mat_addition( dw1data, dw1tmp )

                ## average filter after each round
                dw1data_history = self.mat_avg( dw1data_history, dw1data)
                dw2data_history = self.mat_avg( dw2data_history, dw2data)

            ## / training set

            ## update weights after training cycle
            self._weight1matrix = self.mat_addition( self._weight1matrix, self.mat_factor_multiplication( self._weight1matrix, dw1data_history ))
            self._weight2matrix = self.mat_addition( self._weight2matrix, self.mat_factor_multiplication( self._weight2matrix, self.mat_transpose( dw2data_history )))

            ## update history for plotting
            self.update_history()
        ## / epoch


if __name__ == '__main__':
     nn = Perceptron()

## snapshot
#     nn.snapshot()

## training with test set
     nn.training()

## another snapshot
#     nn.snapshot()

## display learning curve
     nn.snapshot_learning()

print "READY."
