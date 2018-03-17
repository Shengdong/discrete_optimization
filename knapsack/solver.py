#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple

Item = namedtuple("Item", ['index', 'value', 'weight'])


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    Density_Item = namedtuple("Item", ['index', 'density', 'value', 'weight'])
    # parse the input
    global print_msg
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
    density_items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))
        density_items.append(Density_Item(i - 1, float(parts[0])/float(parts[1]), int(parts[0]), int(parts[1])))
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full

    opt_value_greedy = 0
    left_capacity_greedy = capacity
    taken_greedy = ''
    for d_item in density_items:
        if left_capacity_greedy - d_item.weight >= 0:
            opt_value_greedy += d_item.value
            left_capacity_greedy -= d_item.weight
            taken_greedy += '1'
        else:
            taken_greedy += '0'

    density_items.sort(key=lambda x: -x[1])

#    print_msg_1 = ''
#    for d_item in density_items:
#        print_msg_1 += str(d_item.index) + ' ' + str(d_item.density) + ' ' + str(d_item.value) + ' ' + str(d_item.weight) + '\n'
#    print(print_msg_1)

    relax_heuristic = [0.0] * len(density_items)
    for i in range(1, len(density_items)):
        relax_value = 0.0
        current_capacity = 0
        for j in range(i, len(density_items)):
            if (density_items[j].weight + current_capacity) <= capacity:
                relax_value += density_items[j].value
                current_capacity += density_items[j].weight
            else:
                relax_value += (capacity - current_capacity) * density_items[j].density
                relax_heuristic[i] = relax_value
                break


    relax_value = 0.0
    current_capacity = 0
    for d_item in density_items:
        if (d_item.weight + current_capacity) <= capacity:
            relax_value += d_item.value
            current_capacity += d_item.weight
        else:
            relax_value += (capacity - current_capacity) * d_item.density
            break

    Solution = namedtuple("Solution", ['opt_value',
                                       'left_capacity',
                                       'max_possible_value',
                                       'level',
                                       'taken'])


#    print("Greedy opt value is " + str(opt_value_greedy))

    solution_root = Solution(0, capacity, relax_value, 0, '')
    opt_solution  = solution_root
    solution_sets = [solution_root]
    count = 0
    current_opt_value = opt_value_greedy
    while len(solution_sets):
        count += 1
        solution_sets.sort(key=lambda x: x[0])
        solution_current = solution_sets.pop()

        if (solution_current.level == len(density_items)) and (solution_current.opt_value >= current_opt_value):
            opt_solution = solution_current
            current_opt_value = opt_solution.opt_value

        if (solution_current.level < len(density_items)) and (solution_current.max_possible_value >= current_opt_value):
            d_next_item = density_items[solution_current.level]

            if solution_current.left_capacity - d_next_item.weight >= 0:
                solution_children_1 = Solution(solution_current.opt_value + d_next_item.value,
                                               solution_current.left_capacity - d_next_item.weight,
                                               solution_current.max_possible_value,
                                               solution_current.level + 1,
                                               solution_current.taken + '1')
                solution_sets.append(solution_children_1)

                relax_value_inner = 0.0
                current_capacity = capacity - solution_current.left_capacity
                for i in range(solution_current.level + 1, len(density_items)):
                        if (density_items[i].weight + current_capacity) <= capacity:
                            relax_value_inner += density_items[i].value
                            current_capacity += density_items[i].weight
                        else:
                            relax_value_inner += (capacity - current_capacity) * density_items[i].density
                            break

                solution_children_2 = Solution(solution_current.opt_value,
                                               solution_current.left_capacity,
                                               solution_current.opt_value + relax_value_inner,
                                               solution_current.level + 1,
                                               solution_current.taken + '0')
                solution_sets.append(solution_children_2)
            else:
                relax_value_inner = 0.0
                current_capacity = capacity - solution_current.left_capacity
                for i in range(solution_current.level + 1, len(density_items)):
                        if (density_items[i].weight + current_capacity) < capacity:
                            relax_value_inner += density_items[i].value
                            current_capacity += density_items[i].weight
                        else:
                            relax_value_inner += (capacity - current_capacity) * density_items[i].density
                            break

                solution_children = Solution(solution_current.opt_value,
                                             solution_current.left_capacity,
                                             solution_current.opt_value + relax_value_inner,
                                             solution_current.level + 1,
                                             solution_current.taken + '0')
                solution_sets.append(solution_children)

    value = opt_solution.opt_value
    taken = opt_solution.taken

    taken_1 = [0]*len(items)
    for i in range(0, len(taken)):
        taken_1[density_items[i].index] = int(taken[i])

    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken_1))
#    print(output_data)
    return output_data


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        solve_it(input_data)
#    else:
#        print(
#            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
