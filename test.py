from src.functions import clear, read_file_to_matrix, game_from_matrix, print_game
from src.methods import MethodDFS, MethodBFS, MethodHeuristic, MethodAStar
from src.heuristics import min_manhattan_modified, min_manhattan, fast_anti_livelock, walkable_distance, anti_wall
from src.search import search, a_star_search
import pandas as pd
import numpy as np
import time
import os
import matplotlib.pyplot as plt


tests = [
    'test/test_1',
    'test/test_3',
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

tiempos_bfs = [dataframes[test].at[method_names[0], 'mean_time'] for test in tests]
errores_bfs = [dataframes[test].at[method_names[0], 'time_error'] for test in tests]
tiempos_dfs = [dataframes[test].at[method_names[1], 'mean_time'] for test in tests]
errores_dfs = [dataframes[test].at[method_names[1], 'time_error'] for test in tests]

plt.rcParams['figure.dpi'] = 300

# Configuración del gráfico
x = range(len(tests))
ancho_barra = 0.35

# Crear gráfico de barras
fig, ax = plt.subplots()
barra_bfs = ax.bar(x, tiempos_bfs, ancho_barra,
                   yerr=errores_bfs, capsize=5, label='Greedy', color='blue')
barra_dfs = ax.bar([i + ancho_barra for i in x], tiempos_dfs, ancho_barra,
                   yerr=errores_dfs, capsize=5, label='A Star', color='orange')

# Etiquetas y título
ax.set_xlabel('Pruebas')
ax.set_ylabel('Tiempo Medio de Ejecución')
ax.set_title(
    'Comparación de Tiempo Medio de Ejecución entre Greedy y A Star por Prueba')
ax.set_xticks([i + ancho_barra / 2 for i in x])
ax.set_xticklabels(tests)
ax.legend()

# Mostrar gráfico
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
