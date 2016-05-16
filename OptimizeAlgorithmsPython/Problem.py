#!/usr/bin/python
# -*- coding: UTF-8 -*-

# **********************************************************
# * Author        : Gump from CQU
# * Email         : gumpglh@qq.com
# * Create time   : 2016-05-15 20:11
# * Last modified : 2016-05-16 00:51
# * Filename      : Problem.py
# * Description   : solver of problem
# * Copyright © Gump. All rights reserved.
# **********************************************************

import numpy as np

CustomerDistance = [[0,4,6,7.5,9,20,10,16,8], [4,0,6.5,4,10,5,7.5,11,10],
        [6,6.5,0,7.5,10,10,7.5,7.5,7.5], [7.5,4,7.5,0,10,5,9,9,15],
        [9,10,10,10,0,10,7.5,7.5,10], [20,5,10,5,10,0,7,9,7.5],
        [10,7.5,7.5,9,7.5,7,0,7,10], [16,11,7.5,9,7.5,9,7,0,10],
        [8,10,7.5,15,10,7.5,10,10,0]]
Requirement=[0, 1, 2, 1, 2, 1, 4, 2, 2]


class CVRP(object):
    def fitnessFun(self, gene):
        distance = 0.0
        load = 0
        finalPath = []
        for num in range(len(gene)):
            load = load + Requirement[gene[num]]
            if num == 0:
                distance = distance + float(CustomerDistance[gene[num]][0])
                finalPath.append(0)
            if num is not len(gene)-1:
                if load > 8:
                    load = Requirement[gene[num]]
                    distance = distance + float(CustomerDistance[0][gene[num-1]]) + float(CustomerDistance[0][gene[num]])
                    distance = distance - float(CustomerDistance[gene[num]][gene[num -1]])
                    distance = distance + float(CustomerDistance[gene[num]][gene[num +1]])
                    finalPath.append(0)
                    finalPath.append(0)
                    finalPath.append(gene[num])
                else:
                    distance = distance + float(CustomerDistance[gene[num]][gene[num +1]])
                    finalPath.append(gene[num])
            elif num == len(gene)-1:
                    distance = distance + float(CustomerDistance[gene[num]][0])
                    finalPath.append(gene[num])
                    finalPath.append(0)
        return 1.0/distance, finalPath
