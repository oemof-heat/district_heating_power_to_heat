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

    scenarios_1 = [
        'SQ',
        'SQ-HP-50',
        'SQ-HP-50-COP-175',
        'SQ-HP-50-COP-200',
        'SQ-Std-200',
    ]

    scenarios_2 = [
        'FF-50',
        'FF-70',
        'FF-80',
        'FF-90',
        'FF',
    ]

    scenarios_3 = [
        'FF-COP-75',
        'FF-Mean-150',
        'FF-Std-150',
        'FF-Mean-150-Std-150',
    ]

    for s in [scenarios_1, scenarios_2, scenarios_3]:
        s = [element + '-KWK' for element in s]

    all_scalars = pd.read_csv(
        os.path.join(dirs['postprocessed'], 'scalars.csv'),
        index_col=[0,1,2,3,4,5]
    )

    remove_scenario_index_name(all_scalars)

    fig, axs = plt.subplots(1, 3, figsize=(12, 5))

    slicing = idx[scenarios_1, :, :, :, :, 'yearly_heat']

    select = all_scalars.loc[slicing, :]

    plot_stacked_bar(select, scenarios_1, 'Status quo', 'Yearly energy [MWh]', ax=axs[0], legend=False)

    slicing = idx[scenarios_2, :, :, :, :, 'yearly_heat']

    select = all_scalars.loc[slicing, :]

    plot_stacked_bar(select, scenarios_2, 'Transition to FF', ax=axs[1], legend=False)

    slicing = idx[scenarios_3, :, :, :, :, 'yearly_heat']

    select = all_scalars.loc[slicing, :]

    plot_stacked_bar(select, scenarios_3, 'FF', ax=axs[2], legend=False)

    plt.tight_layout()

    filename = os.path.join(dirs['plots'], 'yearly_heat.pdf')

    plt.savefig(filename)

    print(f"Saved plot to {filename}")


if __name__ == '__main__':
    plot()
