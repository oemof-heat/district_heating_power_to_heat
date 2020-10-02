import os
import sys

import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from helper import get_experiment_dirs, get_scenario_assumptions, get_config_file
from plot_helpers import plot_stacked_bar, remove_scenario_index_name


idx = pd.IndexSlice

COLOR_DICT = get_config_file('colors.yml')

LABELS = get_config_file('labels.yml')

COLORS_BY_LABEL = {LABELS[key]: value for key, value in COLOR_DICT.items()}

rcParams['font.size'] = 16


def plot():

    dirs = get_experiment_dirs('all_scenarios')

    scenario_order = [
        'scenario_field_0',
        'scenario_field_1',
        'scenario_field_2',
        'scenario_field_3',
        'scenario_field_4',
        'scenario_field_5',
    ]

    all_scalars = pd.read_csv(
        os.path.join(dirs['postprocessed'], 'scalars.csv'),
        index_col=[0,1,2,3,4,5]
    )

    slicing = idx[scenario_order, :, :, :, :, ['capacity_cost', 'carrier_cost', 'marginal_cost']]

    select = all_scalars.copy().loc[slicing, :]

    def group_varom_keep_marginal_cost(df_in):

        df = df_in.copy()

        marginal_cost = df.copy().loc[idx[:, :, :, :, :, 'marginal_cost'], :]

        index_names = df.index.names

        df.reset_index(inplace=True)

        df.loc[:, 'var_name']\
            .replace({'carrier_cost': 'var_om', 'marginal_cost': 'var_om'}, inplace=True)

        df.set_index(index_names, inplace=True)

        df = pd.concat([df, marginal_cost], 0)

        df= df.groupby(index_names).sum()

        return df

    select = group_varom_keep_marginal_cost(select)

    df = select / 300000  # Normalize to heat demand

    remove_scenario_index_name(df)

    plot_stacked_bar(df, scenario_order, 'Costs/Revenues', 'Costs [Eur/MWhth]')

    filename = os.path.join(dirs['plots'], 'costs.pdf')

    plt.savefig(filename)

    print(f"Saved plot to {filename}")


if __name__ == '__main__':
    plot()
