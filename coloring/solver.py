#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    global max_rank_index
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a trivial solution
    # every node has its own color
    print('No. of nodes is ' + str(node_count))
    print('Input Data: ')
    for edge in edges:
        print(edge)
    solution_matrix = [[(node_count + 1) for i in range(node_count)] for i in range(node_count)]
    for edge in edges:
        solution_matrix[edge[0]][edge[1]] = -1
        solution_matrix[edge[1]][edge[0]] = -1
    for row in solution_matrix:
        print(row)
    solution_greedy = []

    Node = namedtuple('Node', ['index', 'rank', 'color', 'domain', 'edges', 'count'])

    nodes = []
    for i in range(node_count):
        node = Node(i, i, -1, [], [0 for i in range(node_count)], 0)
        nodes.append(node)

    for i in range(node_count):
        count = 0
        for solution_x in solution_matrix[i]:
            if solution_x == -1:
                count += 1
        node_temp = Node(nodes[i].index, nodes[i].rank, nodes[i].color, nodes[i].domain, solution_matrix[i], count)
        nodes[i] = node_temp

    print('Result: ')
    max_rank_index = 0
    for i in range(0, len(nodes)):
        max_rank_index = len(solution_greedy)
        for j in range(len(solution_greedy), node_count):
            if nodes[j].count > max_rank_index:
                max_rank_index = nodes[j].rank
        for nod

    print(max_rank_index)

#    for node in nodes:


#    solution_greedy.append[0]
#    previous_lvl = 0
#    for i in range(1, node_count):



    solution = range(0, node_count)
    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

