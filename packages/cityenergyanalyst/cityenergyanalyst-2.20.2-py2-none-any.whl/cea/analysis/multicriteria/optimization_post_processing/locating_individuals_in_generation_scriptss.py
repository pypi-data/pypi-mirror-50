"""
Locating individuals in generation script

In optimization, the best individuals stored might be from different generations. The corresponding files of these
best individuals are not reproduced but referenced based on their generation and the individual number.

This function takes in all the individuals from a generation and links the address of the individual.
For example, from checkpoint of generation 25, the individual 1 is referenced to generation 10 and individual 5
(of that generation)

It creates a csv file, which can be used to do further analysis
"""
from __future__ import division
from __future__ import print_function

import os
import json
import pandas as pd
import numpy as np
import cea.config
import cea.inputlocator
from cea.optimization.constants import NAMES_TECHNOLOGY_OF_INDIVIDUAL

__author__ = "Sreepathi Bhargava Krishna"
__copyright__ = "Copyright 2018, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Sreepathi Bhargava Krishna", "Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def get_pointers_to_correct_individual_generation(generation, individual, locator):
    """
    Until now we need to create a pointer to the real individual of the generation.
    in the optimization of CEA we save time but not running an individual who has been already
    run in another generation. we create an address to understand it later on.
    :param category:
    :param generation:
    :param individual:
    :param locator:
    :return:
    """
    if not os.path.exists(locator.get_address_of_individuals_of_a_generation(generation)):
        data_address = locating_individuals_in_generation_script(generation, locator)
    else:
        data_address = pd.read_csv(locator.get_address_of_individuals_of_a_generation(generation))
    data_address = data_address[data_address['individual_list'] == individual]
    generation_pointer = data_address['generation_number_address'].values[
        0]  # points to the correct file to be referenced from optimization folders
    individual_pointer = data_address['individual_number_address'].values[0]
    individual_pointer = int(individual_pointer)  # updating the individual based on its correct path from the checkpoint

    return generation_pointer, individual_pointer


def locating_individuals_in_generation_script(generation, locator):
    data_generation = preprocessing_generations_data(locator, generation)

    individual_list = data_generation['individual_barcode']

    generation_number_address = []
    individual_number_address = []

    for ind in individual_list:
        generation_number, individual_number = preprocessing_individual_data(locator, data_generation, ind)
        generation_number_address.append(generation_number)
        individual_number_address.append(individual_number)

    results = pd.DataFrame({"individual_list": individual_list,
                            "generation_number_address": generation_number_address,
                            "individual_number_address": individual_number_address
                            })

    results.to_csv(locator.get_address_of_individuals_of_a_generation(generation), index=False)

    return results

def create_data_address_file(locator, generation):
    data_generation = preprocessing_generations_data(locator, generation)

    individual_list = data_generation['final_generation']['individual_barcode'].axes[0]

    generation_number_address = []
    individual_number_address = []

    for i in range(len(individual_list)):
        generation_number, individual_number = generation, i
        generation_number_address.append(generation_number)
        individual_number_address.append(individual_number)

    results = pd.DataFrame({"individual_list": individual_list,
                            "generation_number_address": generation_number_address,
                            "individual_number_address": individual_number_address
                            })

    results.to_csv(locator.get_address_of_individuals_of_a_generation(generation), index=False)
    return results

def preprocessing_individual_data(locator, data_raw, individual):

    # get netwoork name
    # string_network = data_raw['network'].loc[individual].values[0]
    total_demand = pd.read_csv(locator.get_total_demand())
    building_names = total_demand.Name.values

    # get data about hourly demands in these buildings
    # building_demands_df = pd.read_csv(locator.get_optimization_network_results_summary(string_network)).set_index(
    #     "DATE")

    # get data about the activation patterns of these buildings
    individual_barcode_list = data_raw['individual_barcode'][individual]
    df_all_generations = pd.read_csv(locator.get_optimization_all_individuals())

    # The current structure of CEA has the following columns saved, in future, this will be slightly changed and
    # correspondingly these columns_of_saved_files needs to be changed
    columns_of_saved_files = NAMES_TECHNOLOGY_OF_INDIVIDUAL
    for i in building_names:  # DHN
        columns_of_saved_files.append(str(i) + ' DHN')

    for i in building_names:  # DCN
        columns_of_saved_files.append(str(i) + ' DCN')


    df_current_individual = pd.DataFrame(np.zeros(shape = (1, len(columns_of_saved_files))), columns=columns_of_saved_files)
    for i, ind in enumerate((columns_of_saved_files)):
        df_current_individual[ind] = individual_barcode_list[i]
    for i in range(len(df_all_generations)):
        matching_number_between_individuals = 0
        for j in columns_of_saved_files:
            if np.isclose(float(df_all_generations[j][i]), float(df_current_individual[j][0])):
                matching_number_between_individuals = matching_number_between_individuals + 1

        if matching_number_between_individuals >= (len(columns_of_saved_files) - 1):
            # this should ideally be equal to the length of the columns_of_saved_files, but due to a bug, which
            # occasionally changes the type of Boiler from NG to BG or otherwise, this round about is figured for now
            generation_number = df_all_generations['generation'][i]
            individual_number = df_all_generations['individual'][i]

    generation_number = int(generation_number)
    individual_number = int(individual_number)

    return generation_number, individual_number

def preprocessing_generations_data(locator, generations):

    with open(locator.get_optimization_checkpoint(generations), "rb") as fp:
        data = json.load(fp)

    individual_barcode = [[str(ind) if type(ind) == float else str(ind) for ind in
                           individual] for individual in data['tested_population']]

    data_processed = {'individual_barcode': individual_barcode}

    return data_processed


def main(config):
    locator = cea.inputlocator.InputLocator(config.scenario)
    generation = 25 # these are for testing the script, the script will be directly called and not an interface
    individual = 10
    print("Linking the address of all the individuals of generation " + str(generation))

    locating_individuals_in_generation_script(generation, locator)


if __name__ == '__main__':
    main(cea.config.Configuration())