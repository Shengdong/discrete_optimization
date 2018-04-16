#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np
import random

Point = namedtuple("Point", ['x', 'y'])
PointIndex = namedtuple("Point", ['index', 'x', 'y'])
Solution = namedtuple("Solution", ['depth', 'left_nodes', 'series', 'score', 'flag'])
Edge = namedtuple("Edge", ['length', 'start', 'end', 'index'])

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    
    customers = []
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

    #the depot is always the first customer in the input
    depot = customers[0] 


    # build a trivial solution
    # assign customers to vehicles starting by the largest customer demands
    vehicle_tours = []
    
    remaining_customers = set(customers)
    remaining_customers.remove(depot)
    
    for v in range(0, vehicle_count):
        # print "Start Vehicle: ",v
        vehicle_tours.append([])
        capacity_remaining = vehicle_capacity
        while sum([capacity_remaining >= customer.demand for customer in remaining_customers]) > 0:
            used = set()
            order = sorted(remaining_customers, key=lambda customer: -customer.demand)
            for customer in order:
                if capacity_remaining >= customer.demand:
                    capacity_remaining -= customer.demand
                    vehicle_tours[v].append(customer)
                    # print '   add', ci, capacity_remaining
                    used.add(customer)
            remaining_customers -= used

    # checks that the number of customers served is correct
    assert sum([len(v) for v in vehicle_tours]) == len(customers) - 1

    # print('Start')
    for vehicle_tour in vehicle_tours:
        index_list = [customer.index for customer in vehicle_tour]
        inputData = str(len(index_list) + 1) + '\n'
        inputData += str(depot.x) + ' ' + str(depot.y) + '\n'
        for index in index_list:
            inputData += str(customers[index].x) + ' ' + str(customers[index].y) + '\n'
        swap_list = tsp_solver(inputData)
        # print(swap_list)
        while True:
            if swap_list[0] != 0:
                swap_element = swap_list.pop(0)
                swap_list.append(swap_element)
            else:
                # swap_list.pop(0)
                break
        swap_list.pop(0)

        vehicle_tour_new = []
        for index in swap_list:
            vehicle_tour_new.append(vehicle_tour[index - 1])
        while len(vehicle_tour) != 0:
            vehicle_tour.pop(-1)
        for v in vehicle_tour_new:
            vehicle_tour.append(v)
        # print(vehicle_tour_new)
        # print(swap_list)
        # print(inputData)

    # print('End')


    # calculate the cost of the solution; for each vehicle the length of the route
    obj = 0
    for v in range(0, vehicle_count):
        vehicle_tour = vehicle_tours[v]
        if len(vehicle_tour) > 0:
            obj += length(depot, vehicle_tour[0])
            for i in range(0, len(vehicle_tour)-1):
                obj += length(vehicle_tour[i],vehicle_tour[i+1])
            obj += length(vehicle_tour[-1],depot)
    # prepare the solution in the specified output format
    outputData = '%.2f' % obj + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        outputData += str(depot.index) + ' ' + ' '.join([str(customer.index) for customer in vehicle_tours[v]]) + ' ' + str(depot.index) + '\n'

    for vehicle_tour in vehicle_tours:
        total_demand = 0
        for customer in vehicle_tour:
            total_demand += customer.demand
        if total_demand > vehicle_capacity:
            print('Wrong')
            exit(1)
    # for customer in customers:
    #     if customer.index !=0:
    #         plt.scatter(customer.x, customer.y, color='green', linewidths=0.2)
    #     else:
    #         plt.scatter(customer.x, customer.y, color='red', linewidths=0.5)
    #
    # color_list = ['b', 'g', 'y', 'r', 'k', 'm', 'c', 'orange', 'pink', 'olive', 'peru', 'navy',
    #               'gold', 'fuchsia', 'darkorchid', 'aqua']
    # valid_count = 0
    # for v in range(0, vehicle_count):
    #     vehicle_tour = vehicle_tours[v]
    #     if len(vehicle_tour) > 0:
    #         valid_count += 1
    #         plt.plot([vehicle_tour[0].x, depot.x], [vehicle_tour[0].y, depot.y], color=color_list[v%len(color_list)])
    #         for i in range(0, len(vehicle_tour)-1):
    #             plt.plot([vehicle_tour[i].x, vehicle_tour[i+1].x], [vehicle_tour[i].y, vehicle_tour[i+1].y], color=color_list[v%len(color_list)])
    #         plt.plot([vehicle_tour[len(vehicle_tour)-1].x, depot.x], [vehicle_tour[len(vehicle_tour)-1].y, depot.y], color=color_list[v%len(color_list)])
    # print(valid_count)
    # for i in range(-1, nodeCount - 1):
    #     plt.plot([points[solution_opt[i]].x, points[solution_opt[i + 1]].x],
    #              [points[solution_opt[i]].y, points[solution_opt[i + 1]].y])
    # plt.legend()
    plt.show()
    # print(outputData)
    return outputData



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

def tsp_solver(input_data):
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


    return solution_opt
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
        # file_path_1 = '/home/kaylor/Desktop/discrete_optimization/vrp/data/vrp_16_3_1'
        # file_path_2 = '/home/kaylor/Desktop/discrete_optimization/vrp/data/vrp_26_8_1'c
        # file_path_3 = '/home/kaylor/Desktop/discrete_optimization/vrp/data/vrp_51_5_1'
        # file_path_4 = '/home/kaylor/Desktop/discrete_optimization/vrp/data/vrp_101_10_1'
        # file_path_5 = '/home/kaylor/Desktop/discrete_optimization/vrp/data/vrp_200_16_1'
        # file_path_6 = '/home/kaylor/Desktop/discrete_optimization/vrp/data/vrp_421_41_1'
        # file_location = file_path_1.strip()
        #
        # with open(file_location, 'r') as input_data_file:
        #     input_data = input_data_file.read()
        # solve_it(input_data)

