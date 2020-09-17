#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# Assignment05 for Intelligent Systems
#
#
# Question 1.
#
# Implement a binary Genetic Algorithm that uses fitness proportional selection,
# 1-point crossover, and bit-flip mutation to solve the problem in which the
# fitness is the number of 1s in the chromosome, i.e. the optimal solution is
# the chromosome where all genes are set to 1.
#
# A. (40 points) Run the algorithm 10 times for each of the four following
# versions of the problem:
# l = 5, 10, 20, 50, where l is the length of the chromosomes. Vary the
# population size and mutation rate to obtain good results (fast solution).
#
# B. (10 points) Plot the best fitness in each generation (averaged over the 10
# runs), for each of the four problems. There should be one graph with four
# curves, the x-axis being the generations, and the y-axis the average (best)
# fitness.
#
#
# author: Lothar Rubusch
# email: l.rubusch@gmx.ch


import random # randrange()

import sys # sys.exit()

import matplotlib.pyplot as plt # plotting

def die( msg = "" ):
    print "FATAL",
    if 0 < len(str(msg)):
        print ": " + str(msg)
    sys.exit( -1 )


class Person(object):
    def __init__(self, chromosome=[], fitness=0, probability=0.0):
        self._chromosome=chromosome
        self._fitness=fitness
        self._probability=probability
    def chromosome(self): return self._chromosome
    def set_chromosome(self,chromosome): self._chromosome=chromosome
    def fitness(self): return self._fitness
    def set_fitness(self,fitness): self._fitness=fitness
    def probability(self): return self._probability
    def set_probability(self, probability): self._probability=probability
    def set_chromatide(self, idx, chromatide): self._chromosome[idx] = chromatide


class Genetic(object):
    def __init__(self,population_size, chromosome_size, mutation_rate):
        self.population_size=population_size
        self.chromosome_size=chromosome_size
        self.mutation_rate=mutation_rate
        self.population=[]
        self.new_population=[]
        self._run=0
        self.optimal=0

    def run(self,average=None,limit=5000):
        self._run = 0
        # 1. initialize random popolation of candidate solutions
        # create random chromosome
        self.population = [Person(chromosome=self.generate_chromosome()) for p in range(self.population_size)]

        while self.optimal==0:
            # 2. evaluate solutions on problem and assign a fitnes score
            self.evaluate()

            # 3. select some solutions for mating
            self.selection()

            # 4. recombine: create new solutions from selected ones by exchanging structure
            self.recombination()

            # 5. IF good solution not found: GOTO 2
            self.optimal = self.is_done()

            if None != average:
                total = sum([sum(p.chromosome()) for p in self.population])
                full = len(self.population) * self.chromosome_size
                average +=[(1.0*total)/full]

            self._run += 1
            if self._run == limit:
                self._run = -1 # stop after max iterations..
                break
            
        ## DEBUG
