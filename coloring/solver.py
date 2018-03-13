#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from datetime import datetime, timedelta
from time import sleep, time
from random import randint


def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    start = datetime.now()
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

    Node = namedtuple('Node', ['index', 'color', 'domain', 'edges'])

    nodes = []
    for i in range(node_count):
        node = Node(i, [], [], [0 for i in range(node_count)])
        nodes.append(node)

    for i in range(node_count):
        node_temp = Node(nodes[i].index, nodes[i].color, nodes[i].domain, solution_matrix[i])
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
            node_temp = nodes[j]
            if node_temp.edges.count(-1) > best_count:
                best_count = node_temp.edges.count(-1)
                best_index_2 = j
        if best_index_1 > 0 and (len(nodes[best_index_2].domain) > 0 or best_index_2 < 0):
            best_index = best_index_1
        else:
            best_index = best_index_2

        node_pop = nodes.pop(best_index)
        nodes.insert(i, node_pop)
        for node in nodes:
            pop_element = node.edges.pop(best_index)
            node.edges.insert(i, pop_element)
        if len(nodes[i].domain) == 0:
            nodes[i].color.append(color_count)
            for t in range(i + 1):
                if color_count != nodes[i].color[0]:
                    nodes[t].edges[i] = node_count
                    nodes[i].edges[t] = node_count
            for q in range(i + 1, node_count):
                if color_count not in nodes[q].domain and nodes[q].edges[i] != -1:
                    nodes[q].domain.append(color_count)
            color_count += 1
        else:
            min_influence_count = node_count
            best_color_choice = -1
            for color_choice_i in range(len(nodes[i].domain)):
                influence_count = 0
                for j in range(i, node_count):
                    if nodes[i].domain[color_choice_i] in nodes[j].domain and nodes[j].edges[i] == -1:
                        influence_count += 1
                if influence_count < min_influence_count:
                    min_influence_count = influence_count
                    best_color_choice = color_choice_i

            color_temp = nodes[i].domain.pop(best_color_choice)
            nodes[i].color.append(color_temp)
            for t in range(i + 1):
                if color_temp != nodes[i].color[0]:
                    nodes[t].edges[i] = node_count
                    nodes[i].edges[t] = node_count
            for q in range(i + 1, node_count):
                if color_temp in nodes[q].domain and nodes[q].edges[i] == -1:
                    index_pop = -1
                    for index in range(len(nodes[q].domain)):
                        if nodes[q].domain[index] == color_temp:
                            index_pop = index
                            break
                    if index_pop >= 0:
                        nodes[q].domain.pop(index_pop)

    solution_greedy_raw = [0 for i in range(node_count)]
    for i in range(len(nodes)):
        solution_greedy_raw[i] = nodes[i].color[0]

    for node in nodes:
        solution_greedy[node.index] = node.color[0]
    greedy_opt = color_count
    greedy_solution_nodes = nodes

    solution_matrix = [[(node_count + 1) for i in range(node_count)] for i in range(node_count)]
    for edge in edges:
        solution_matrix[edge[0]][edge[1]] = -1
        solution_matrix[edge[1]][edge[0]] = -1
    nodes_start = []
    for i in range(node_count):
        node = Node(i, [], [], [0 for i in range(node_count)])
        nodes_start.append(node)

    for i in range(node_count):
        count = 0
        for solution_x in solution_matrix[i]:
            if solution_x == -1:
                count += 1
        node_temp = Node(nodes_start[i].index, nodes_start[i].color, nodes_start[i].domain, solution_matrix[i])
        nodes_start[i] = node_temp

    Solution = namedtuple('Solution', ['color_number', 'depth', 'nodes'])

    solution_root = Solution(-1, 0, [node for node in nodes_start])
    solution_sets = []
    solution_sets.append(solution_root)
    current_opt = greedy_opt - 1
    best_solution_nodes = greedy_solution_nodes

    start_time = datetime.now()
    break_time = 2

    bool_flag = 1
    invariant_count = 0
    invariant_index_list = []
    while len(solution_sets):
        solution_sets.sort(key=lambda x: (float(x[1] - x[0]) / float(x[1] + 1)))
        solution_sets.sort(key=lambda x: x[1])
        current_time = datetime.now()
        timespan = current_time - start_time
        if timespan.total_seconds() >= break_time:
            break
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
                node_temp = current_nodes[j]
                if node_temp.edges.count(-1) > best_count:
                    best_count = node_temp.edges.count(-1)
                    best_index_2 = j
            if best_index_1 > 0 and (len(current_nodes[best_index_2].domain) > 0 or best_index_2 < 0):
                best_index = best_index_1
            else:
                best_index = best_index_2

            permute_node = current_nodes.pop(best_index)
            current_nodes.insert(current_depth, permute_node)
            for node in current_nodes:
                pop_element = node.edges.pop(best_index)
                node.edges.insert(current_depth, pop_element)

            if len(current_nodes[current_depth].domain) == 0 and (
                    current_color_number + 1) < current_opt and current_depth < node_count:
                current_color_number += 1
                color_lists = [[] for i in range(node_count)]
                for i in range(node_count):
                    for index_x in range(len(current_nodes[i].color)):
                        color_lists[i].append(current_nodes[i].color[index_x])
                color_lists[current_depth].append(current_color_number)
                for t in range(current_depth + 1):
                    if current_color_number != color_lists[t][0]:
                        current_nodes[t].edges[current_depth] = node_count
                        current_nodes[current_depth].edges[t] = node_count
                for q in range(current_depth + 1, node_count):
                    if current_color_number not in current_nodes[q].domain \
                            and current_nodes[q].edges[current_depth] != -1:
                        current_nodes[q].domain.append(current_color_number)
                temp_nodes = []
                for i in range(node_count):
                    temp_nodes.append(
                        Node(current_nodes[i].index, color_lists[i], current_nodes[i].domain, current_nodes[i].edges))
                solution_new = Solution(current_color_number, current_depth + 1, temp_nodes)
                solution_sets.append(solution_new)
                if bool_flag == 1:
                    invariant_count += 1
                    invariant_index_list.append(current_nodes[current_depth].index)

            else:
                bool_flag = 0
                list_t = [[] for i in range(len(current_nodes[current_depth].domain))]
                for d_index in range(len(current_nodes[current_depth].domain)):
                    test_list = [0 for i in range(node_count - current_depth)]
                    for i in range(current_depth, node_count):
                        if current_nodes[current_depth].domain[d_index] in current_nodes[i].domain and \
                                current_nodes[current_depth].edges[i] == -1:
                            test_list[i - current_depth] = len(current_nodes[i].domain) - current_nodes[i].domain.count(
                                current_nodes[current_depth].domain[d_index])
                            list_t[d_index].append(len(current_nodes[i].domain) - 1)
                        else:
                            test_list[i - current_depth] = len(current_nodes[i].domain)
                            list_t[d_index].append(len(current_nodes[i].domain))
                compare_result = [0 for i in range(len(current_nodes[current_depth].domain))]
                for i in range(len(list_t)):
                    for j in range(i, len(list_t)):
                        compare_list = list_t[i]
                        compared_list = list_t[j]
                        count_1 = 0
                        count_2 = 0
                        for p in range(len(compare_list)):
                            if compare_list[p] > compared_list[p]:
                                count_1 += 1
                            if compare_list[p] < compared_list[p]:
                                count_2 += 1
                        if count_1 == 0 and count_2 >= 0:
                            compare_result[i] = j
                            compare_result[j] = j
                        elif count_2 == 0 and count_1 >= 0:
                            compare_result[i] = i
                            compare_result[j] = i
                pop_count = 0
                for i in range(len(compare_result)):
                    if compare_result[i] != i:
                        current_nodes[current_depth].domain.pop(i - pop_count)
                        pop_count += 1

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
                        if color_temp != color_lists[t][0]:
                            solution_matrix_temp[t][current_depth] = node_count
                            solution_matrix_temp[current_depth][t] = node_count
                    for q in range(current_depth + 1, node_count):
                        for index in range(len(domain_lists[q])):
                            if domain_lists[q][index] != color_temp or solution_matrix_temp[q][current_depth] != -1:
                                result_lists[q].append(domain_lists[q][index])
                    temp_nodes = []
                    for i in range(node_count):
                        temp_nodes.append(
                            Node(current_nodes[i].index, color_lists[i], result_lists[i], solution_matrix_temp[i]))
                    solution_new = Solution(current_color_number, current_depth + 1, temp_nodes)
                    solution_sets.append(solution_new)

            # if current_depth < node_count and (current_color_number + 1) < current_opt \
            # 	and current_nodes[current_depth].edges.count(-1) > 0:
            # 		current_color_number += 1
            # 		current_nodes[current_depth].color.append(current_color_number)
            # 		for t in range(current_depth + 1):
            # 			if current_color_number != current_nodes[current_depth].color[0]:
            # 				current_nodes[t].edges[current_depth] = node_count
            # 				current_nodes[current_depth].edges[t] = node_count
            # 		for q in range(current_depth + 1, node_count):
            # 			if current_color_number not in current_nodes[q].domain and current_nodes[q].edges[
            # 				current_depth] != -1:
            # 				current_nodes[q].domain.append(current_color_number)
            # 		solution_new = Solution(current_color_number, current_depth + 1, current_nodes)
            # 		solution_sets_1.append(solution_new)

    solution_raw = [0 for i in range(node_count)]
    for i in range(len(best_solution_nodes)):
        solution_raw[i] = best_solution_nodes[i].color[0]

    solution = [0 for i in range(node_count)]
    for node in best_solution_nodes:
        if len(node.color) > 0:
            solution[node.index] = node.color[0]
        else:
            solution[node.index] = -1
    current_opt += 1

    color_count = current_opt
    for edge in edges:
        if solution_greedy[edge[0]] == solution_greedy[edge[1]]:
            print('XXX')
    print('Invariant count is: ' + str(invariant_count))
    print(invariant_index_list)
    print('\n')
    # ----------------------------------------------------Local Search Part--------------------------------------------#
    solution_matrix = [[(node_count + 1) for i in range(node_count)] for i in range(node_count)]
    for edge in edges:
        solution_matrix[edge[0]][edge[1]] = -1
        solution_matrix[edge[1]][edge[0]] = -1
    nodes = []
    for i in range(node_count):
        node_temp = Node(i, [solution[i]], [], solution_matrix[i])
        nodes.append(node_temp)

    color_list = [i for i in range(color_count)]
    count_list = [0 for i in range(color_count)]
    for i in range(color_count):
        count_list[i] = solution.count(i)
    print('Raw Solution   : ' + str(solution))
    print('Raw Counts ' + str(len(count_list)) + '  : ' + str(count_list))

    color_to_be = len(count_list)
    color_index = -1
    for index in range(len(count_list)):
        if count_list[index] < color_to_be:
            color_to_be = count_list[index]
            color_index = index
    color_choose = 14
    count_list.pop(color_choose)
    color_list.pop(color_choose)
    print('Delete Color:' + str(color_choose) + '\n')

    conflict_lists = []
    for i in range(len(solution)):
        if solution[i] == color_choose:
            nodes[i].color.pop()
            nodes[i].color.append(-1)
            conflict_lists.append(nodes[i])

    while len(conflict_lists):
        for node in conflict_lists:
            print(node)
        for conflict_node in conflict_lists:
            min_conflict_count = node_count * 1000
            best_color = -1
            for color_temp in color_list:
                influence_count = 0
                for node_compare in nodes:
                    if conflict_node.edges[node_compare.index] == -1 and color_temp == node_compare.color[0] and conflict_node.index != node_compare.index:
                        if node_compare.index not in invariant_index_list:
                            influence_count += 1
                        else:
                            influence_count += 1000
                if influence_count < min_conflict_count:
                    best_color = color_temp
                    min_conflict_count = influence_count

            print('Best ' + str(best_color) + ' and influences: ' + str(min_conflict_count))
            # print('\n')
            # best_color_ind = randint(0, len(color_list) - 1)
            # best_color = color_list[best_color_ind]
            if conflict_node.index == 20:
                best_color = 4
            conflict_node.color.pop()
            conflict_node.color.append(best_color)
        for node in conflict_lists:
            print(node)
        # print('\n')
        next_conflict_lists = []
        for conflict_node in conflict_lists:
            for node_compare in nodes:
                if conflict_node.edges[node_compare.index] == -1 and conflict_node.color[0] == node_compare.color[0] \
                        and conflict_node.index != node_compare.index:
                    next_conflict_lists.append(node_compare)
        while len(conflict_lists):
            conflict_lists.pop()
        while len(next_conflict_lists):
            temp_n = next_conflict_lists.pop()
            if temp_n not in conflict_lists:
                conflict_lists.append(temp_n)
        solution_temp = [0 for i in range(len(nodes))]
        for node in nodes:
            solution_temp[node.index] = node.color[0]
        print(solution_temp)
        print('######################################################################################')
        sleep(1)

    # ----------------------------------------------------Local Search Part--------------------------------------------#

    solution_new = []
    for node in nodes:
        solution_new.append(node.color[0])
    print(solution_new)
    color_result_list = []
    for solution_element in solution_new:
        if solution_element not in color_result_list:
            color_result_list.append(solution_element)
    # print('Counts ' + str(len(color_result_list)) + '  : ' + str(color_result_list))
    # print(solution)
    current_opt = len(color_result_list)

    for edge in edges:
        if solution_new[edge[0]] == solution_new[edge[1]]:
            print('XX ' + str(edge[0]) + ' -> ' + str(edge[1]))

    # prepare the solution in the specified output format
    output_data = str(current_opt) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution_new))

    print(str(greedy_opt) + ' -> ' + str(current_opt))
    print(output_data)
    current_time = datetime.now()
    timespan = current_time - start
    print('Time: ' + str(timespan.total_seconds()))

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
