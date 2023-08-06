"""
This is the dashboard of CEA
"""
from __future__ import division
from __future__ import print_function

import json
import os

import numpy as np
import pandas as pd

import cea.config
import cea.inputlocator
from cea.analysis.multicriteria.optimization_post_processing.individual_configuration import supply_system_configuration
from cea.analysis.multicriteria.optimization_post_processing.locating_individuals_in_generation_script import \
    locating_individuals_in_generation_script
from cea.optimization.lca_calculations import LcaCalculations
from cea.plots.optimization.cost_analysis_curve_centralized import cost_analysis_curve_centralized
from cea.plots.optimization.pareto_capacity_installed import pareto_capacity_installed
from cea.plots.optimization.pareto_curve import pareto_curve


__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2018, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Sreepathi Bhargava Krishna", "Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "2.8"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def plots_main(locator, config):
    # local variables
    generation = config.plots_optimization.generation
    categories = config.plots_optimization.categories

    scenario = config.scenario
    type_of_network = config.plots_optimization.network_type

    # generate plots
    category = "optimization-overview"

    if not os.path.exists(locator.get_address_of_individuals_of_a_generation(generation)):
        data_address = locating_individuals_in_generation_script(generation, locator)
    else:
        data_address = pd.read_csv(locator.get_address_of_individuals_of_a_generation(generation))

    # initialize class
    plots = Plots(locator, generation, config, type_of_network, data_address)

    if "pareto_curve" in categories:
        plots.pareto_curve_for_one_generation(category)

    if "system_sizes" in categories:
        plots.cost_analysis_central_decentral(category)
        if config.plots_optimization.network_type == 'DH':
            plots.comparison_capacity_installed_heating_supply_system_one_generation(category)
        if config.plots_optimization.network_type == 'DC':
            plots.comparison_capacity_installed_cooling_supply_system_one_generation(category)

    if "costs_analysis" in categories:
        plots.cost_analysis_central_decentral(category)
        if config.plots_optimization.network_type == 'DH':
            plots.comparison_capex_opex_heating_supply_system_for_one_generation_per_production_unit(category)
        if config.plots_optimization.network_type == 'DC':
            plots.comparison_capex_opex_cooling_supply_system_for_one_generation_per_production_unit(category)

    return


