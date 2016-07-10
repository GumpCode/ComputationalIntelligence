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
from LoadData import LoadData
from Problem import CVRP
import copy
import random
import matplotlib.pyplot as plt


def singleGA(populationCount, crossRate, murationRate, iteraNum, filename):
    cvrp = CVRP()
    name, dimension, capacity, CustomerDistance, Requirement = LoadData(filename)
    ga = GA(GeneLenght=(dimension-1), PopulationCount=populationCount, CrossRate=crossRate, MurationRate=murationRate, DistanceMat=CustomerDistance, Requirement=Requirement, Capacity=capacity)
    ga.initPopulation()
    population = copy.copy(ga.population)
    #population.append([21, 31, 19, 17, 13, 7, 26, 12, 1, 16, 30, 27, 24, 29, 18, 8, 9, 22, 15, 10, 25, 5, 20, 14, 28, 11, 4, 23, 3, 2, 6])
    bestGene = []
    minDistance = 100000
    minItera = 0
    for itera in range(iteraNum):
        newPopulation = []
        while True:
            selectNum1, selectNum2, bestNum, distance, bestPath, bestFit = ga.selectGene(population)
            child1, child2 = ga.cross(selectNum1, selectNum2)
            newPopulation.extend(ga.muration([child1, child2]))
            if len(newPopulation) > populationCount:
                newPopulation.append(population[bestNum])
                bestGene = copy.copy(population[bestNum])
                if distance < minDistance:
                    minItera = itera
                    minDistance = distance
                    population = copy.copy(newPopulation)
                break
        print minItera, bestPath, minDistance, bestFit
    return minItera, bestPath, minDistance, bestFit


def doubleGA(populationCount, crossRate1, murationRate1, crossRate2, murationRate2, iteraNum, filename):
    cvrp = CVRP()
    name, dimension, capacity, CustomerDistance, Requirement = LoadData(filename)
    ga1 = GA(GeneLenght=(dimension-1), PopulationCount=populationCount, CrossRate=crossRate1, MurationRate=murationRate1, DistanceMat=CustomerDistance, Requirement=Requirement, Capacity=capacity)
    ga2 = GA(GeneLenght=(dimension-1), PopulationCount=populationCount, CrossRate=crossRate2, MurationRate=murationRate2, DistanceMat=CustomerDistance, Requirement=Requirement, Capacity=capacity)
    ga1.initPopulation()
    ga2.initPopulation()
    population1 = copy.copy(ga1.population)
    population2 = copy.copy(ga2.population)
    bestGene = []
    minDistance = 100000
    minItera = 0
    for itera in range(0,iteraNum):
        newPopulation1 = []
        newPopulation2 = []
        while True:
            #选择两个父亲，生成两个子代后变异放入新种群
            selectNum1, selectNum2, bestNum1, distance1, bestPath1, bestFit1 = ga1.selectGene(population1)
            child1, child2 = ga1.cross(selectNum1, selectNum2)
            newPopulation1.extend(ga1.muration([child1, child2]))

            selectNum1, selectNum2, bestNum2, distance2, bestPath2, bestFit2 = ga2.selectGene(population2)
            child1, child2 = ga2.cross(selectNum1, selectNum2)
            newPopulation2.extend(ga2.muration([child1, child2]))
            #当数量超过设定值，交换两个平行种群的解
            if len(newPopulation1) > populationCount:
                selectNum1, selectNum2, bestNum1, distance1, bestPath1, bestFit1 = ga1.selectGene(newPopulation1)
                selectNum1, selectNum2, bestNum2, distance2, bestPath2, bestFit2 = ga2.selectGene(newPopulation2)
                exPopulation1 = []
                exPopulation2 = []
                exNum1 = range(len(newPopulation1)-1)
                exNum2 = range(len(newPopulation2)-1)
                random.shuffle(exNum1)
                random.shuffle(exNum2)
                exPopulation1.append(newPopulation2[bestNum2])
                exPopulation2.append(newPopulation1[bestNum1])
                num = random.randint(5,len(newPopulation1)-5)
                count = 0
                for i in range(len(newPopulation1)):
                    if i != bestNum1:
                        if i in exNum1:
                            if count < num:
                                exPopulation2.append(newPopulation1[i])
                            else:
                                exPopulation1.append(newPopulation1[i])
                        else:
                            exPopulation1.append(newPopulation1[i])
                        count = count + 1
                if newPopulation1[bestNum1] in exPopulation1:
                    exPopulation1.remove(newPopulation1[bestNum1])

                count = 0
                for i in range(len(newPopulation2)):
                    if i != bestNum2:
                        if i in exNum2:
                            if count < num:
                                exPopulation1.append(newPopulation2[i])
                            else:
                                exPopulation2.append(newPopulation2[i])
                        else:
                            exPopulation2.append(newPopulation2[i])
                        count = count + 1
                if newPopulation2[bestNum2] in exPopulation2:
                    exPopulation2.remove(newPopulation2[bestNum2])

                if distance1 < minDistance:
                    minItera = itera
                    minDistance = distance1
                    bestFit = bestFit1
                    bestPath =copy.copy(bestPath1)
                if distance2 < minDistance:
                    minItera = itera
                    minDistance = distance2
                    bestFit = bestFit2
                    bestPath =copy.copy(bestPath2)
                Population1 = copy.copy(exPopulation1)
                Population2 = copy.copy(exPopulation2)
                break
        print minItera, bestPath, minDistance, bestFit
    return minItera, bestPath, minDistance, bestFit

if __name__ == '__main__':
    """
    count1 = 0
    count2 = 0
    for j in range(10):
        minItera1, finalPath1, minDistance1, fitness1 = singleGA(35, 0.8, 0.05, 300)
        minItera2, finalPath2, minDistance2, fitness2 = doubleGA(35, 0.8, 0.05, 0.9, 0.03, 300)
        count1 = minDistance1 + count1
        count2 = minDistance2 + count2
        print j
        print minItera1, finalPath1, minDistance1
        print minItera2, finalPath2, minDistance2
    print count1/10
    print count2/10
    minItera2, finalPath2, minDistance2, fitness2 = doubleGA(35, 0.9, 0.03, 0.9, 0.05, 1000, 'A-n64-k9.vrp')
    print minItera2, minDistance2
    """

    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    num = 20
    for j in range(num):
        minItera1, finalPath1, minDistance1, fitness1 = singleGA(35, 0.9, 0.1, 3000, 'A-n33-k5.vrp')
        minItera2, finalPath2, minDistance2, fitness2 = doubleGA(35, 0.9, 0.03, 0.9, 0.05, 3000, 'A-n33-k5.vrp')
        count1 = minDistance1 + count1
        count2 = minDistance2 + count2
        count3 = minItera1 + count3
        count4 = minItera2 + count4
        print minItera1, minItera2
        print minDistance1, minDistance2
    print j
    print count1/num
    print count2/num
    print count3/num
    print count4/num

    #minItera1, finalPath1, minDistance1, fitness1 = singleGA(35, 0.9, 0.1, 10, 'A-n64-k9.vrp')
    #print minDistance1


