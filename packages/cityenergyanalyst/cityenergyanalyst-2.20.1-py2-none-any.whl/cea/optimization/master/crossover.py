"""
CrossOver routine

"""
from __future__ import division
import random
from deap import base
from cea.optimization.constants import N_HEAT, N_SOLAR, N_HR, N_COOL, INDICES_CORRESPONDING_TO_DHN, INDICES_CORRESPONDING_TO_DCN

toolbox = base.Toolbox()


def cxUniform(child1, child2, proba, nBuildings, config):
    """
    Performs a uniform crossover between the two parents.
    Each segments is swapped with probability *proba*
    
    :param child1: a list containing the parameters of the parent 1
    :param child2: a list containing the parameters of the parent 2
    :param proba: Crossover probability
    :type child1: list
    :type child2: list
    :type proba: float

    :return: child1, child2
    :rtype: list, list
    """

    # local variables
    district_heating_network = config.optimization.district_heating_network
    district_cooling_network = config.optimization.district_cooling_network
    
    # Swap functions
    def swap(inda, indb, n):
        inda[n], indb[n] = indb[n], inda[n]

    def cross_integer_variables(child_1, child_2, number_of_plants, index_on_individual):
        for i in range(number_of_plants):
            if random.random() < proba:
                child_1[index_on_individual + 2*i], child_2[index_on_individual + 2*i] = child_2[index_on_individual + 2*i], \
                                                                                     child_1[index_on_individual + 2*i]
    # Swap
    cross_integer_variables(child1, child2, N_HEAT, 0) # crossing the integer variables corresponding to heating technologies
    cross_integer_variables(child1, child2, N_SOLAR, N_HEAT * 2 + N_HR) # crossing the integer variables corresponding to solar technologies
    cross_integer_variables(child1, child2, N_COOL, (N_HEAT + N_SOLAR) * 2 + N_HR + INDICES_CORRESPONDING_TO_DHN) # crossing the integer variables corresponding to cooling technologies
    # Swap heating recovery options
    for i in range(N_HR):
        if random.random() < proba:
            swap(child1, child2, N_HEAT*2 + i)

    # Swap DHN and DCN variables
    for i in range(INDICES_CORRESPONDING_TO_DHN):
        if random.random() < proba:
            swap(child1, child2, (N_HEAT + N_SOLAR) * 2 + N_HR + i)

    for i in range(INDICES_CORRESPONDING_TO_DCN):
        if random.random() < proba:
            swap(child1, child2, (N_HEAT + N_SOLAR) * 2 + N_HR + INDICES_CORRESPONDING_TO_DHN + N_COOL * 2 + i)

    # Swap DHN and DCN, connected buildings
    if district_heating_network:
        for i in range(nBuildings):
            if random.random() < proba:
                swap(child1, child2, (N_HEAT + N_SOLAR) * 2 + N_HR + INDICES_CORRESPONDING_TO_DHN + N_COOL * 2 + INDICES_CORRESPONDING_TO_DCN + i)

    if district_cooling_network:
        for i in range(nBuildings):
            if random.random() < proba:
                swap(child1, child2, (N_HEAT + N_SOLAR) * 2 + N_HR + INDICES_CORRESPONDING_TO_DHN + N_COOL * 2 + INDICES_CORRESPONDING_TO_DCN + nBuildings + i)

    return child1, child2