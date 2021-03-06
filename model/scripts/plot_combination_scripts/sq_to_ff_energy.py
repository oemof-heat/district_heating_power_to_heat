import os
import sys

import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tools.helper import get_experiment_dirs, get_scenario_assumptions, get_config_file
from tools.plot_helpers import plot_stacked_bar, remove_scenario_index_name, draw_legend


idx = pd.IndexSlice

COLOR_DICT = get_config_file('colors.yml')

LABELS = get_config_file('labels.yml')

COLORS_BY_LABEL = {LABELS[key]: value for key, value in COLOR_DICT.items()}

rcParams['font.size'] = 16


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

    remove_scenario_index_name(all_scalars)

    fig, axs = plt.subplots(1, 3, figsize=(12, 6), sharey=True)

    legend = False

    for i, (title, scenario_bunch) in enumerate(scenarios.items()):

        slicing = idx[scenario_bunch, :, :, :, ['chp', 'hob', 'hp'], 'yearly_heat']

        select = all_scalars.loc[slicing, :]

        select *= 1e-3  # MWh to GWh

        if i == 2:
            legend=True

        plot_stacked_bar(
            select,
            scenario_bunch,
            title,
            'Yearly heat in GWh',
            ax=axs[i],
            legend=legend,
            yticks=np.arange(0, 350, 50),
        )

    plt.tight_layout()

    filename = os.path.join(dirs['plots'], 'yearly_heat.pdf')

    plt.savefig(filename)

    print(f"Saved plot to {filename}")


if __name__ == '__main__':
    plot()
