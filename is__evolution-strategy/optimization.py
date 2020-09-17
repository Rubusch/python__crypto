#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# Assignment05 for Intelligent Systems
#
#
# Question 2.
#
# Implement (1+lambda)-ES to optimize the following function:
# sum{i=1;N-1} [(1 - xi )2 + 100(xi+1 - x2 )2 ]
#
# known as the Rosenbrock function (http://en.wikipedia.org/wiki/Rosenbrock_function),
# where N is the number of dimensions, and -5 <= xi <= 10, i = 1, 2, . . . , N .
# A. (40 points) Run the algorithm 10 times for each of the following four settings, N = 5, 10, 20, 50.
# Choose your own lambda.
# B. (10 points) Plot the average fitness (over the 10 runs) of the parent in each generation for each
# N . As with question 1B, there should be four curves here.
#
#
# author: Lothar Rubusch
# email: l.rubusch@gmx.ch

import random # randrange()

import sys # sys.exit()

import matplotlib.pyplot as plt # plotting

import math # exp()

def die(msg=""):
    print "FATAL",
    if 0 < len(str(msg)):
        print ": "+str(msg)
    sys.exit(-1)


class Problem(object):
    def __init__(self, chromosome_x=[], chromosome_sigma=[], fitness=0.0):
        self.chromosome_x = chromosome_x
        self.chromosome_sigma = chromosome_sigma
        self.fitness=fitness*1.0


class Evolution(object):
    def __init__(self, ndims, noffspring):
        self.ndims = ndims
        self.noffspring = noffspring
        self.parent = Problem()
        self.offspring = [Problem() for p in range(self.noffspring)]
        self.factor = 0.5 ## TODO check if 0.5 is ok, for const factor
        self.tau=0
        self.tau_prime=0
        self._run=0


    def run(self, epsilon, limit=1000):
## 1. initialize parents and evaluate them
        self.initialization(self.parent)
        diagramvalues = []

        ## evaluate uncorrellated mutation with n sigma prime
        self.parent = self.evaluate_mutation(self.parent)

        ## compute the fitness
        self.parent.fitness = self.compute_fitness(self.parent.chromosome_x)

        self.new_parent = self.parent
        while self._run < limit:
#            print "\n%d. round"%idx
            self.parent = self.new_parent

## 5. if good solution not found go to 2
            if self.parent.fitness <= epsilon: break
            diagramvalues.append(self.parent.fitness)

## 2. create some offspring by perturbing parents with Gaussian noise according to parent's mutation parameters
            for idx_o in range(self.noffspring):
                self.offspring[idx_o] = self.evaluate_mutation(self.parent)
                self.offspring[idx_o].fitness = self.compute_fitness(self.offspring[idx_o].chromosome_x)

## 3. evaluate offspring
            ## find the minimum fitness in offspring and parent
            fitnesslist = [o.fitness for o in self.offspring] + [self.parent.fitness]
            idx_min = fitnesslist.index(min(fitnesslist))

## 4. select new parents from offspring and possibly old parents
            self.new_parent = self.parent if idx_min == (len(fitnesslist)-1) else self.offspring[idx_min]

            self._run+=1
        ## // while

                                                                 
        self.DB_print(self.parent, "\n%d. round: selected"%self._run)
                                                                 
        return diagramvalues


    def initialization(self, problem):
        ## initialize the parents chromosome to the values -5 <= x < 11
        problem.chromosome_x = [1.0 * random.randrange(-5, 11) for i in range(self.ndims)]
        problem.chromosome_sigma = [1.0 for i in range(self.ndims)]

    def evaluate_mutation(self, element):
        beta = random.gauss(mu=0.0, sigma=self.tau_overall())
        chromosome_sigma = [s for s in element.chromosome_sigma]
        chromosome_x = [x for x in element.chromosome_x]
        for idx in range(len(self.parent.chromosome_x)):
            chromosome_sigma[idx] *= math.exp(beta + random.gauss(mu=0.0, sigma=self.tau_coordinate()))
            chromosome_x[idx] += random.gauss(mu=0.0, sigma=chromosome_sigma[idx])
        return Problem(chromosome_x=chromosome_x, chromosome_sigma=chromosome_sigma, fitness=element.fitness)

    def tau_overall(self):
        if self.tau == 0: self.tau = self.factor / math.sqrt(2*self.ndims)
        return self.tau

    def tau_coordinate(self):
        if self.tau_prime == 0.0:
            self.tau_prime = self.factor / math.sqrt(2*math.sqrt(self.ndims))
        return self.tau_prime

    def compute_fitness(self, chromosome_x):
        fitness=0.0
        for idx in range(self.ndims-1):
            x = chromosome_x[idx]
            x_next = chromosome_x[idx+1]
            fitness += math.pow((1.0-x), 2) + 100.0 * math.pow((x_next + math.pow(x,2)), 2)
        return fitness*1.0

    def DB_print(self, element, name):
        print name
        print "\tchromosome_x:\t\t",
        print [str(x) for x in element.chromosome_x]
        print "\tchromosome_sigma:\t",
        print [str(s) for s in element.chromosome_sigma]
        print "\tfitness:\t\t",
        print element.fitness
        print ""




                                                                               
## MAIN
if __name__ == '__main__':
    ndims = [5,10,20,50]
    noffspring = 20 # lambda value
    limit=5000
    epsilon=10

    for ndim in ndims:
        dataset = []

        evolution = Evolution(ndim, noffspring)
        data = evolution.run(epsilon, limit)

        evolution = Evolution(ndim, noffspring)
        datb = evolution.run(epsilon, limit)

        evolution = Evolution(ndim, noffspring)
        datc = evolution.run(epsilon, limit)

        evolution = Evolution(ndim, noffspring)
        datd = evolution.run(epsilon, limit)

        evolution = Evolution(ndim, noffspring)
        date = evolution.run(epsilon, limit)

        evolution = Evolution(ndim, noffspring)
        datf = evolution.run(epsilon, limit)

        evolution = Evolution(ndim, noffspring)
        datg = evolution.run(epsilon, limit)

        evolution = Evolution(ndim, noffspring)
        dath = evolution.run(epsilon, limit)

        evolution = Evolution(ndim, noffspring)
        dati = evolution.run(epsilon, limit)

        evolution = Evolution(ndim, noffspring)
        datj = evolution.run(epsilon, limit)

        minlen = min(len(data), len(datb), len(datc), len(datd), len(date), len(datf), len(datg), len(dath), len(dati), len(datj))

        for idx in range(minlen):
            dataset += [sum([data[idx], datb[idx], datc[idx], datd[idx], date[idx], datf[idx], datg[idx], dath[idx], dati[idx], datj[idx]])/minlen]
        plt.plot(dataset,label="N = %d"%ndim)

#    plt.plot(self.diagramvalues)
    plt.legend(loc="upper right")
    plt.title("avg. fitness")
    plt.ylabel("total fitness")
    plt.xlabel("cycles")
    plt.xlim(0,10)
    plt.show()

    print "READY."
