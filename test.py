from src.functions import clear, read_file_to_matrix, game_from_matrix, print_game
from src.methods import MethodDFS, MethodBFS, MethodHeuristic, MethodAStar
from src.heuristics import min_manhattan_modified, min_manhattan, fast_anti_livelock, walkable_distance, anti_wall
from src.search import search, a_star_search
import pandas as pd
import numpy as np
import time
import os


tests = [
    'test/test_1',
    'test/test_4',
    'test/test_5',
    'test/test_6'
]

method_names = ['bfs', 'dfs']
methods = [MethodBFS, MethodDFS]


columns = ['solved', 'mean_time', 'time_error', 'cost', 'expanded', 'frontier', 'solution']
dataframes = {}

def test_not_informed():
    print("Running not informed...")
    for test in tests:
        print(test)
        dataframes[test] = pd.DataFrame(0.0, index=method_names, columns=columns)
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
            dataframes[test].at[method_name, 'time_error'] = np.std(durations) / iterations**0.5
            if solution is not None:
                dataframes[test].at[method_name, 'solved'] = True
                dataframes[test].at[method_name, 'cost'] = solution.cost
            else:
                dataframes[test].at[method_name, 'solved'] = False
                dataframes[test].at[method_name, 'cost'] = 0

            dataframes[test].at[method_name, 'expanded'] = len(explored)
            dataframes[test].at[method_name, 'frontier'] = len(frontier)
    print(dataframes)

def test_informed():
    print("Running informed...")
    method_names = ['Greedy', 'A star']
    
    for test in tests:
        print(test)
        dataframes[test] = pd.DataFrame(0.0, index=method_names, columns=columns)
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
                state, fast_anti_livelock(walkable_distance(board, targets, state), board))
            start = time.time()
            [solution, explored, frontier] = search(method_heuristic, board, targets)
            end = time.time()
            duration = end - start
            durations.append(duration)
        dataframes[test].at[method_names[0], 'mean_time'] = np.mean(durations)
        dataframes[test].at[method_names[0], 'time_error'] = np.std(durations) / iterations**0.5
        if solution is not None:
            dataframes[test].at[method_names[0], 'solved'] = True
            dataframes[test].at[method_names[0], 'cost'] = solution.cost
        else:
            dataframes[test].at[method_names[0], 'solved'] = False
            dataframes[test].at[method_names[0], 'cost'] = 0

        dataframes[test].at[method_names[0], 'expanded'] = len(explored)
        dataframes[test].at[method_names[0], 'frontier'] = len(frontier)
            
        for i in range(1, iterations):
            method_astar = MethodAStar(state, fast_anti_livelock(walkable_distance(board, targets, state),board))
            start = time.time()
            [solution, explored, frontier] = a_star_search(method_astar, board, targets)
            end = time.time()
            duration = end - start
            durations.append(duration)
        dataframes[test].at[method_names[1], 'mean_time'] = np.mean(durations)
        dataframes[test].at[method_names[1], 'time_error'] = np.std(durations) / iterations**0.5
        if solution is not None:
            dataframes[test].at[method_names[1], 'solved'] = True
            dataframes[test].at[method_names[1], 'cost'] = solution.cost
        else:
            dataframes[test].at[method_names[1], 'solved'] = False
            dataframes[test].at[method_names[1], 'cost'] = 0

        dataframes[test].at[method_names[1], 'expanded'] = len(explored)
        dataframes[test].at[method_names[1], 'frontier'] = len(frontier)

    print(dataframes)

#test_not_informed()
test_informed()

"""
{'test/test_1':     solved  mean_time  time_error    cost  expanded  frontier  solution
bfs   True   0.017649     0.00460   470.0     553.0     177.0       0.0
dfs   True   0.012046     0.00235  1760.0     124.0    4608.0       0.0, 'test/test_4':
    solved  mean_time  time_error    cost  expanded  frontier  solution
bfs   True   1.705568    0.064060  1172.0   41245.0     876.0       0.0
dfs   True   0.022788    0.010665  1132.0     278.0    2605.0       0.0, 'test/test_5':
    solved  mean_time  time_error   cost  expanded  frontier  solution
bfs   True   0.384150    0.021139  317.0   10203.0    6413.0       0.0
dfs   True   0.016104    0.005860  357.0     100.0     475.0       0.0, 'test/test_6':
   solved  mean_time  time_error   cost  expanded  frontier  solution
bfs   True   0.811480    0.146367  208.0    4597.0  155487.0       0.0
dfs   True   4.755564    0.496355  788.0     104.0    1524.0       0.0}
"""
