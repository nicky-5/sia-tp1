from src.functions import clear, read_file_to_matrix, game_from_matrix, print_game
from src.methods import MethodDFS, MethodBFS, MethodHeuristic, MethodAStar
from src.heuristics import min_manhattan_modified, min_manhattan, fast_anti_livelock, walkable_distance, anti_wall
from src.search import search, a_star_search
import pandas as pd
import numpy as np
import time
import os
import matplotlib.pyplot as plt
import seaborn as sns
import copy


tests = [
    'test/test_1',
    'test/test_4',
    'test/test_5',
    'test/test_6'
]

method_names = ['bfs', 'dfs']
methods = [MethodBFS, MethodDFS]


columns = ['solved', 'mean_time', 'time_error',
           'cost', 'expanded', 'frontier', 'solution']
dataframes = {}


def test_not_informed():
    print("Running not informed...")
    for test in tests:
        print(test)
        dataframes[test] = pd.DataFrame(
            0.0, index=method_names, columns=columns)
        matrix = read_file_to_matrix(test)
        [board, targets, state] = game_from_matrix(matrix)

        for method, method_name in zip(methods, method_names):
            durations = []
            solution = None
            explored = None
            frontier = None
            iterations = 100
            for i in range(1, iterations):
                m = method(state)
                start = time.time()
                solution, explored, frontier = search(m, board, targets)
                end = time.time()
                duration = end - start
                durations.append(duration)
            dataframes[test].at[method_name, 'mean_time'] = np.mean(durations)
            dataframes[test].at[method_name, 'time_error'] = np.std(
                durations) / iterations**0.5
            if solution is not None:
                dataframes[test].at[method_name, 'solved'] = True
                dataframes[test].at[method_name, 'cost'] = solution.cost
            else:
                dataframes[test].at[method_name, 'solved'] = False
                dataframes[test].at[method_name, 'cost'] = 0

            dataframes[test].at[method_name, 'expanded'] = len(explored)
            dataframes[test].at[method_name, 'frontier'] = len(frontier)
    print(dataframes)
    return dataframes


def test_informed():
    print("Running informed...")
    method_names = ['Greedy', 'A star']

    for test in tests:
        print(test)
        dataframes[test] = pd.DataFrame(
            0.0, index=method_names, columns=columns)
        matrix = read_file_to_matrix(test)
        [board, targets, state] = game_from_matrix(matrix)

        method_dfs = MethodDFS(state)
        durations = []
        solution = None
        explored = None
        frontier = None
        iterations = 10
        for i in range(1, iterations):
            method_heuristic = MethodHeuristic(
                state, fast_anti_livelock(min_manhattan(targets), board))
            start = time.time()
            [solution, explored, frontier] = search(
                method_heuristic, board, targets)
            end = time.time()
            duration = end - start
            durations.append(duration)
        dataframes[test].at[method_names[0], 'mean_time'] = np.mean(durations)
        dataframes[test].at[method_names[0], 'time_error'] = np.std(
            durations) / iterations**0.5
        if solution is not None:
            dataframes[test].at[method_names[0], 'solved'] = True
            dataframes[test].at[method_names[0], 'cost'] = solution.cost
        else:
            dataframes[test].at[method_names[0], 'solved'] = False
            dataframes[test].at[method_names[0], 'cost'] = 0

        dataframes[test].at[method_names[0], 'expanded'] = len(explored)
        dataframes[test].at[method_names[0], 'frontier'] = len(frontier)

        for i in range(1, iterations):
            method_astar = MethodAStar(state, fast_anti_livelock(
                min_manhattan(targets), board))
            start = time.time()
            [solution, explored, frontier] = a_star_search(
                method_astar, board, targets)
            end = time.time()
            duration = end - start
            durations.append(duration)
        dataframes[test].at[method_names[1], 'mean_time'] = np.mean(durations)
        dataframes[test].at[method_names[1], 'time_error'] = np.std(
            durations) / iterations**0.5
        if solution is not None:
            dataframes[test].at[method_names[1], 'solved'] = True
            dataframes[test].at[method_names[1], 'cost'] = solution.cost
        else:
            dataframes[test].at[method_names[1], 'solved'] = False
            dataframes[test].at[method_names[1], 'cost'] = 0

        dataframes[test].at[method_names[1], 'expanded'] = len(explored)
        dataframes[test].at[method_names[1], 'frontier'] = len(frontier)

    print(dataframes)
    return dataframes


# dataframes = test_not_informed()
# method_names = ['dfs', 'bfs']

dataframes = test_informed()
method_names = ['Greedy', 'A star']

tiempos_bfs = [dataframes[test].at[method_names[0], 'mean_time']
               for test in tests]
errores_bfs = [dataframes[test].at[method_names[0], 'time_error']
               for test in tests]
tiempos_dfs = [dataframes[test].at[method_names[1], 'mean_time']
               for test in tests]
errores_dfs = [dataframes[test].at[method_names[1], 'time_error']
               for test in tests]

plt.rcParams['figure.dpi'] = 300

# Configuración del gráfico
x = range(len(tests))
ancho_barra = 0.35

# Crear gráfico de barras
fig, ax = plt.subplots()
barra_bfs = ax.bar(x, tiempos_bfs, ancho_barra,
                   yerr=errores_bfs, capsize=5, label=method_names[0], color='blue')
barra_dfs = ax.bar([i + ancho_barra for i in x], tiempos_dfs, ancho_barra,
                   yerr=errores_dfs, capsize=5, label=method_names[1], color='orange')