class Plots(object):

    def __init__(self, locator, generation, config, type_of_network, data_address):
        # local variables
        self.locator = locator
        self.config = config
        self.generation = generation
        self.network_type = type_of_network
        self.final_generation = [generation]
        self.data_address = data_address
        # fields of loads in the systems of heating, cooling and electricity
        self.analysis_fields_cost_cooling_centralized = ["Capex_a_ACH_USD",
                                                         "Capex_a_CCGT_USD",
                                                         "Capex_a_CT_USD",
                                                         "Capex_a_Tank_USD",
                                                         "Capex_a_VCC_USD",
                                                         "Capex_a_VCC_backup_USD",
                                                         "Capex_a_pump_USD",
                                                         "Capex_a_PV_USD",
                                                         "Network_costs_USD",
                                                         "Substation_costs_USD",
                                                         "Opex_var_ACH_USD",
                                                         "Opex_var_CCGT_USD",
                                                         "Opex_var_CT_USD",
                                                         "Opex_var_Lake_USD",
                                                         "Opex_var_VCC_USD",
                                                         "Opex_var_VCC_backup_USD",
                                                         "Opex_var_pumps_USD",
                                                         "Opex_var_PV_USD",
                                                         "Electricitycosts_for_appliances_USD",
                                                         "Electricitycosts_for_hotwater_USD"]

        self.analysis_fields_cost_central_decentral = ["Capex_Centralized_USD",
                                                       "Capex_Decentralized_USD",
                                                       "Opex_Centralized_USD",
                                                       "Opex_Decentralized_USD"]
        self.analysis_fields_cost_heating_centralized = ["Capex_SC_USD",
                                                         "Capex_PVT_USD",
                                                         "Capex_furnace_USD",
                                                         "Capex_Boiler_Total_USD",
                                                         "Capex_CHP_USD",
                                                         "Capex_Lake_USD",
                                                         "Capex_Sewage_USD",
                                                         "Capex_pump_USD",
                                                         "Opex_HP_Sewage_USD",
                                                         "Opex_HP_Lake_USD",
                                                         "Opex_GHP_USD",
                                                         "Opex_CHP_Total_USD",
                                                         "Opex_Furnace_Total_USD",
                                                         "Opex_Boiler_Total_USD",
                                                         "Electricity_Costs_USD"]
        self.analysis_fields_individual_heating = ['Base_boiler_BG_capacity_W', 'Base_boiler_NG_capacity_W',
                                                   'CHP_BG_capacity_W',
                                                   'CHP_NG_capacity_W', 'Furnace_dry_capacity_W',
                                                   'Furnace_wet_capacity_W',
                                                   'GHP_capacity_W', 'HP_Lake_capacity_W', 'HP_Sewage_capacity_W',
                                                   'PVT_capacity_W', 'PV_capacity_W', 'Peak_boiler_BG_capacity_W',
                                                   'Peak_boiler_NG_capacity_W', 'SC_ET_capacity_W', 'SC_FP_capacity_W',
                                                   'Disconnected_Boiler_BG_capacity_W',
                                                   'Disconnected_Boiler_NG_capacity_W',
                                                   'Disconnected_FC_capacity_W',
                                                   'Disconnected_GHP_capacity_W']
        self.analysis_fields_individual_cooling = ['Lake_kW', 'VCC_LT_kW', 'VCC_HT_kW', 'single_effect_ACH_LT_kW',
                                                   'single_effect_ACH_HT_kW', 'DX_kW', 'CHP_CCGT_thermal_kW',
                                                   'Storage_thermal_kW']
        self.individual_barcodes = self.read_barcodes_of_all_individuals_in_generation()
        self.data_processed_cost_centralized = self.preprocessing_final_generation_data_cost_centralized(self.locator,
                                                                                                         self.individual_barcodes,
                                                                                                         self.config,
                                                                                                         self.data_address,
                                                                                                         self.generation)
        self.data_processed_capacities = self.preprocessing_capacities_data(self.locator, self.individual_barcodes,
                                                                            self.generation, self.network_type, config,
                                                                            self.data_address)

    def read_barcodes_of_all_individuals_in_generation(self):

        generation = self.final_generation[0]
        data_processed = []
        with open(self.locator.get_optimization_checkpoint(generation), "rb") as fp:
            data = json.load(fp)
        # get lists of data for performance values of the population
        costs_Mio = [round(objectives[0] / 1000000, 2) for objectives in
                     data['tested_population_fitness']]  # convert to millions
        individual_names = ['ind' + str(i) for i in range(len(costs_Mio))] # TODO: change the way to read ind names
        individual_barcode = [[str(ind) if type(ind) == float else str(ind) for ind in
                               individual] for individual in data['tested_population']]
        df_individual_barcode = pd.DataFrame({'Name': individual_names,
                                               'individual_barcode': individual_barcode}).set_index("Name")
        data_processed = {'individual_barcode': df_individual_barcode}

        return data_processed

    def preprocessing_capacities_data(self, locator, data_generation, generation, network_type, config, data_address):

        if network_type == 'DC':
            column_names = ['Lake_kW', 'VCC_LT_kW', 'VCC_HT_kW', 'single_effect_ACH_LT_kW',
                            'single_effect_ACH_HT_kW', 'DX_kW', 'CHP_CCGT_thermal_kW',
                            'Storage_thermal_kW', 'CT_kW', 'Buildings Connected Share']
        elif network_type == 'DH':
            column_names = ['Boiler_kW', 'CHP_thermal_kW', 'Furnace_kW', 'GHP_kW', 'HPLake_kW', 'HPSewage_kW',
                            'Storage_thermal_kW', 'Buildings Connected Share']

        individual_index = data_generation['individual_barcode'].index.values
        capacities_of_generation = pd.DataFrame(np.zeros([len(individual_index), len(column_names)]),
                                                columns=column_names)

        for i, ind in enumerate(individual_index):

            data_address_individual = data_address[data_address['individual_list'] == ind]

            generation_pointer = data_address_individual['generation_number_address'].values[
                0]  # points to the correct file to be referenced from optimization folders
            individual_pointer = data_address_individual['individual_number_address'].values[0]
            district_supply_sys, building_connectivity = supply_system_configuration(generation_pointer,
                                                                                     individual_pointer, locator,
                                                                                     network_type)

            for name in column_names:
                if name is 'Buildings Connected Share':
                    connected_buildings = len(building_connectivity.loc[building_connectivity.Type == "CENTRALIZED"])
                    total_buildings = connected_buildings + len(
                        building_connectivity.loc[building_connectivity.Type == "DECENTRALIZED"])
                    capacities_of_generation.iloc[i][name] = np.float(connected_buildings * 100 / total_buildings)
                else:
                    capacities_of_generation.iloc[i][name] = district_supply_sys[name].sum()

            print ('retrieved technology capacity data of: ', ind)

        capacities_of_generation['indiv'] = individual_index
        capacities_of_generation.set_index('indiv', inplace=True)
        return {'capacities_of_final_generation': capacities_of_generation}

    def preprocessing_final_generation_data_cost_centralized(self, locator, individual_barcodes, config, data_address, generation):

        total_demand = pd.read_csv(locator.get_total_demand())
        building_names = total_demand.Name.values

        df_all_generations = pd.read_csv(locator.get_optimization_all_individuals())
        preprocessing_costs = pd.read_csv(locator.get_preprocessing_costs())

        # The current structure of CEA has the following columns saved, in future, this will be slightly changed and
        # correspondingly these columns_of_saved_files needs to be changed
        columns_of_saved_files = ['CHP/Furnace', 'CHP/Furnace Share', 'Base Boiler',
                                  'Base Boiler Share', 'Peak Boiler', 'Peak Boiler Share',
                                  'Heating Lake', 'Heating Lake Share', 'Heating Sewage', 'Heating Sewage Share', 'GHP',
                                  'GHP Share',
                                  'Data Centre', 'Compressed Air', 'PV', 'PV Area Share', 'PVT', 'PVT Area Share',
                                  'SC_ET',
                                  'SC_ET Area Share', 'SC_FP', 'SC_FP Area Share', 'DHN Temperature',
                                  'DHN unit configuration',
                                  'Lake Cooling', 'Lake Cooling Share', 'VCC Cooling', 'VCC Cooling Share',
                                  'Absorption Chiller', 'Absorption Chiller Share', 'Storage', 'Storage Share',
                                  'DCN Temperature', 'DCN unit configuration']
        for i in building_names:  # DHN
            columns_of_saved_files.append(str(i) + ' DHN')

        for i in building_names:  # DCN
            columns_of_saved_files.append(str(i) + ' DCN')

        ind_name_list = individual_barcodes['individual_barcode'].index.values
        # build empty data_processed
        if config.plots_optimization.network_type == 'DH':
            df_heating_costs = pd.read_csv(locator.get_optimization_slave_investment_cost_detailed(1, 1))
            column_names = df_heating_costs.columns.values
            column_names = np.append(column_names, ['Opex_HP_Sewage', 'Opex_HP_Lake', 'Opex_GHP', 'Opex_CHP_BG',
                                                    'Opex_CHP_NG', 'Opex_Furnace_wet', 'Opex_Furnace_dry',
                                                    'Opex_BaseBoiler_BG', 'Opex_BaseBoiler_NG', 'Opex_PeakBoiler_BG',
                                                    'Opex_PeakBoiler_NG', 'Opex_BackupBoiler_BG',
                                                    'Opex_BackupBoiler_NG',
                                                    'Capex_SC',
                                                    'Capex_Boiler', 'Opex_Total', 'Capex_Total',
                                                    'Capex_Boiler_Total',
                                                    'Opex_Boiler_Total', 'Opex_CHP_Total', 'Opex_Furnace_Total',
                                                    'Disconnected_costs',
                                                    'Capex_Decentralized', 'Opex_Decentralized', 'Capex_Centralized',
                                                    'Opex_Centralized', 'Electricity_Costs', 'Process_Heat_Costs']) # FIXME: not sure which file should be added to column_names

            data_processed = pd.DataFrame(np.zeros([len(individual_barcodes['individual_barcode']), len(column_names)]),
                                          columns=column_names)

        elif config.plots_optimization.network_type == 'DC':
            data_cost_path = os.path.join(
                locator.get_optimization_slave_investment_cost_detailed_cooling(1, 1))
            df_cooling_costs = pd.read_csv(data_cost_path)
            column_names = df_cooling_costs.columns.values
            column_names = np.append(column_names,
                                     ['Opex_var_ACH_USD', 'Opex_var_CCGT_USD', 'Opex_var_CT_USD', 'Opex_var_Lake_USD', 'Opex_var_VCC_USD',
                                      'Opex_var_PV_USD',
                                      'Opex_var_VCC_backup_USD', 'Capex_ACH_USD', 'Capex_CCGT_USD', 'Capex_CT_USD', 'Capex_Tank_USD',
                                      'Capex_VCC_USD', 'Capex_a_PV_USD',
                                      'Capex_VCC_backup_USD', 'Opex_Total_USD', 'Capex_Total_USD', 'Opex_var_pumps_USD',
                                      'Disconnected_costs_USD',
                                      'Capex_Decentralized_USD', 'Opex_Decentralized_USD', 'Capex_Centralized_USD',
                                      'Opex_Centralized_USD', 'Electricitycosts_for_hotwater_USD',
                                      'Electricitycosts_for_appliances_USD', 'Process_Heat_Costs_USD', 'Network_costs_USD',
                                      'Substation_costs_USD'])

            data_processed = pd.DataFrame(np.zeros([len(individual_barcodes['individual_barcode']), len(column_names)]),
                                          columns=column_names)
        # get mcda
        try:
            data_mcda = pd.read_csv(locator.get_multi_criteria_analysis(generation))
        except IOError:
            raise IOError("Please run the multi-criteria analysis tool first for the generation you would like to visualize")

        # write individual costs into data_processed
        for index in range(len(ind_name_list)):
            # build empty df_current_individual
            individual_barcode = individual_barcodes['individual_barcode'].loc[ind_name_list[index]].values[0]
            df_current_individual = pd.DataFrame(np.zeros(shape=(1, len(columns_of_saved_files))),
                                                 columns=columns_of_saved_files)
            # write costs into df_current_individual
            for i, column in enumerate(columns_of_saved_files):
                df_current_individual[column] = individual_barcode[i]

            # points to the correct file to be referenced from optimization folders
            data_address_individual = data_address[data_address['individual_list'] == ind_name_list[index]]
            generation_pointer = data_address_individual['generation_number_address'].values[0]
            individual_pointer = data_address_individual['individual_number_address'].values[0]

            if config.plots_optimization.network_type == 'DH':
                df_heating_costs = pd.read_csv(locator.get_optimization_slave_investment_cost_detailed(individual_pointer, generation_pointer))
                df_heating = pd.read_csv(locator.get_optimization_slave_heating_activation_pattern(individual_pointer, generation_pointer)).set_index("DATE")
                # write individual costs into data_processed
                for column_name in df_heating_costs.columns.values:
                    data_processed.loc[index][column_name] = df_heating_costs[column_name].values

                data_processed.loc[index]['Opex_HP_Sewage'] = np.sum(df_heating['Opex_var_HP_Sewage'])
                data_processed.loc[index]['Opex_HP_Lake'] = np.sum(df_heating['Opex_var_HP_Lake'])
                data_processed.loc[index]['Opex_GHP'] = np.sum(df_heating['Opex_var_GHP'])
                data_processed.loc[index]['Opex_CHP_BG'] = np.sum(df_heating['Opex_var_CHP_BG'])
                data_processed.loc[index]['Opex_CHP_NG'] = np.sum(df_heating['Opex_var_CHP_NG'])
                data_processed.loc[index]['Opex_Furnace_wet'] = np.sum(df_heating['Opex_var_Furnace_wet'])
                data_processed.loc[index]['Opex_Furnace_dry'] = np.sum(df_heating['Opex_var_Furnace_dry'])
                data_processed.loc[index]['Opex_BaseBoiler_BG'] = np.sum(df_heating['Opex_var_BaseBoiler_BG'])
                data_processed.loc[index]['Opex_BaseBoiler_NG'] = np.sum(df_heating['Opex_var_BaseBoiler_NG'])
                data_processed.loc[index]['Opex_PeakBoiler_BG'] = np.sum(df_heating['Opex_var_PeakBoiler_BG'])
                data_processed.loc[index]['Opex_PeakBoiler_NG'] = np.sum(df_heating['Opex_var_PeakBoiler_NG'])
                data_processed.loc[index]['Opex_BackupBoiler_BG'] = np.sum(
                    df_heating['Opex_var_BackupBoiler_BG'])
                data_processed.loc[index]['Opex_BackupBoiler_NG'] = np.sum(
                    df_heating['Opex_var_BackupBoiler_NG'])

                data_processed.loc[index]['Capex_SC'] = data_processed.loc[index]['Capex_a_SC_FP_USD'] + \
                                                                  data_processed.loc[index]['Opex_fixed_SC'] # TODO: find out how this is saved in optimization outputs. how to know if is FP or ET in use?
                data_processed.loc[index]['Capex_PVT'] = data_processed.loc[index]['Capex_a_PVT'] + \
                                                                   data_processed.loc[index]['Opex_fixed_PVT']
                data_processed.loc[index]['Capex_Boiler_backup'] = data_processed.loc[index][
                                                                                 'Capex_a_Boiler_backup'] + \
                                                                             data_processed.loc[index][
                                                                                 'Opex_fixed_Boiler_backup']
                data_processed.loc[index]['Capex_storage_HEX'] = data_processed.loc[index][
                                                                               'Capex_a_storage_HEX'] + \
                                                                           data_processed.loc[index][
                                                                               'Opex_fixed_storage_HEX']
                data_processed.loc[index]['Capex_furnace'] = data_processed.loc[index][
                                                                           'Capex_a_furnace'] + \
                                                                       data_processed.loc[index][
                                                                           'Opex_fixed_furnace']
                data_processed.loc[index]['Capex_Boiler'] = data_processed.loc[index][
                                                                          'Capex_a_Boiler'] + \
                                                                      data_processed.loc[index][
                                                                          'Opex_fixed_Boiler']
                data_processed.loc[index]['Capex_Boiler_peak'] = data_processed.loc[index][
                                                                               'Capex_a_Boiler_peak'] + \
                                                                           data_processed.loc[index][
                                                                               'Opex_fixed_Boiler_peak']
                data_processed.loc[index]['Capex_Lake'] = data_processed.loc[index][
                                                                        'Capex_a_Lake'] + \
                                                                    data_processed.loc[index][
                                                                        'Opex_fixed_Lake']
                data_processed.loc[index]['Capex_Sewage'] = data_processed.loc[index][
                                                                          'Capex_a_Sewage'] + \
                                                                      data_processed.loc[index][
                                                                          'Opex_fixed_Boiler']
                data_processed.loc[index]['Capex_pump'] = data_processed.loc[index][
                                                                        'Capex_a_pump'] + \
                                                                    data_processed.loc[index][
                                                                        'Opex_fixed_pump']
                data_processed.loc[index]['Capex_CHP'] = data_processed.loc[index]['Capex_a_CHP'] + \
                                                                   data_processed.loc[index]['Opex_fixed_CHP']
                data_processed.loc[index]['Disconnected_costs'] = df_heating_costs['CostDiscBuild']

                data_processed.loc[index]['Capex_Boiler_Total'] = data_processed.loc[index][
                                                                                'Capex_Boiler'] + \
                                                                            data_processed.loc[index][
                                                                                'Capex_Boiler_peak'] + \
                                                                            data_processed.loc[index][
                                                                                'Capex_Boiler_backup']
                data_processed.loc[index]['Opex_Boiler_Total'] = data_processed.loc[index][
                                                                               'Opex_BackupBoiler_NG'] + \
                                                                           data_processed.loc[index][
                                                                               'Opex_BackupBoiler_BG'] + \
                                                                           data_processed.loc[index][
                                                                               'Opex_PeakBoiler_NG'] + \
                                                                           data_processed.loc[index][
                                                                               'Opex_PeakBoiler_BG'] + \
                                                                           data_processed.loc[index][
                                                                               'Opex_BaseBoiler_NG'] + \
                                                                           data_processed.loc[index][
                                                                               'Opex_BaseBoiler_BG']
                data_processed.loc[index]['Opex_CHP_Total'] = data_processed.loc[index][
                                                                            'Opex_CHP_NG'] + \
                                                                        data_processed.loc[index][
                                                                            'Opex_CHP_BG']

                data_processed.loc[index]['Opex_Furnace_Total'] = data_processed.loc[index][
                                                                                'Opex_Furnace_wet'] + \
                                                                            data_processed.loc[index][
                                                                                'Opex_Furnace_dry']

                data_processed.loc[index]['Electricity_Costs'] = preprocessing_costs['elecCosts'].values[0]
                data_processed.loc[index]['Process_Heat_Costs'] = preprocessing_costs['hpCosts'].values[0]

                data_processed.loc[index]['Opex_Centralized'] \
                    = data_processed.loc[index]['Opex_HP_Sewage'] + data_processed.loc[index][
                    'Opex_HP_Lake'] + \
                      data_processed.loc[index]['Opex_GHP'] + data_processed.loc[index][
                          'Opex_CHP_BG'] + \
                      data_processed.loc[index]['Opex_CHP_NG'] + data_processed.loc[index][
                          'Opex_Furnace_wet'] + \
                      data_processed.loc[index]['Opex_Furnace_dry'] + data_processed.loc[index][
                          'Opex_BaseBoiler_BG'] + \
                      data_processed.loc[index]['Opex_BaseBoiler_NG'] + data_processed.loc[index][
                          'Opex_PeakBoiler_BG'] + \
                      data_processed.loc[index]['Opex_PeakBoiler_NG'] + data_processed.loc[index][
                          'Opex_BackupBoiler_BG'] + \
                      data_processed.loc[index]['Opex_BackupBoiler_NG'] + \
                      data_processed.loc[index]['Electricity_Costs'] + data_processed.loc[index][
                          'Process_Heat_Costs']

                data_processed.loc[index]['Capex_Centralized'] = data_processed.loc[index][
                                                                               'Capex_SC'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_PVT'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_Boiler_backup'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_storage_HEX'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_furnace'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_Boiler'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_Boiler_peak'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_Lake'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_Sewage'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_pump']

                data_processed.loc[index]['Capex_Decentralized'] = df_heating_costs['Capex_Disconnected']
                data_processed.loc[index]['Opex_Decentralized'] = df_heating_costs['Opex_Disconnected']
                data_processed.loc[index]['Capex_Total'] = data_processed.loc[index][
                                                                         'Capex_Centralized'] + \
                                                                     data_processed.loc[index][
                                                                         'Capex_Decentralized']
                data_processed.loc[index]['Opex_Total'] = data_processed.loc[index][
                                                                        'Opex_Centralized'] + \
                                                                    data_processed.loc[index][
                                                                        'Opex_Decentralized']

            elif config.plots_optimization.network_type == 'DC':
                data_mcda_ind = data_mcda[data_mcda['individual'] == ind_name_list[index]]

                for column_name in df_cooling_costs.columns.values:
                    data_processed.loc[index][column_name] = df_cooling_costs[column_name].values[0]

                data_processed.loc[index]['Opex_var_ACH_USD'] = data_mcda_ind['Opex_total_ACH_USD'].values[0] - \
                                                                      data_mcda_ind['Opex_fixed_ACH_USD'].values[0]
                data_processed.loc[index]['Opex_var_CCGT_USD'] = data_mcda_ind['Opex_total_CCGT_USD'].values[0] - \
                                                                       data_mcda_ind['Opex_fixed_CCGT_USD'].values[0]
                data_processed.loc[index]['Opex_var_CT_USD'] = data_mcda_ind['Opex_total_CT_USD'].values[0] - \
                                                                     data_mcda_ind['Opex_fixed_CT_USD'].values[0]
                data_processed.loc[index]['Opex_var_Lake_USD'] = data_mcda_ind['Opex_total_Lake_USD'].values[0] - \
                                                                       data_mcda_ind['Opex_fixed_Lake_USD'].values[0]
                data_processed.loc[index]['Opex_var_VCC_USD'] = data_mcda_ind['Opex_total_VCC_USD'].values[0] - \
                                                                      data_mcda_ind['Opex_fixed_VCC_USD'].values[0]
                data_processed.loc[index]['Opex_var_VCC_backup_USD'] = \
                data_mcda_ind['Opex_total_VCC_backup_USD'].values[0] - data_mcda_ind['Opex_fixed_VCC_backup_USD'].values[0]
                data_processed.loc[index]['Opex_var_pumps_USD'] = data_mcda_ind['Opex_var_pump_USD'].values[0]
                data_processed.loc[index]['Opex_var_PV_USD'] = data_mcda_ind['Opex_total_PV_USD'].values[0] - \
                                                                     data_mcda_ind['Opex_fixed_PV_USD'].values[0]

                data_processed.loc[index]['Capex_a_ACH_USD'] = (
                        data_mcda_ind['Capex_a_ACH_USD'].values[0] + data_mcda_ind['Opex_fixed_ACH_USD'].values[0])
                data_processed.loc[index]['Capex_a_CCGT_USD'] = data_mcda_ind['Capex_a_CCGT_USD'].values[0] + \
                                                                      data_mcda_ind['Opex_fixed_CCGT_USD'].values[0]
                data_processed.loc[index]['Capex_a_CT_USD'] = data_mcda_ind['Capex_a_CT_USD'].values[0] + \
                                                                    data_mcda_ind['Opex_fixed_CT_USD'].values[0]
                data_processed.loc[index]['Capex_a_Tank_USD'] = data_mcda_ind['Capex_a_Tank_USD'].values[0] + \
                                                                      data_mcda_ind['Opex_fixed_Tank_USD'].values[0]
                data_processed.loc[index]['Capex_a_VCC_USD'] = (
                        data_mcda_ind['Capex_a_VCC_USD'].values[0] + data_mcda_ind['Opex_fixed_VCC_USD'].values[0])
                data_processed.loc[index]['Capex_a_VCC_backup_USD'] = (data_mcda_ind['Capex_a_VCC_backup_USD'].values[
                                                                                0] + data_mcda_ind[
                                                                                'Opex_fixed_VCC_backup_USD'].values[0])
                data_processed.loc[index]['Capex_a_pump_USD'] = (data_mcda_ind['Capex_pump_USD'].values[0] + \
                                                                      data_mcda_ind['Opex_fixed_pump_USD'].values[0])
                data_processed.loc[index]['Capex_a_PV_USD'] = data_mcda_ind['Capex_a_PV_USD'].values[0]
                data_processed.loc[index]['Substation_costs_USD'] = data_mcda_ind['Substation_costs_USD'].values[0]
                data_processed.loc[index]['Network_costs_USD'] = data_mcda_ind['Network_costs_USD'].values[0]

                data_processed.loc[index]['Capex_Decentralized_USD'] = data_mcda_ind['Capex_a_disconnected_USD']
                data_processed.loc[index]['Opex_Decentralized_USD'] = data_mcda_ind['Opex_total_disconnected_USD']

                lca = LcaCalculations(locator, config.detailed_electricity_pricing)

                data_processed.loc[index]['Electricitycosts_for_hotwater_USD'] = (
                        data_mcda_ind['Electricity_for_hotwater_GW'].values[0] * 1000000000 * lca.ELEC_PRICE.mean())
                data_processed.loc[index]['Electricitycosts_for_appliances_USD'] = (
                        data_mcda_ind['Electricity_for_appliances_GW'].values[0] * 1000000000 * lca.ELEC_PRICE.mean())
                data_processed.loc[index]['Process_Heat_Costs'] = preprocessing_costs['hpCosts'].values[0]

                data_processed.loc[index]['Opex_Centralized_USD'] = data_processed.loc[index][
                                                                              'Opex_var_ACH_USD'] + \
                                                                          data_processed.loc[index][
                                                                              'Opex_var_CCGT_USD'] + \
                                                                          data_processed.loc[index][
                                                                              'Opex_var_CT_USD'] + \
                                                                          data_processed.loc[index][
                                                                              'Opex_var_Lake_USD'] + \
                                                                          data_processed.loc[index][
                                                                              'Opex_var_VCC_USD'] + \
                                                                          data_processed.loc[index][
                                                                              'Opex_var_VCC_backup_USD'] + \
                                                                          data_processed.loc[index][
                                                                              'Opex_var_pumps_USD'] + \
                                                                          data_processed.loc[index][
                                                                              'Electricitycosts_for_hotwater_USD'] + \
                                                                          data_processed.loc[index][
                                                                              'Process_Heat_Costs_USD'] + \
                                                                          data_processed.loc[index][
                                                                              'Opex_var_PV_USD'] + \
                                                                          data_processed.loc[index][
                                                                              'Electricitycosts_for_appliances_USD']

                data_processed.loc[index]['Capex_Centralized_USD'] = data_processed.loc[index][
                                                                               'Capex_a_ACH_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_a_CCGT_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_a_CT_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_a_Tank_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_a_VCC_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_a_VCC_backup_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_pump_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Opex_fixed_ACH_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Opex_fixed_CCGT_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Opex_fixed_CT_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Opex_fixed_Tank_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Opex_fixed_VCC_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Opex_fixed_VCC_backup_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Opex_fixed_pump_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Capex_a_PV_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Substation_costs_USD'] + \
                                                                           data_processed.loc[index][
                                                                               'Network_costs_USD']

                data_processed.loc[index]['Capex_Total_USD'] = data_processed.loc[index][
                                                                         'Capex_Centralized_USD'] + \
                                                                     data_processed.loc[index][
                                                                         'Capex_Decentralized_USD']
                data_processed.loc[index]['Opex_Total_USD'] = data_processed.loc[index][
                                                                        'Opex_Centralized_USD'] + \
                                                                    data_processed.loc[index][
                                                                        'Opex_Decentralized_USD']

        individual_names = ['column' + str(i) for i in data_processed.index.values]
        data_processed['indiv'] = individual_names
        data_processed.set_index('indiv', inplace=True)
        return data_processed

    def erase_zeros(self, data, fields):
        analysis_fields_no_zero = []
        for field in fields:
            if isinstance(data[field], float):
                sum = data[field]
            else:
                sum = data[field].sum()
            if not np.isclose(sum, 0.0):
                analysis_fields_no_zero += [field]
        return analysis_fields_no_zero

    def preprocessing_multi_criteria_data(self, locator, generation):
        try:
            data_multi_criteria = pd.read_csv(locator.get_multi_criteria_analysis(generation))
        except IOError:
            raise IOError("Please run the multi-criteria analysis tool first for the generation you would like to visualize")

        return data_multi_criteria

    def pareto_curve_for_one_generation(self, category):
        title = 'Pareto curve for generation ' + str(self.final_generation[0])
        output_path = self.locator.get_timeseries_plots_file('gen' + str(self.final_generation[0]) + '_pareto_curve',
                                                             category)
        objectives = ['TAC_Mio', 'total_emissions_kiloton', 'total_prim_energy_TJ']
        analysis_fields = ['individual', 'TAC_Mio', 'total_emissions_kiloton', 'total_prim_energy_TJ',
                           'renewable_share_electricity',
                           'Capex_total_Mio', 'Opex_total_Mio']
        data = self.preprocessing_multi_criteria_data(self.locator, self.final_generation[0])
        plot = pareto_curve(data, objectives, analysis_fields, title, output_path)
        return plot

    def comparison_capacity_installed_heating_supply_system_one_generation(self, category):
        title = 'Capacity installed in generation ' + str(self.final_generation[0])
        output_path = self.locator.get_timeseries_plots_file(
            'gen' + str(self.final_generation[0]) + '_centralized_and_decentralized_capacities_installed', category)
        data = self.data_processed_capacities['capacities_of_final_generation'].copy()
        analysis_fields_clean = self.erase_zeros(data, self.analysis_fields_individual_heating)
        plot = pareto_capacity_installed(data, analysis_fields_clean, title, output_path)
        return plot

    def comparison_capacity_installed_cooling_supply_system_one_generation(self, category):
        title = 'Capacity installed in generation' + str(self.final_generation[0])
        output_path = self.locator.get_timeseries_plots_file(
            'gen' + str(self.final_generation[0]) + '_centralized_and_decentralized_capacities_installed', category)
        data = self.data_processed_capacities['capacities_of_final_generation'].copy()
        analysis_fields_clean = self.erase_zeros(data, self.analysis_fields_individual_cooling)
        plot = pareto_capacity_installed(data, analysis_fields_clean, title, output_path)
        return plot

    def comparison_capex_opex_cooling_supply_system_for_one_generation_per_production_unit(self, category):
        title = 'CAPEX vs. OPEX district cooling network for every optimal supply system scenario in generation ' + str(
            self.final_generation[0])
        output_path = self.locator.get_timeseries_plots_file(
            'gen' + str(self.final_generation[0]) + '_centralized_costs_per_generation_unit', category)
        data = self.data_processed_cost_centralized.copy()
        plot = cost_analysis_curve_centralized(data, self.analysis_fields_cost_cooling_centralized, title, output_path)
        return plot

    def comparison_capex_opex_heating_supply_system_for_one_generation_per_production_unit(self, category):
        title = 'CAPEX vs. OPEX of centralized system in generation ' + str(self.final_generation)
        output_path = self.locator.get_timeseries_plots_file(
            'gen' + str(self.final_generation[0]) + '_centralized_costs_per_generation_unit', category)
        data = self.data_processed_cost_centralized.copy()
        plot = cost_analysis_curve_centralized(data, self.analysis_fields_cost_heating_centralized, title, output_path)
        return plot

    def cost_analysis_central_decentral(self, category):
        title = 'CAPEX vs. OPEX of centralized system in generation ' + str(self.final_generation[0])
        output_path = self.locator.get_timeseries_plots_file(
            'gen' + str(self.final_generation[0]) + '_centralized_and_decentralized_costs_total', category)
        data = self.data_processed_cost_centralized.copy()
        plot = cost_analysis_curve_centralized(data, self.analysis_fields_cost_central_decentral, title, output_path)
        return plot


def main(config):
    locator = cea.inputlocator.InputLocator(config.scenario)

    print("Running dashboard with scenario = %s" % config.scenario)
    print("Running dashboard with the next generation = %s" % config.plots_optimization.generation)

    plots_main(locator, config)


if __name__ == '__main__':
    main(cea.config.Configuration())
