#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import matplotlib.pyplot as plt

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

    # calculate the cost of the solution; for each vehicle the length of the route
    obj = 0
    for v in range(0, vehicle_count):
        vehicle_tour = vehicle_tours[v]
        if len(vehicle_tour) > 0:
            obj += length(depot,vehicle_tour[0])
            for i in range(0, len(vehicle_tour)-1):
                obj += length(vehicle_tour[i],vehicle_tour[i+1])
            obj += length(vehicle_tour[-1],depot)

    # prepare the solution in the specified output format
    outputData = '%.2f' % obj + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        outputData += str(depot.index) + ' ' + ' '.join([str(customer.index) for customer in vehicle_tours[v]]) + ' ' + str(depot.index) + '\n'


    for customer in customers:
        if customer.index !=0:
            plt.scatter(customer.x, customer.y, color='green', linewidths=0.2)
        else:
            plt.scatter(customer.x, customer.y, color='red', linewidths=0.5)

    color_list = ['b', 'g', 'y', 'r', 'k', 'm', 'c', 'orange', 'pink', 'olive', 'peru', 'navy',
                  'gold', 'fuchsia', 'darkorchid', 'aqua']
    valid_count = 0
    for v in range(0, vehicle_count):
        vehicle_tour = vehicle_tours[v]
        if len(vehicle_tour) > 0:
            valid_count += 1
            plt.plot([vehicle_tour[0].x, depot.x], [vehicle_tour[0].y, depot.y], color=color_list[v%len(color_list)])
            for i in range(0, len(vehicle_tour)-1):
                plt.plot([vehicle_tour[i].x, vehicle_tour[i+1].x], [vehicle_tour[i].y, vehicle_tour[i+1].y], color=color_list[v%len(color_list)])
            plt.plot([vehicle_tour[len(vehicle_tour)-1].x, depot.x], [vehicle_tour[len(vehicle_tour)-1].y, depot.y], color=color_list[v%len(color_list)])
    print(valid_count)
    # for i in range(-1, nodeCount - 1):
    #     plt.plot([points[solution_opt[i]].x, points[solution_opt[i + 1]].x],
    #              [points[solution_opt[i]].y, points[solution_opt[i + 1]].y])
    # plt.legend()
    plt.show()
    print(outputData)
    return outputData


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        solve_it(input_data)
    else:
        file_path_1 = '/home/kaylor/Desktop/discrete_optimization/vrp/data/vrp_16_3_1'
        file_path_2 = '/home/kaylor/Desktop/discrete_optimization/vrp/data/vrp_26_8_1'
        file_path_3 = '/home/kaylor/Desktop/discrete_optimization/vrp/data/vrp_51_5_1'
        file_path_4 = '/home/kaylor/Desktop/discrete_optimization/vrp/data/vrp_101_10_1'
        file_path_5 = '/home/kaylor/Desktop/discrete_optimization/vrp/data/vrp_200_16_1'
        file_path_6 = '/home/kaylor/Desktop/discrete_optimization/vrp/data/vrp_421_41_1'
        file_location = file_path_2.strip()

        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        solve_it(input_data)

