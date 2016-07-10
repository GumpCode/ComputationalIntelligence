#!/usr/bin/python
# -*- coding: UTF-8 -*-

# **********************************************************
# * Author        : Gump
# * Email         : gumpglh@qq.com
# * Create time   : 2016-05-14 23:19
# * Last modified : 2016-05-19 17:11
# * Filename      : GA.py
# * Description   : class of Genetic Algorithm
# * Copyright © Gump. All rights reserved.
# **********************************************************

import random
import copy
from Problem import CVRP

class GA(object):
    def __init__(self, GeneLenght, PopulationCount, CrossRate, MurationRate, DistanceMat, Requirement, Capacity):
        self.geneLenght = GeneLenght
        self.populationCount = PopulationCount
        self.population = []
        self.crossRate = CrossRate
        self.murationRate = MurationRate
        self.mindistance=0.0
        self.distanceMat = DistanceMat
        self.requirement = Requirement
        self.capacity = Capacity
        self.initPopulation()

    def initPopulation(self):
        for i in range(self.populationCount):
            gene = range(1,self.geneLenght+1)
            random.shuffle(gene)
            self.population.append(gene)

    def selectGene(self, population):
        fitnessList = []

        #compute the fitness and sum
        fitnessSum = 0.0
        maxFit = 0
        bestNum = 0
        for i in range(len(population)):
            cvrp = CVRP()
            fitness, finalPath = cvrp.fitnessFun(population[i], self.distanceMat, self.requirement, self.capacity)
            if fitness > maxFit:
                maxFit = fitness
                self.mindistance = 1/fitness
                bestNum = i
                bestPath = copy.copy(finalPath)
            fitnessList.append(fitness)
            fitnessSum = fitness + fitnessSum

        #select two gene
        breakPoint1 = random.randint(1, 10000000)* 0.0000001
        breakPoint2 = random.randint(1, 10000000)* 0.0000001
        selectNum1 = 0
        selectNum2 = 1
        fitPointList = []
        fitPoint = 0.0
        for num in range(len(fitnessList)):
            fitPoint = fitnessList[num]/fitnessSum + fitPoint
            if breakPoint1 > fitPoint:
                selectNum1 = num
                break

        for num in range(len(fitnessList)):
            fitPoint = fitnessList[num]/fitnessSum + fitPoint
            if breakPoint2 > fitPoint:
                selectNum2 = num
                break

        return selectNum1, selectNum2, bestNum, self.mindistance, bestPath, fitness

    def cross(self, selectNum1, selectNum2):
        if random.randint(1, 1000)*0.001 > self.crossRate:
            child1 = copy.copy(self.population[selectNum1])
            child2 = copy.copy(self.population[selectNum2])
        else:
            index1 = random.randint(0, self.geneLenght -3)
            index2 = random.randint(index1+1, self.geneLenght-1)

            parent1 = copy.copy(self.population[selectNum1])
            parent2 = copy.copy(self.population[selectNum2])

            #cross
            child1 = []
            child2 = []
            child1.extend(parent1[0:index1])
            child1.extend(parent2[index1:index2])
            child1.extend(parent1[index2:])
            child2.extend(parent2[0:index1])
            child2.extend(parent1[index1:index2])
            child2.extend(parent2[index2:])

            #exchange repeated elements
            repeatList1 = []
            repeatList2 = []
            for i in range(0, index1):
                for j in range(index1, index2):
                    if child1[i] == child1[j]:
                        repeatList1.append(i)
                    if child2[i] == child2[j]:
                        repeatList2.append(i)

            for i in range(index2, len(child2)):
                for j in range(index1, index2):
                    if child1[i] == child1[j]:
                        repeatList1.append(i)
                    if child2[i] == child2[j]:
                        repeatList2.append(i)

            for num in range(len(repeatList1)):
                temp = copy.copy(child1[repeatList1[num]])
                child1[repeatList1[num]] = copy.copy(child2[(len(repeatList1)-1) - repeatList2[num]])
                child2[(len(repeatList1)-1) - repeatList2[num]] = copy.copy(temp)
        return child1, child2


    def muration(self, population):
        newPopulation = []
        for gene in population:
            if random.randint(0,1000) < self.murationRate*1000:
                index1 = random.randint(0, self.geneLenght-3)
                index2 = random.randint(index1+1, self.geneLenght-1)
                gene[index1], gene[index2] = gene[index2], gene[index1]
                newPopulation.append(gene)
            else:
                newPopulation.append(gene)
        return newPopulation
