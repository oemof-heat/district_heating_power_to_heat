import os
import sys

import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from helper import get_experiment_dirs, get_scenario_assumptions, get_config_file
from plot_helpers import plot_stacked_bar, remove_scenario_index_name


idx = pd.IndexSlice

COLOR_DICT = get_config_file('colors.yml')

LABELS = get_config_file('labels.yml')

COLORS_BY_LABEL = {LABELS[key]: value for key, value in COLOR_DICT.items()}

rcParams['font.size'] = 16


def group_varom_cost(df_in):
    r"""
    Takes a MultiIndex'ed DataFrame with index levels
    ['scenario', 'name', 'type', 'carrier', 'tech', 'var_name']
    and a column 'var_value' and returns a  MultiIndex'ed DataFrame
    with the entries with carrier_cost and marginal_cost aggregated into
    var_om.

    Parameters
    ----------
    df_in : pd.DataFrame

    Returns
    -------
    df : pd.DataFrame
    """
    # Make a copies, one of which will remain, the other be grouped.
    df = df_in.copy()

    index_names = df.index.names

    df.reset_index(inplace=True)

    df.loc[:, 'var_name'] \
        .replace({'carrier_cost': 'var_om', 'marginal_cost': 'var_om'}, inplace=True)

    df.set_index(index_names, inplace=True)

    df = df.groupby(index_names).sum()

    return df


def plot():

    dirs = get_experiment_dirs('all_scenarios')

    scenarios = {
        'Status quo': [
            'SQ',
            'SQ-CHP',
            'SQ-HP-50',
            'SQ-HP-50-COP-175',
            'SQ-HP-50-COP-200',
            'SQ-Std-200',
         ],
        'Transition to FF': [
            'FF-50',
            'FF-70',
            'FF-80',
            'FF-90',
        ],
        'FF': [
            'FF',
            'FF-COP-75',
            'FF-Mean-150',
            'FF-Std-150',
            'FF-Mean-150-Std-150',
        ],
    }

    all_scalars = pd.read_csv(
        os.path.join(dirs['postprocessed'], 'scalars.csv'),
        index_col=[0,1,2,3,4,5]
    )

    fig, axs = plt.subplots(1, 3, figsize=(12, 6), sharey=True)

    for i, (title, scenario_bunch) in enumerate(scenarios.items()):

        slicing = idx[scenario_bunch, :, :, :, :, ['capacity_cost', 'carrier_cost', 'marginal_cost']]

        select = all_scalars.loc[slicing, :]

        # select = group_varom_cost(select)

        remove_scenario_index_name(select)

        select = select / 300000  #TODO: Find a better solution than this fix.

        plot_stacked_bar(
            select,
            scenario_bunch,
            title,
            ax=axs[i],
            legend=False,
            yticks=np.arange(-100, 120, 20),
        )

    filename = os.path.join(dirs['plots'], 'costs.pdf')

    axs[0].set_ylabel('Cost of heat in Eur/MWh')

    plt.tight_layout()

    plt.savefig(filename)

    print(f"Saved plot to {filename}")


if __name__ == '__main__':
    plot()