# Etiquetas y título
ax.set_xlabel('Pruebas')
ax.set_ylabel('Tiempo Medio de Ejecución')
ax.set_title(
    'Comparación de Tiempo Medio de Ejecución entre ' + method_names[0] + ' y ' + method_names[1] + ' por Prueba')
ax.set_xticks([i + ancho_barra / 2 for i in x])
ax.set_xticklabels(tests)
ax.legend()

# Mostrar gráfico
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Sample data
categories = tests

values_group1 = [dataframes[test].at[method_names[0], 'cost']
                 for test in tests]
values_group2 = [dataframes[test].at[method_names[1], 'cost']
                 for test in tests]

# Set the width of the bars
bar_width = 0.35

# Set the positions of the bars on the x-axis
bar_positions_group1 = np.arange(len(categories))
bar_positions_group2 = [x + bar_width for x in bar_positions_group1]

# Create bar plot
plt.bar(bar_positions_group1, values_group1,
        color='blue', width=bar_width, label=method_names[0])
plt.bar(bar_positions_group2, values_group2,
        color='orange', width=bar_width, label=method_names[1])

# Add labels and title
plt.xlabel('Test')
plt.ylabel('Cost')
plt.title('Bar graph comparing ' +
          method_names[0] + ' and ' + method_names[1] + ' costs')

# Add x-axis tick labels
plt.xticks([r + bar_width/2 for r in range(len(categories))], categories)

# Add legend
plt.legend()

# Show plot
plt.show()

values_group1 = [dataframes[test].at[method_names[0], 'expanded']
                 for test in tests]
values_group2 = [dataframes[test].at[method_names[1], 'expanded']
                 for test in tests]

# Set the width of the bars
bar_width = 0.35

# Set the positions of the bars on the x-axis
bar_positions_group1 = np.arange(len(categories))
bar_positions_group2 = [x + bar_width for x in bar_positions_group1]

# Create bar plot
plt.bar(bar_positions_group1, values_group1,
        color='blue', width=bar_width, label=method_names[0])
plt.bar(bar_positions_group2, values_group2,
        color='orange', width=bar_width, label=method_names[1])

# Add labels and title
plt.xlabel('Test')
plt.ylabel('Number of Expanded Nodes')
plt.title('Bar graph comparing ' +
          method_names[0] + ' and ' + method_names[1] + ' expanded nodes')

# Add x-axis tick labels
plt.xticks([r + bar_width/2 for r in range(len(categories))], categories)

# Add legend
plt.legend()

plt.show()

values_group1 = [dataframes[test].at[method_names[0], 'frontier']
                 for test in tests]
values_group2 = [dataframes[test].at[method_names[1], 'frontier']
                 for test in tests]

# Set the width of the bars
bar_width = 0.35

# Set the positions of the bars on the x-axis
bar_positions_group1 = np.arange(len(categories))
bar_positions_group2 = [x + bar_width for x in bar_positions_group1]

# Create bar plot
plt.bar(bar_positions_group1, values_group1,
        color='blue', width=bar_width, label=method_names[0])
plt.bar(bar_positions_group2, values_group2,
        color='orange', width=bar_width, label=method_names[1])

# Add labels and title
plt.xlabel('Test')
plt.ylabel('Number of Expanded Nodes')
plt.title('Bar graph comparing ' +
          method_names[0] + ' and ' + method_names[1] + ' frontier')

# Add x-axis tick labels
plt.xticks([r + bar_width/2 for r in range(len(categories))], categories)

# Add legend
plt.legend()

# Show plot
plt.show()


# Show plot
plt.show()

file_name = 'test/test_3'  # Replace 'your_file.txt' with the path to your file
matrix = read_file_to_matrix(file_name)
[board, targets, state] = game_from_matrix(matrix)
print_game(board, state)

method_heuristic_1 = MethodHeuristic(
    state, fast_anti_livelock(min_manhattan_modified(targets), board))
method_heuristic_2 = MethodHeuristic(
    state, fast_anti_livelock(anti_wall(board, targets, state), board))

method_heuristic_3 = MethodHeuristic(
    state, min_manhattan_modified(targets))
method_heuristic_4 = MethodHeuristic(
    state, anti_wall(board, targets, state))

heuristic_methods = [method_heuristic_1, method_heuristic_2,
                     method_heuristic_3, method_heuristic_4]

# method_a_star_1 = MethodAStar(state, fast_anti_livelock(
#     min_manhattan_modified(targets), board))
# method_a_star_2 = MethodAStar(state, fast_anti_livelock(
#     anti_wall(board, targets, state), board))

# a_star_methods = [method_a_star_1, method_a_star_2]
dataframe = pd.DataFrame(
            0.0, index=heuristic_methods, columns=columns)

for method in heuristic_methods:
    iterations = 10
    durations = []
    for i in range(1, iterations):
        start = time.time()
        solution, explored, frontier = search(copy.deepcopy(method), board, targets)
        # solution, explored, frontier = a_star_search(method_a_star, board, targets)
        end = time.time()
        durations.append(end - start)
        dataframe.at[method, 'cost'] = solution.cost
        dataframe.at[method, 'expanded'] = len(explored)
        dataframe.at[method, 'frontier'] = len(frontier)
    dataframe.at[method, 'mean_time'] = np.mean(durations)
    dataframe.at[method, 'time_error'] = np.std(durations) / iterations**0.5


print(dataframe)

# for method in a_star_methods:
#     start = time.time()
#     solution, explored, frontier = a_star_search(method, board, targets)
#     print(solution)
#     print(len(explored))
#     print(len(frontier))
#     end = time.time()
