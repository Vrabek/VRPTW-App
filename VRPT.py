"""Vehicles Routing Problem (VRP) with Time Windows main code."""
import numpy as np
import streamlit as st
from scipy.spatial import distance_matrix

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import pandas as pd



# Python program to compute distance matrix
 
# import important libraries
 
# Create the matrix


 
# Display the matrix
 
# compute the distance matrix
#dist_mat = distance_matrix(x, x, p=2)
 
# display distance matrix

def calculate_distance_matrix(point_coords):
    return distance_matrix(point_coords, point_coords, p=1)

def create_data_model():
    """ Inicjalizacja parametrów i danych problemu VRTW"""
    data = {}
    
    data['point_coords'] = np.array([[0,0],[4,-4],[4,4],[3,-4],[3,-3],[2,1],[2,3],[1, -1], [1, 2], [-1, 1], [-1, 4], [-2, -3], [-2, -2],[-3, -1], [-3, 2], [-4, -4], [-4, 3]])
    data['time_matrix'] = calculate_distance_matrix(data['point_coords'])


    # data['time_matrix'] = [
    #     [0, 6, 9, 8, 7, 3, 6, 2, 3, 2, 6, 6, 4, 4, 5, 9, 7],
    #     [6, 0, 8, 3, 2, 6, 8, 4, 8, 8, 13, 7, 5, 8, 12, 10, 14],
    #     [9, 8, 0, 11, 10, 6, 3, 9, 5, 8, 4, 15, 14, 13, 9, 18, 9],
    #     [8, 3, 11, 0, 1, 7, 10, 6, 10, 10, 14, 6, 7, 9, 14, 6, 16],
    #     [7, 2, 10, 1, 0, 6, 9, 4, 8, 9, 13, 4, 6, 8, 12, 8, 14],
    #     [3, 6, 6, 7, 6, 0, 2, 3, 2, 2, 7, 9, 7, 7, 6, 12, 8],
    #     [6, 8, 3, 10, 9, 2, 0, 6, 2, 5, 4, 12, 10, 10, 6, 15, 5],
    #     [2, 4, 9, 6, 4, 3, 6, 0, 4, 4, 8, 5, 4, 3, 7, 8, 10],
    #     [3, 8, 5, 10, 8, 2, 2, 4, 0, 3, 4, 9, 8, 7, 3, 13, 6],
    #     [2, 8, 8, 10, 9, 2, 5, 4, 3, 0, 4, 6, 5, 4, 3, 9, 5],
    #     [6, 13, 4, 14, 13, 7, 4, 8, 4, 4, 0, 10, 9, 8, 4, 13, 4],
    #     [6, 7, 15, 6, 4, 9, 12, 5, 9, 6, 10, 0, 1, 3, 7, 3, 10],
    #     [4, 5, 14, 7, 6, 7, 10, 4, 8, 5, 9, 1, 0, 2, 6, 4, 8],
    #     [4, 8, 13, 9, 8, 7, 10, 3, 7, 4, 8, 3, 2, 0, 4, 5, 6],
    #     [5, 12, 9, 14, 12, 6, 6, 7, 3, 3, 4, 7, 6, 4, 0, 9, 2],
    #     [9, 10, 18, 6, 8, 12, 15, 8, 13, 9, 13, 3, 4, 5, 9, 0, 9],
    #     [7, 14, 9, 16, 14, 8, 5, 10, 6, 5, 4, 10, 8, 6, 2, 9, 0],
    #]
    data['time_windows'] = [
        (0, 5),  # depot
        (7, 12),  # 1
        (10, 15),  # 2
        (16, 18),  # 3
        (10, 13),  # 4
        (0, 5),  # 5
        (5, 10),  # 6
        (0, 4),  # 7
        (5, 10),  # 8
        (0, 3),  # 9
        (10, 16),  # 10
        (10, 15),  # 11
        (0, 5),  # 12
        (5, 10),  # 13
        (7, 8),  # 14
        (10, 15),  # 15
        (11, 15),  # 16
    ]
    data['num_vehicles'] = 4
    data['depot'] = 0
    return data


    
def VRPTW_Algorithm():
    """Solve the VRP with time windows."""
    # Instantiate the data problem.
    #data = create_data_model()

    #handle session state data model!
    data = st.session_state.data_model

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Time Windows constraint.
    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        30,  # allow waiting time
        30,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == data['depot']:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(int(time_window[0]), int(time_window[1]))
    # Add time window constraints for each vehicle start node.
    depot_idx = data['depot']
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            int(data['time_windows'][depot_idx][0]),
            int(data['time_windows'][depot_idx][1]))

    # Instantiate route start and end times to produce feasible times.
    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    return data, manager, routing, solution




def solution_cost_json():
    """Formalizuje finalny koszt (rozwiązanie) problemu do postaci (JSON)"""
    _, _, _, solution = VRPTW_Algorithm()

    print(f'Objective: {solution.ObjectiveValue()}')

    final_cost = solution.ObjectiveValue()
    json_final_cost = final_cost  #jsonify(final_cost)

    return json_final_cost

def solution_routes_json():
    """Formalizuje wygenerowane trasy dla problemu do postaci słownika (JSON)"""
    data, manager, routing, solution = VRPTW_Algorithm()
    final_routes = {}

    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        vehicle_number = vehicle_id+1
        output_list = []

        while not routing.IsEnd(index):

            output_list.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))

        output_list.append(manager.IndexToNode(index))

        final_routes['Vehicle {}'.format(vehicle_number)] = output_list
        json_final_routes = final_routes#jsonify(final_routes)
        
    return json_final_routes


def solution_full_json():
    """Formalizuje pełne dane dla wyniku algorytmu do postaci słownika (JSON)."""

    data, manager, routing, solution = VRPTW_Algorithm()

    time_dimension = routing.GetDimensionOrDie('Time')
    final_solution = {}
    total_time = 0


    final_solution['Final cost'] = solution.ObjectiveValue()

    for vehicle_id in range(data['num_vehicles']):

        index = routing.Start(vehicle_id)
        vehicle_number = vehicle_id+1
        plan_output = ''
        route_time = 0

        output_list = []
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), solution.Min(time_var),
                solution.Max(time_var))
            index = solution.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        plan_output += '{0} Time({1},{2})\n'.format(manager.IndexToNode(index),
                                                    solution.Min(time_var),
                                                    solution.Max(time_var))
        
        route_time += solution.Min(time_var)

        output_list.append({'Route and time windows': plan_output})
        output_list.append({'Route time': route_time})
        final_solution['Vehicle {}'.format(vehicle_number)] = output_list
        total_time += solution.Min(time_var)
    
    final_solution['Total time'] = total_time

    return final_solution

