#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import matplotlib.pyplot as plt
from time import sleep, time

Point = namedtuple("Point", ['x', 'y'])
PointIndex = namedtuple("Point", ['index', 'x', 'y'])
Solution = namedtuple("Solution", ['depth', 'left_nodes', 'series', 'score', 'flag'])


def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    solution = range(0, nodeCount)

    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

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
    for index in range(0, nodeCount-1):
        obj_greedy += length(points[solution_greedy[index]], points[solution_greedy[index+1]])

    # print(obj_greedy)
    # print(solution_greedy)
    for i in range(len(points)):
        point = points[i]
        # print(str(point.x) + ' ' + str(point.y))
        points_temp.append(PointIndex(i, point.x, point.y))
    # print(points_temp)
    solution_root = Solution(0, [point for point in points_temp], [], 0, 1)
    solution_sets = [solution_root]
    current_opt = obj_greedy
    current_opt_series = solution_greedy
    count = 0
    while len(solution_sets):
        count += 1
        print(len(solution_sets))
        solution_sets.sort(key=lambda x: x[3]/(x[0] + 1))
        # print(count)
        # for solution in solution_sets:
        #     print(solution)

        current_solution = solution_sets.pop()
        current_left_nodes = current_solution.left_nodes
        current_flag = current_solution.flag
        if current_flag == 0:
            continue
        current_score = current_solution.score
        current_depth = current_solution.depth
        current_series = current_solution.series
        if current_depth == nodeCount and current_score + length(points[0], points[current_series[len(current_series) - 1]]) < current_opt:
            current_opt = current_score + length(points[0], points[current_series[len(current_series) - 1]])
            current_opt_series = [i for i in current_series]
            print('Yeah')
            sleep(1)

        if current_depth == 0:
            pop_point = current_left_nodes.pop(0)
            current_series.append(pop_point.index)
            solution_temp = Solution(current_depth+1, current_left_nodes, current_series, current_score, current_flag)
            solution_sets.append(solution_temp)
            # print(solution_sets)
            continue
        if current_depth < nodeCount:
            for id_x in range(len(current_left_nodes)):
                temp_points = [point for point in current_left_nodes]
                temp_series = [element for element in current_series]
                # print(temp_series)
                length_to_next_point = length(points[current_left_nodes[id_x].index], points[temp_series[len(temp_series) - 1]])
                min_index = -1
                max_index = -1
                min_x = 1000000000000000000
                max_x = -1
                for point in current_left_nodes:
                    if point.x < min_x and point.index != current_left_nodes[id_x].index:
                        min_x = point.x
                        min_index = point.index
                    if point.x > max_x and point.index != current_left_nodes[id_x].index:
                        max_x = point.x
                        max_index = point.index
                distance_1 = length(points[min_index], points[max_index])
                distance_2 = min(length(points[min_index], points[0]), length(points[0], points[max_index]))
                distance_3 = min(length(points[min_index], points[temp_series[-1]]), length(points[temp_series[-1]], points[max_index]))

                next_point_to_start = distance_1 + distance_2 + distance_3
                next_move_score = next_point_to_start + current_score + length_to_next_point
                if next_move_score < current_opt:
                    temp_series.append(current_left_nodes[id_x].index)
                    temp_points.pop(id_x)
                    solution_temp = Solution(current_depth + 1, temp_points, temp_series, (current_score + length_to_next_point), current_flag)
                    compare_sets = []
                    for solution_i in range(len(solution_sets)):
                        if solution_sets[solution_i].depth == solution_temp.depth and \
                                solution_sets[solution_i].series[-1] == solution_temp.series[-1]:
                            compare_sets.append(solution_i)
                    if len(compare_sets) == 0:
                        solution_sets.append(solution_temp)
                        continue
                    for compare_solution in compare_sets:
                        temp_series_1 = [i for i in solution_temp.series]
                        temp_series_2 = [i for i in solution_sets[compare_solution].series]
                        temp_series_1.sort()
                        temp_series_2.sort()
                        if temp_series_1 == temp_series_2 and solution_temp.score < solution_sets[compare_solution].score:
                            # print('Yeah')
                            solution_sets.pop(compare_solution)
                            solution_sets.append(solution_temp)
                            break
                        elif temp_series_1 != temp_series_2:
                            solution_sets.append(solution_temp)
                            break
                        # else:
                        #     print('AHA')

                    # solution_sets.append(solution_temp)




                # sleep(1)

    print(count)
    print('\n\n')
    obj_new = current_opt
    solution_new = current_opt_series

    print(obj_new)
    print(solution_new)
    index = 0
    for point in points:
        if index == 0:
            plt.scatter(point.x, point.y, color='green', linewidths=0.2, label=(str(point.x) + ' ' + str(point.y)))
        else:
            plt.scatter(point.x, point.y, color='green', linewidths=0.2)
        index += 1
    for i in range(-1, nodeCount - 1):
        plt.plot([points[solution_new[i]].x, points[solution_new[i + 1]].x],
                 [points[solution_new[i]].y, points[solution_new[i + 1]].y])
    plt.legend()
    plt.show()

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj_new + ' ' + str(nodeCount) + '\n'
    output_data += ' '.join(map(str, solution_new))

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

