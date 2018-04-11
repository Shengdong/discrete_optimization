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
    facilities_ori = []
    for i in range(1, facility_count + 1):
        parts = lines[i].split()
        facilities.append(Facility(i - 1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])), []))
        facilities_ori.append(Facility(i - 1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])), []))

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
    # print('Customer Total Demand:' + str(total_demand) + '\n')
    facilities.sort(key=lambda x: len(x[4]))
    # for facility in facilities:
    #     print(str(facility.index) + ' ' + str(facility.setup_cost) + ' ' + str(facility.capacity) + ' '
    #           + str(facility.location) + ' ' + str(facility.nearest_customers))
    facility_opened = []
    while len(facilities):
        facilities.sort(key=lambda x: len(x[4]))
        # for facility in facilities:
        #     if len(facility.nearest_customers) != 0:
        #         print(str(facility.index) + ' ' + str(facility.setup_cost) + ' ' + str(facility.capacity) + ' '
        #             + str(facility.location) + ' ' + str(facility.nearest_customers))
        # print('\n')
        facility_chosen = facilities.pop()

        if len(facility_chosen.nearest_customers) == 0:
            break

        close_penalty = 0
        current_cost = 0
        temp_capacity = [capacity for capacity in capacity_remaining]
        temp_solution = []
        for customer_i in facility_chosen.nearest_customers:
            current_cost += customer_i[1]
            nearest_dist = 1000000000000000000000000000
            assigned_index = -1
            for facility in facility_opened:
                if temp_capacity[facility.index] >= customers[customer_i[0]].demand:
                    temp_dist = length(facility.location, customers[customer_i[0]].location)
                    if temp_dist < nearest_dist:
                        nearest_dist = temp_dist
                        assigned_index = facility.index
            if assigned_index == -1:
                close_penalty = 1000000000000000000000000000000
                break
            temp_capacity[assigned_index] -= customers[customer_i[0]].demand
            close_penalty += nearest_dist
            temp_solution.append(assigned_index)

        close_penalty = close_penalty - current_cost

        if close_penalty <= facility_chosen.setup_cost:
            for index in range(len(facility_chosen.nearest_customers)):
                customer_index = facility_chosen.nearest_customers[index]
                customers[customer_index[0]].assigned_facility.append(temp_solution[index])
                capacity_remaining[temp_solution[index]] -= customers[customer_index[0]].demand
        else:
            facility_opened.append(facility_chosen)
            facility_chosen.nearest_customers.sort(key=lambda x: x[1])
            for customer_index in facility_chosen.nearest_customers:
                if capacity_remaining[facility_chosen.index] >= customers[customer_index[0]].demand and len(customers[customer_index[0]].assigned_facility) == 0:
                    customers[customer_index[0]].assigned_facility.append(facility_chosen.index)
                    capacity_remaining[facility_chosen.index] -= customers[customer_index[0]].demand

        for facility in facilities:
            while len(facility.nearest_customers) > 0:
                facility.nearest_customers.pop()

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
    # demand = [0 for facility in facilities]
    # for i in range(len(solution)):
    #     demand[solution[i]] += customers[i].demand
    #
    # print(demand)
    # capacity = [0 for facility in facilities]
    # for i in range(len(facilities)):
    #     capacity[i] = facilities[i].capacity
    # print(capacity)
    #
    # capacity_remaining_1 = [0 for facility in facilities]
    # compare = [0 for facility in facilities]
    # for i in range(len(facilities)):
    #     capacity_remaining_1[i] = capacity[i] - demand[i]
    #     compare[i] = capacity_remaining_1[i] - capacity_remaining[i]
    #     if capacity_remaining_1[i] < 0:
    #         print("Wow")
    #     if compare[i] != 0:
    #         print("Wa Wow")
    # print(capacity_remaining_1)
    # print(compare)
    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
#    print(output_data)

    return output_data

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        solve_it(input_data)
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')
