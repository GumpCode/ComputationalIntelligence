#!/usr/bin/python
# -*- coding: UTF-8 -*-

# **********************************************************
# * Author        : Gump from CQU
# * Email         : gumpglh@qq.com
# * Create time   : 2016-05-19 08:44
# * Last modified : 2016-05-19 10:46
# * Filename      : LoadData.py
# * Description   :
# * Copyright © Gump. All rights reserved.
# **********************************************************

import copy
import math

def LoadData(dirName):
    with open(dirName, 'r') as file:
        item = []
        node_coord = []
        nodeFlag = False
        demand = []
        demandFlag = False
        for line in file.readlines():
            item = line.strip('\n').strip('\r').split(' ')
            if item[0] == 'NAME':
                name = item[2]
            elif item[0] == 'DEPOT_SECTION':
                nodeFlag = False
                demandFlag = False
            elif item[0] == 'DIMENSION':
                dimension = int(item[2])
            elif item[0] == 'CAPACITY':
                capacity = int(item[2])
            elif item[0] == 'NODE_COORD_SECTION':
                nodeFlag = True
            elif item[0] == 'DEMAND_SECTION':
                nodeFlag = False
                demandFlag = True
            elif (nodeFlag == True) & (item[0] == ''):
                node_coord.append([float(item[2]), float(item[3])])
            elif (demandFlag == True) & (item[0] != ''):
                demand.append(int(item[1]))

    distance = [[0 for k in range(dimension)] for i in range(dimension)]
    for i in range(dimension):
        for j in range(dimension):
            distance[i][j] = int(math.sqrt(math.pow((node_coord[i][0]-node_coord[j][0]),2)+math.pow((node_coord[i][1]-node_coord[j][1]),2)))
    return name, dimension, capacity, distance, demand
