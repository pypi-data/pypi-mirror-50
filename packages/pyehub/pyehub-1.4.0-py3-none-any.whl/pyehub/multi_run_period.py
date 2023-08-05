import argparse
import os
import numpy as np
import copy

from energy_hub.param_var import ConstantOrVar
from energy_hub import EHubModel
from energy_hub.utils import constraint
from energy_hub.input_data import InputData
from outputter import print_section, output_excel
import excel_to_request_format
import pylp
from pylp import RealVariable, BinaryVariable, IntegerVariable

import pdb

DOMAIN_TO_VARIABLE = {
    'Continuous': RealVariable,
    'Integer': IntegerVariable,
    'Binary': BinaryVariable,
}


@constraint()
def same_converter_constraint(converter, hubs):
    """
    Constraint to ensure the capacities are kept constant across all the subproblems. 
    """
    #TODO: Check that storage capacites are also kept the same
    for i in range(len(hubs)-1):
        yield hubs[i].capacities[converter] == hubs[i+1].capacities[converter]

@constraint()
def same_storage_constraint(storage, hubs):
    """
    Constraint to ensure the capacities are kept constant across all the subproblems. 
    """
    #TODO: Check that storage capacites are also kept the same
    for i in range(len(hubs)-1):
        yield hubs[i].storage_capacity[storage] == hubs[i+1].storage_capacity[storage]    


def split_hubs(excel=None, request=None, max_carbon=None, num_periods=1, len_periods=24, num_periods_in_sample_period=1, sample_period_position=0):
    """
    Splits a PyEHub into a series of smaller hubs with a given period.
    """
    if excel:
        request = excel_to_request_format.convert(excel)

    if request:
        _data = InputData(request)
    else:
        raise RuntimeError("Can't create hubs with no data.")
        
    hubs = []

    if ((num_periods*len_periods*num_periods_in_sample_period) > len(request['time_series'][0]['data'])):
        raise IndexError("Not enough data to cover all the periods.")
    
    if (num_periods_in_sample_period <= sample_period_position):
        raise IndexError("Not enough periods in sample to start at the given position.")

    for i in range(0, num_periods):
        temp_request = copy.deepcopy(request)
        for stream in temp_request['time_series']:
            stream['data'] = stream['data'][len_periods*(i + i*(num_periods_in_sample_period-1) + sample_period_position) :
                len_periods*(i+1 + i*(num_periods_in_sample_period-1) + sample_period_position)]

        hub = EHubModel(request=temp_request, max_carbon=max_carbon)
        hubs.append(hub)
    return hubs

def merge_hubs(hubs):
    """
    Compiles and combines the constraints of each subproblem into one list.
    :param hubs: List of EHubs.
    :return: The list of constraints for each hub combined with the capacities constraint to ensure the same converter capacities across all EHubs.
    """
    constraints = []
    for hub in hubs:
        hub.recompile()
        for constr in hub.constraints:
            constraints.append(constr)

    for converter in hubs[0].technologies:
        for c in same_converter_constraint(converter, hubs):
            constraints.append(c)
    
    for storage in hubs[0].storages:
        for c in same_storage_constraint(storage, hubs):
            constraints.append(c)

    return constraints

#TODO: Finish and move to outputter?
def multi_run_output(hubs, factor):
    """
    Function for collecting the correct info from the multiple EHub models and combining them into one set of results
    :param hubs: the EHub models now containing their solutions
    :param factor: If the models are samples for larger time scales
    """

    absolute_cost = hubs[0].solution_dict['investment_cost']
    for result in hubs:
        absolute_cost += result.solution_dict['maintenance_cost']*factor +  result.solution_dict['operating_cost']* factor
    return absolute_cost

def run_split_period(excel=None, request=None, output_filename=None, max_carbon=None, num_periods=1, len_periods=24, num_periods_in_sample_period=1, sample_period_position=0, solver='glpk'):
    """
    Core function for splitting a PyEHub model into smaller problems to solve together.
    :param excel: Input excel file if the hub to be split is in excel. Converted into request format before being split into subproblems.
    :param request: Input in request JSON format if the hub to be split is in JSON.
    :param output_filename: Name for file to right the output to if an output file is being used.
    :param max_carbon: Max carbon value if using a capped carbon value.
    :param num_periods: Number of sub problem EHubs to be solved together.
    :param len_periods: Number of time steps per sub problem EHub to be solved.
    :param num_periods_in_sample_period: Number of periods being grouped together to be represented by 1 sub problem EHub. Example: One week representing a whole month would be ~four periods in a sample period.
    :param sample_period_position: Which period in the grouped sample to use as the representative EHub. Example the second week of every month would be two.
    :param solver: Which MILP solver to use.
    """
    hubs = split_hubs(excel, request, max_carbon, num_periods, len_periods, num_periods_in_sample_period, sample_period_position)
    constraints = merge_hubs(hubs)

    #TODO: Make sure storage looping is working for each sub_hub

    #FIXME: Ralph had specific instructions for how to handle the objective (wanting a single one or something)
    # "Make the objective function only one of the investment consts (since they're all the same) 
    # plus the operating cost for each sub-hub scaled by an appropriate factor to represent the whole year.""
    # objective = hubs[0].investment_cost
    # for hub in hubs:
    #     objective += hub.operating_cost*(num_periods_in_sample_period) + hub.maintenance_cost*(num_periods_in_sample_period)
    #If I don't set the function to this the investement costs are not balanced across the sub problems and the accuracy goes down.
    #In taking the total_cost for the final solution the investement cost should only be counted once
    objective = hubs[0].investment_cost
    for hub in hubs:
        objective += hub.operating_cost + hub.maintenance_cost


    status = pylp.solve(objective=objective, constraints=constraints, minimize=True, solver=solver)

    output = multi_run_output(hubs, num_periods_in_sample_period)

    return status, hubs, output

    #TODO: Figure out setting up the output