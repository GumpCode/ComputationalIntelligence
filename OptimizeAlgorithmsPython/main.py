#!/usr/bin/python
# -*- coding: UTF-8 -*-

# **********************************************************
# * Author        : Gump from CQU
# * Email         : gumpglh@qq.com
# * Create time   : 2016-05-15 20:11
# * Last modified : 2016-05-16 00:51
# * Filename      : main.py
# * Description   : solver of problem
# * Copyright © Gump. All rights reserved.
# **********************************************************

import numpy as np
from GA import GA
from Problem import CVRP
import copy

CustomerDistance = [[0,4,6,7.5,9,20,10,16,8], [4,0,6.5,4,10,5,7.5,11,10],
        [6,6.5,0,7.5,10,10,7.5,7.5,7.5], [7.5,4,7.5,0,10,5,9,9,15],
        [9,10,10,10,0,10,7.5,7.5,10], [20,5,10,5,10,0,7,9,7.5],
        [10,7.5,7.5,9,7.5,7,0,7,10], [16,11,7.5,9,7.5,9,7,0,10],
        [8,10,7.5,15,10,7.5,10,10,0]]
Requirement=[0, 1, 2, 1, 2, 1, 4, 2, 2]


def main():
    cvrp = CVRP()
    ga = GA(GeneLenght=8,PopulationCount=50,MurationRate=0.003)
    ga.initPopulation()
    population = []
    selectNum1, selectNum2, bestNum, distance = ga.selectGene(ga.population)
    population.append(ga.population[selectNum1])
    population.append(ga.population[selectNum2])
    bestGene = []
    minDistance = 1000
    minItera = 0
    for itera in range(0,5000):
        while True:
            selectNum1, selectNum2, bestNum, distance = ga.selectGene(population)
            child1, child2 = ga.cross(selectNum1, selectNum2)
            population.append(child1)
            population.append(child2)
            population = ga.muration(population)
            population.append(population[bestNum])
            if len(population) > 50:
                selectNum1, selectNum2, bestNum, distance = ga.selectGene(population)
                newPopulation = []
                newPopulation.append(population[selectNum1])
                newPopulation.append(population[selectNum2])
                newPopulation.append(population[bestNum])
                population = copy.copy(newPopulation)
                break
            if distance < minDistance:
                minDistance = distance
                bestGene = copy.copy(population[bestNum])
                minItera = itera
                fitness, finalPath = cvrp.fitnessFun(bestGene)
        print itera
        print minItera, finalPath, minDistance, fitness

if __name__ == '__main__':
    main()
