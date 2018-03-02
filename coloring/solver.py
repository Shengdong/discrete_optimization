#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
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
    solution_matrix = [[(node_count + 1) for i in range(node_count)] for i in range(node_count)]
    for edge in edges:
        solution_matrix[edge[0]][edge[1]] = -1
        solution_matrix[edge[1]][edge[0]] = -1
    # for row in solution_matrix:
    #     print(row)

    Node = namedtuple('Node', ['index', 'rank', 'color', 'domain', 'edges', 'count'])

    nodes = []
    for i in range(node_count):
        node = Node(i, i, [], [], [0 for i in range(node_count)], 0)
        nodes.append(node)

    for i in range(node_count):
        count = 0
        for solution_x in solution_matrix[i]:
            if solution_x == -1:
                count += 1
        node_temp = Node(nodes[i].index, nodes[i].rank, nodes[i].color, nodes[i].domain, solution_matrix[i], count)
        nodes[i] = node_temp

    solution_greedy = [-1 for i in range(node_count)]

    color_count = 0
    for i in range(0, node_count):
        best_count = -1
        best_index_1 = -1
        best_index_2 = -1
        for j in range(i, node_count):
            if len(nodes[j].domain) == 0:
                best_index_1 = j
            else:
                node_temp = nodes[j]
                if node_temp.edges.count(-1) > best_count:
                    best_count = node_temp.edges.count(-1)
                    best_index_2 = j
        if best_index_1 > 0 and len(nodes[best_index_2].domain) > 0:
            best_index = best_index_1
        elif best_index_1 > 0 and best_index_2 < 0:
            best_index = best_index_1
        else:
            best_index = best_index_2

        node_pop = nodes.pop(best_index)
        nodes.insert(i, node_pop)
        for node in nodes:
            pop_element = node.edges.pop(best_index)
            node.edges.insert(i, pop_element)
        # print(str(i) + ' ' + str(best_index))
        if len(nodes[i].domain) == 0:
            nodes[i].color.append(color_count)
            # print('Choose New Color:' + str(color_count))
            for t in range(i + 1):
                if color_count != nodes[i].color:
                    nodes[t].edges[i] = node_count
                    nodes[i].edges[t] = node_count
            for q in range(i + 1, node_count):
                if color_count not in nodes[q].domain and nodes[q].edges[i] != -1:
                    nodes[q].domain.append(color_count)
            color_count += 1
            # for node in nodes:
            #     node.count = node.edges.count(-1)
        else:
            color_temp = nodes[i].domain.pop()
            nodes[i].color.append(color_temp)
            # print('Choose Old Color:' + str(color_temp))
            for t in range(i + 1):
                if color_temp != nodes[i].color:
                    nodes[t].edges[i] = node_count
                    nodes[i].edges[t] = node_count
            for q in range(i + 1, node_count):
                if color_temp in nodes[q].domain and nodes[q].edges[i] == -1:
                    index_pop = 0
                    for index in range(len(nodes[q].domain)):
                        if nodes[q].domain[index] == color_temp:
                            index_pop = index
                    nodes[q].domain.pop(index_pop)

    for node in nodes:
        solution_greedy[node.index] = node.color[0]
    greedy_opt = color_count
    greedy_solution_nodes = nodes
    for edge in edges:
        if solution_greedy[edge[0]] == solution_greedy[edge[1]]:
            print('XXX')

    solution_matrix = [[(node_count + 1) for i in range(node_count)] for i in range(node_count)]
    for edge in edges:
        solution_matrix[edge[0]][edge[1]] = -1
        solution_matrix[edge[1]][edge[0]] = -1
    nodes_start = []
    for i in range(node_count):
        node = Node(i, i, [], [], [0 for i in range(node_count)], 0)
        nodes_start.append(node)

    for i in range(node_count):
        count = 0
        for solution_x in solution_matrix[i]:
            if solution_x == -1:
                count += 1
        node_temp = Node(nodes_start[i].index, nodes_start[i].rank, nodes_start[i].color, nodes_start[i].domain,
                         solution_matrix[i], count)
        nodes_start[i] = node_temp

    Solution = namedtuple('Solution', ['color_number', 'depth', 'nodes'])

    solution_root = Solution(-1, 0, [node for node in nodes_start])
    solution_sets = [solution_root]
    current_opt = greedy_opt
    best_solution_nodes = greedy_solution_nodes
    while len(solution_sets):
        solution_sets.sort(key=lambda x: x[0])
        current_solution = solution_sets.pop()
        current_depth = current_solution.depth
        current_color_number = current_solution.color_number
        current_nodes = current_solution.nodes
        if current_depth == node_count and current_color_number < current_opt:
            current_opt = current_solution.color_number
            best_solution_nodes = current_solution.nodes
        if current_depth < node_count and current_color_number < current_opt:
            best_count = -1
            best_index_1 = -1
            best_index_2 = -1
            for j in range(current_depth, len(current_nodes)):
                if len(current_nodes[j].domain) == 0:
                    best_index_1 = j
                else:
                    node_temp = current_nodes[j]
                    if node_temp.edges.count(-1) > best_count:
                        best_count = node_temp.edges.count(-1)
                        best_index_2 = j
            if best_index_1 > 0 and len(current_nodes[best_index_2].domain) > 0:
                best_index = best_index_1
            elif best_index_1 > 0 and best_index_2 < 0:
                best_index = best_index_1
            else:
                best_index = best_index_2

            if best_index < 0:
                print('Wrong: ' + str(best_index_1) + ' ' + str(best_index_2))
                exit(1)

            permute_node = current_nodes.pop(best_index)
            current_nodes.insert(current_depth, permute_node)
            for node in current_nodes:
                pop_element = node.edges.pop(best_index)
                node.edges.insert(current_depth, pop_element)

            if len(current_nodes[current_depth].domain) == 0:
                current_color_number += 1
                color_lists = [[] for i in range(node_count)]
                for i in range(node_count):
                    for index_x in range(len(current_nodes[i].color)):
                        color_lists[i].append(current_nodes[i].color[index_x])
                color_lists[current_depth].append(current_color_number)
                #                current_nodes[current_depth].color.append(current_color_number)
                for t in range(current_depth + 1):
                    if current_color_number != current_nodes[t].color:
                        current_nodes[t].edges[current_depth] = node_count
                        current_nodes[current_depth].edges[t] = node_count
                for q in range(current_depth + 1, node_count):
                    if current_color_number not in current_nodes[q].domain \
                            and current_nodes[q].edges[current_depth] != -1:
                        current_nodes[q].domain.append(current_color_number)
                temp_nodes = []
                for i in range(node_count):
                    temp_nodes.append(Node(current_nodes[i].index, current_nodes[i].rank,
                                           color_lists[i], current_nodes[i].domain, current_nodes[i].edges,
                                           current_nodes[i].count))
                solution_new = Solution(current_color_number, current_depth + 1, temp_nodes)
                solution_sets.append(solution_new)
            else:
                for d_index in range(len(current_nodes[current_depth].domain)):
                    solution_matrix_temp = [[0 for i in range(node_count)] for j in range(node_count)]
                    domain_lists = [[] for i in range(node_count)]
                    color_lists = [[] for i in range(node_count)]
                    for i in range(node_count):
                        for j in range(node_count):
                            solution_matrix_temp[i][j] = current_nodes[i].edges[j]
                        for index_x in range(len(current_nodes[i].domain)):
                            domain_lists[i].append(current_nodes[i].domain[index_x])
                        for index_x in range(len(current_nodes[i].color)):
                            color_lists[i].append(current_nodes[i].color[index_x])

                    result_lists = [[] for i in range(node_count)]
                    color_temp = domain_lists[current_depth][d_index]

                    for t_index in range(len(domain_lists[current_depth])):
                        if t_index != d_index:
                            result_lists[current_depth].append(domain_lists[t_index])

                    color_lists[current_depth].append(color_temp)

                    for t in range(current_depth + 1):
                        if color_temp != current_nodes[t].color:
                            solution_matrix_temp[t][current_depth] = node_count
                            solution_matrix_temp[current_depth][t] = node_count
                    for q in range(current_depth + 1, node_count):
                        for index in range(len(domain_lists[q])):
                            if domain_lists[q][index] != color_temp or solution_matrix_temp[q][current_depth] != -1:
                                result_lists[q].append(domain_lists[q][index])
                    temp_nodes = []
                    for i in range(node_count):
                        temp_nodes.append(Node(current_nodes[i].index, current_nodes[i].rank,
                                               color_lists[i], result_lists[i], solution_matrix_temp[i],
                                               current_nodes[i].count))
                    solution_new = Solution(current_color_number, current_depth + 1, temp_nodes)
                    solution_sets.append(solution_new)

    for node in best_solution_nodes:
#        print(node)
        if len(node.color) > 0:
            solution_greedy[node.index] = node.color[0]
        else:
            solution_greedy[node.index] = -1
    current_opt += 1
#    print(str(greedy_opt) + ' -> ' + str(current_opt))
    color_count = current_opt
    solution = solution_greedy
    for edge in edges:
        if solution_greedy[edge[0]] == solution_greedy[edge[1]]:
            print('XXX')
    # prepare the solution in the specified output format
    output_data = str(color_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

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
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')
