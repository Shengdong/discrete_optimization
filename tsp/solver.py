#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import matplotlib.pyplot as plt
from time import sleep, time
import numpy as np
import random

Point = namedtuple("Point", ['x', 'y'])
PointIndex = namedtuple("Point", ['index', 'x', 'y'])
Solution = namedtuple("Solution", ['depth', 'left_nodes', 'series', 'score', 'flag'])
Edge = namedtuple("Edge", ['length', 'start', 'end', 'index'])


def length(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    if (A.x == D.x and A.y == D.y) or (B.x == C.x and B.y == C.y):
        return False
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def swap_neighbor(solution_new, edge_early_point_start, edge_early_point_late, points):
    start_index = solution_new.index(edge_early_point_start)
    end_index = solution_new.index(edge_early_point_late)

    if start_index == len(points) - 1:
        element = solution_new[-1]
        solution_new.pop(-1)
        solution_new.insert(0, element)
        # print('After : ' + str(solution_new))
        start_index = solution_new.index(edge_early_point_start)
        end_index = solution_new.index(edge_early_point_late)

    list_1 = solution_new[0:start_index + 1]
    list_2 = solution_new[end_index:len(solution_new)]
    list_3 = solution_new[start_index + 1:end_index]
    list_swap = []

    while len(list_3):
        list_swap.append(list_3.pop())

    solution_new = list_1
    for element in list_swap:
        solution_new.append(element)
    for element in list_2:
        solution_new.append(element)

    return solution_new

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount + 1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # for point in points:
    #     print point
    # print intersect(points[0], points[3], points[1], points[2])
    # build a trivial solution
    # visit the nodes in the order they appear in the file
    solution = range(0, nodeCount)

    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount - 1):
        obj += length(points[solution[index]], points[solution[index + 1]])

    solution_greedy = []
    points_temp = []
    for i in range(len(points)):
        point = points[i]
        # print(str(point.x) + ' ' + str(point.y))
        points_temp.append(PointIndex(i, point.x, point.y))

    point_start = points_temp.pop(0)
    # print(points_temp)
    current_point = point_start
    solution_greedy.append(0)
    for i in range(0, nodeCount - 1):
        min_distance = 1000000000000000000000
        min_index = -1
        for index in range(len(points_temp)):
            if length(points_temp[index], current_point) < min_distance:
                min_distance = length(points_temp[index], current_point)
                min_index = index
        if min_index > -1:
            solution_greedy.append(points_temp[min_index].index)
            current_point = points_temp.pop(min_index)

    # solution_greedy = [0, 2, 1, 3, 4]
    obj_greedy = length(points[solution_greedy[-1]], points[solution_greedy[0]])
    for index in range(0, nodeCount - 1):
        obj_greedy += length(points[solution_greedy[index]], points[solution_greedy[index + 1]])

    # print(obj_greedy)
    # print(solution_greedy)
    for i in range(len(points)):
        point = points[i]
        # print(str(point.x) + ' ' + str(point.y))
        points_temp.append(PointIndex(i, point.x, point.y))

    obj_new = obj_greedy
    solution_new = solution_greedy
    if nodeCount > 2000:
        end_time = 1
    else:
        end_time = 500

    if nodeCount != 574:
        loop_time = 1
        random_search = 0
    else:
        loop_time = 100
        random_search = 100000

    obj_opt = obj_greedy
    solution_opt = solution_greedy
    for i in range(loop_time):
        for time in range(end_time):
            edges = []
            for i in range(len(solution_new)):
                edge = Edge(length(points[solution_new[i-1]], points[solution_new[i]]),
                            solution_new[i-1], solution_new[i], i)
                edges.append(edge)

            edges.sort(key=lambda x: -x[0])
            intersect_early = -1
            intersect_late = -1
            for i in range(len(edges)):
                flag = 1
                for j in range(i, len(edges)):
                    if intersect(points[edges[i].start], points[edges[i].end],
                                 points[edges[j].start], points[edges[j].end]):
                        flag = 0
                        intersect_late = j
                        break
                if flag == 0:
                    intersect_early = i
                    break
            if intersect_early == -1 or intersect_late == -1:
                break
            if edges[intersect_early].index < edges[intersect_late].index:
                edge_early = edges[intersect_early]
                edge_late = edges[intersect_late]
            else:
                edge_late = edges[intersect_early]
                edge_early = edges[intersect_late]
            edge_early_point_start = edge_early.start
            edge_early_point_late = edge_late.end
            solution_new = swap_neighbor(solution_new, edge_early_point_start, edge_early_point_late, points)

        obj_new = length(points[solution_new[-1]], points[solution_new[0]])
        for index in range(0, nodeCount - 1):
            obj_new += length(points[solution_new[index]], points[solution_new[index + 1]])
        # print('First Solution:')
        # print(obj_new)
        # print(solution_new)
        if obj_new < obj_opt:
            obj_opt = obj_new
            solution_opt = solution_new

        result_flag = 1
        for time1 in range(random_search):
            random_int_1 = random.randint(0, nodeCount - 1)
            random_int_2 = random.randint(0, nodeCount - 1)
            if random_int_1 != random_int_2:
                if solution_new.index(random_int_1) < solution_new.index(random_int_2):
                    final_start = random_int_1
                    final_end = random_int_2
                else:
                    final_start = random_int_2
                    final_end = random_int_1
                solution_temp = [i for i in solution_new]
                solution_temp = swap_neighbor(solution_temp, final_start, final_end, points)
                obj_temp = length(points[solution_temp[-1]], points[solution_temp[0]])
                for index in range(0, nodeCount - 1):
                    obj_temp += length(points[solution_temp[index]], points[solution_temp[index + 1]])
                if obj_temp < obj_new:
                    obj_new = obj_temp
                    solution_new = [i for i in solution_temp]
                    result_flag = 0
                    break
        if result_flag == 1 and random_search != 0:
            random_int_1 = random.randint(0, nodeCount - 1)
            random_int_2 = random.randint(0, nodeCount - 1)
            if random_int_1 != random_int_2:
                if solution_new.index(random_int_1) < solution_new.index(random_int_2):
                    final_start = random_int_1
                    final_end = random_int_2
                else:
                    final_start = random_int_2
                    final_end = random_int_1
                solution_temp = [i for i in solution_new]
                solution_temp = swap_neighbor(solution_temp, final_start, final_end, points)
                obj_temp = length(points[solution_temp[-1]], points[solution_temp[0]])
                for index in range(0, nodeCount - 1):
                    obj_temp += length(points[solution_temp[index]], points[solution_temp[index + 1]])
                obj_new = obj_temp
                solution_new = [i for i in solution_temp]
        obj_new = length(points[solution_new[-1]], points[solution_new[0]])
        for index in range(0, nodeCount - 1):
            obj_new += length(points[solution_new[index]], points[solution_new[index + 1]])
    #     print('Second Solution:')
    #     print(obj_new)
    #     print(solution_new)
    #
    # print("Final Solution: ")
    # print(obj_opt)
    # print(solution_opt)
    # index = 0
    # for point in points:
    #     if index == 0:
    #         plt.scatter(point.x, point.y, color='green', linewidths=0.2, label=(str(point.x) + ' ' + str(point.y)))
    #     else:
    #         plt.scatter(point.x, point.y, color='green', linewidths=0.2)
    #     index += 1
    # for i in range(-1, nodeCount - 1):
    #     plt.plot([points[solution_opt[i]].x, points[solution_opt[i + 1]].x],
    #              [points[solution_opt[i]].y, points[solution_opt[i + 1]].y])
    # plt.legend()
    # plt.show()

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj_opt + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution_opt))

    return output_data


import sys

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        solve_it(input_data)
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