#        self.DB_population()     

        ## // while
        return self._run

    def evaluate(self):
        for idx in range(self.population_size):
            self.population[idx].set_fitness(self.get_fitness(self.population[idx].chromosome()))

    def selection(self):
        ## calculate a genotypes probability of being selected in proportion to its fitness
        for idx in range(self.population_size):
            self.population[idx].set_probability(self.compute_probability(self.population, self.population[idx].fitness()))

        ## pre-init, so that we can fall back to previous value, if none was selected by random process
        self.new_population = [Person(chromosome=p.chromosome()) for p in self.population]

        ## prepare new_population by pre-selecting genotypes with highest probability, based on random value
        idx=0
        while idx < self.population_size: # or, after 100 tries, give up, and take old one...
            # for each position in new_population choose a "likely" individual
            for jdx in range(self.population_size):
                ## get random criteria
                rnd_probability = (1.0*random.randrange(1, self.population_size)) / 10
                ## go through all population items and see by probability if one gots selected,
                ## only increment the counter if we have an item for new_population
                ## if not, go through all again
                probability = self.population[jdx].probability()
                if rnd_probability < probability:
                    ## we found an item
                    self.new_population[idx] = Person(chromosome=self.population[jdx].chromosome())
                    break
            idx+=1


    def recombination(self):
        ## mating
        self.new_population = self.crossover(self.new_population)

        ## mutation
        for idx_p in range(self.population_size):
            rate = random.randrange(0,1000) / 1000.0
            if rate < self.mutation_rate:
                ## flip a bit on mutation rate
                bit = random.randrange(0,self.chromosome_size)
                self.new_population[idx_p].set_chromatide(bit,(self.new_population[idx_p].chromosome()[bit] + 1) % 2)
            ## // if
        ## // for

    def is_done(self):
        ## doing next generation
        self.population = [Person( chromosome=elem.chromosome()) for elem in self.new_population]
        self.new_population = []
        if 0 != self.is_optimal(self.population):
            return 1
        return 0

    def generate_chromosome(self): # elements of [0;2[
        return [random.randrange(0,2) for i in range(self.chromosome_size)]

    def get_best_fitness(self, population):
        return max([population[i].fitness() for i in range(self.population_size)])/self.chromosome_size

    def get_fitness(self, chromosome):
        return sum(chromosome)

    def compute_probability(self, population, fitness):
        return (1.0 * fitness) / sum([i.fitness() for i in population])

    def crossover(self, population):
        for idx_p in range(1,self.population_size,2):
            chromosome_a=[]; chromosome_b=[]
            ## 1 point chrossover
            xo_pt=random.randrange(0,self.chromosome_size)
            for idx_c in range(self.chromosome_size):
                chromosome_a += [population[idx_p-1 if idx_c < xo_pt else idx_p].chromosome()[idx_c]]
                chromosome_b += [population[idx_p if idx_c < xo_pt else idx_p-1].chromosome()[idx_c]]
            ## init by generated chromosome
            population[idx_p-1].set_chromosome(chromosome_a)
            population[idx_p].set_chromosome(chromosome_b)
        return population

    def is_optimal(self, population):
        total = 0
        for p in population:
            total += sum(p.chromosome())
        if total == self.chromosome_size * self.population_size:
            return 1
        return 0
    
    ## debug, print the chromosomes of all population
    def DB_population(self):
        print "self.population"
        for idx in range(self.population_size):
            print "%d. individuum, fitness: '%d', probability: '%f', chromosome: "%(idx, self.population[idx].fitness(), self.population[idx].probability()),
            print '%s'%' '.join(map(str,self.population[idx].chromosome()))
        print "self.new_population"
        for idx in range(len(self.new_population)):
            print "%d. individuum, fitness: '%d', probability: '%f', chromosome: "%(idx, self.new_population[idx].fitness(), self.new_population[idx].probability()),
            print '%s'%' '.join(map(str,self.new_population[idx].chromosome()))

    def print_new_chromosome(self):
        print "Population : Chromosome"
        for idx_pop in self.population_size:
            for idx_chr in self.chromosome_size:
                print "%d\t%d"%(idx_pop, self._new_population[idx_pop].chromosome[idx_chr])
    
    def __str__(self):
        return str(self.run())


                                                                               
## MAIN
if __name__ == '__main__':

    ## exercise 1a
    population_sizes = [5,10,12]
    chromosome_sizes = [5,10,20,50]
    mutation_rates = [0.05,0.1,0.15,0.2,0.3]

    mesg = ""
    for mutation_rate in mutation_rates:
        mut = "mutation rate %f "%mutation_rate
        for population_size in population_sizes:
            pop = "population size %d "%population_size
            for chromosome_size in chromosome_sizes:
                chrom = "chromosome size %d "%(chromosome_size)
                print "%s:,"%(mut+pop+chrom),
                for run in range(10):
                    genetic = Genetic(population_size, chromosome_size, mutation_rate)
                    print "%s,"%str(genetic),
                print ""
            print ""

    ## exercise 1b
    limit=150
    plt.plot([1 for i in range(limit)], "k:", label="upper bound")
    for chromosome_size in chromosome_sizes:
        average=[]
        genetic = Genetic(10, chromosome_size, 0.15)
        genetic.run(average=average,limit=limit)
        plt.plot(average, label="chromosome size = "+str(chromosome_size))
    plt.title("avg. fitness")
    plt.ylabel("total set chromatides / all chromatides")
    plt.legend(loc="lower right")
    plt.xlabel("cycles")
    plt.show()



    print "READY."
