import os
import yaml

import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd

from tools.helper import get_experiment_dirs, get_scenario_assumptions, get_config_file


idx = pd.IndexSlice


def add_index(x, name, value):
    x[name] = value
    x.set_index(name, append=True, inplace=True)
    return x


def get_scenario_paths(scenario_assumptions):
    scenario_paths = {}

    for scenario in scenario_assumptions['scenario']:
        path = get_experiment_dirs(scenario)['postprocessed']

        scenario_paths.update({scenario: path})

    return scenario_paths


def get_scenario_dfs(scenario_paths, file_name):
    scenario_df = {}

    for scenario, path in scenario_paths.items():
        file_path = os.path.join(path, file_name)

        df = pd.read_csv(file_path)

        scenario_df.update({scenario: df})

    return scenario_df


def combine_scalars(scenario_dfs):
    for scenario, df in scenario_dfs.items():
        df.insert(0, 'scenario', scenario)

    all_scalars = pd.concat(scenario_dfs.values(), 0)

    all_scalars.set_index(
        ['scenario', 'name', 'type', 'carrier', 'tech', 'var_name'],
        inplace=True
    )

    return all_scalars


def main(scenario_assumptions):
    print("Combining scenario results")

    dirs = get_experiment_dirs('all_scenarios')

    scenario_paths = get_scenario_paths(scenario_assumptions)

    scenario_dfs = get_scenario_dfs(scenario_paths, 'scalars.csv')

    all_scalars = combine_scalars(scenario_dfs)

    all_scalars.drop('heat-distribution', level='name', inplace=True)

    all_scalars.drop('heat-demand', level='name', inplace=True)

    all_scalars.drop('heat_decentral-shortage', level='name', inplace=True)

    file_path = os.path.join(dirs['postprocessed'], 'scalars.csv')

    all_scalars.to_csv(file_path)

    print(f"Saved scenario results to {file_path}")


if __name__ == '__main__':
    scenario_assumptions = get_scenario_assumptions()
    main(scenario_assumptions)
