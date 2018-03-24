#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
from time import sleep, time

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location', 'nearest_customers'])
Customer = namedtuple("Customer", ['index', 'demand', 'location', 'assigned_facility'])

Solution = namedtuple("Solution", ['facility_status', 'demand', 'location', 'assigned_facility'])


def length(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])

    facilities = []
    for i in range(1, facility_count + 1):
        parts = lines[i].split()
        facilities.append(Facility(i - 1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])), []))

    customers = []
    for i in range(facility_count + 1, facility_count + 1 + customer_count):
        parts = lines[i].split()
        customers.append(Customer(i - 1 - facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2])), []))

    # build a trivial solution
    # pack the facilities one by one until all the customers are served
    solution = [-1] * len(customers)
    capacity_remaining = [f.capacity for f in facilities]

    # facility_index = 0
    # for customer in customers:
    #     if capacity_remaining[facility_index] >= customer.demand:
    #         solution[customer.index] = facility_index
    #         capacity_remaining[facility_index] -= customer.demand
    #     else:
    #         facility_index += 1
    #         assert capacity_remaining[facility_index] >= customer.demand
    #         solution[customer.index] = facility_index
    #         capacity_remaining[facility_index] -= customer.demand

    # used = [0] * len(facilities)
    # for facility_index in solution:
    #     used[facility_index] = 1

    for customer in customers:
        min_dist = 100000000000000000000000000000000000000
        assigned_index = [-1, -1]
        for facility in facilities:
            temp_dist = length(facility.location, customer.location)
            if temp_dist < min_dist and len(customer.assigned_facility) == 0:
                min_dist = temp_dist
                assigned_index[0] = facility.index
                assigned_index[1] = customer.index
        for facility in facilities:
            if facility.index == assigned_index[0]:
                facility.nearest_customers.append(
                    [assigned_index[1], min_dist, customers[assigned_index[1]].demand])
    total_demand = 0
    for customer in customers:
        total_demand += customer.demand
    print(total_demand)
    facilities.sort(key=lambda x: len(x[4]))
    for facility in facilities:
        print(str(facility.index) + ' ' + str(facility.setup_cost) + ' ' + str(facility.capacity) + ' '
              + str(facility.location) + ' ' + str(facility.nearest_customers))
    # exit(1)
    facility_closed = []
    while len(facilities):
        facilities.sort(key=lambda x: len(x[4]))
        facility_chosen = facilities.pop()

        if len(facility_chosen.nearest_customers) == 0:
            break
        facility_chosen.nearest_customers.sort(key=lambda x: x[1])

        temp_capacity = [i for i in capacity_remaining]

        opt_cost_1 = 0
        opt_cost_2 = 0
        count = 0
        for customer_index in facility_chosen.nearest_customers:
            opt_cost_1 += customer_index[1]
            if len(facility_closed) == 0:
                opt_cost_2 += 10000000000000
            min_dist = 100000000000000000000000000000000000000
            assigned_index = [-1, -1]
            for facility in facility_closed:
                temp_dist = length(facility.location, customers[customer_index[0]].location)
                if temp_dist <= min_dist:
                    min_dist = temp_dist
                    assigned_index[0] = facility.index
                    assigned_index[1] = customers[customer_index[0]].index
            for facility in facility_closed:
                if facility.index == assigned_index[0]:
                    opt_cost_2 += min_dist

        opt_cost_1 += facility_chosen.setup_cost
        if opt_cost_2 < opt_cost_1 and count == len(facility_chosen.nearest_customers):
            print('Yeah' + ' ' + str(facility_chosen.index) + ' ' + str(len(facilities)))
            for customer_index in facility_chosen.nearest_customers:
                for facility in facility_closed:
                    if customer_index[2] <= capacity_remaining[facility.index]:
                        capacity_remaining[facility.index] -= customer_index[2]
                        customers[customer_index[0]].assigned_facility.append(facility_chosen.index)
            continue
        facility_closed.append(facility_chosen)

        for customer_index in facility_chosen.nearest_customers:
            if capacity_remaining[facility_chosen.index] >= customers[customer_index[0]].demand and len(customers[customer_index[0]].assigned_facility) == 0:
                customers[customer_index[0]].assigned_facility.append(facility_chosen.index)
                capacity_remaining[facility_chosen.index] -= customers[customer_index[0]].demand
        for customer in customers:
            if len(customer.assigned_facility) != 0:
                continue
            min_dist = 100000000000000000000000000000000000000
            assigned_index = [-1, -1]
            for facility in facilities:
                temp_dist = length(facility.location, customer.location)
                if temp_dist <= min_dist:
                    min_dist = temp_dist
                    assigned_index[0] = facility.index
                    assigned_index[1] = customer.index
            for facility in facilities:
                if facility.index == assigned_index[0]:
                    facility.nearest_customers.append(
                        [assigned_index[1], min_dist, customers[assigned_index[1]].demand])

    for customer in customers:
        solution[customer.index] = customer.assigned_facility[-1]

    facilities = []
    for i in range(1, facility_count + 1):
        parts = lines[i].split()
        facilities.append(Facility(i - 1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])), []))

    used = [0] * len(facilities)
    for facility_index in solution:
        used[facility_index] = 1

    # calculate the cost of the solution
    obj = sum([f.setup_cost * used[f.index] for f in facilities])
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)


    obj_new = obj

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')
