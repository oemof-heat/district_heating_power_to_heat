import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tools.helper import get_experiment_dirs
from tools.plot_helpers import plot_load_duration


def plot():

    dirs = get_experiment_dirs('all_scenarios')

    demand_heat = pd.read_csv(
        os.path.join(dirs['raw'], 'demand_heat_2017.csv'),
        index_col=0
    ).sum(1)

    demand_heat.name = 'heat-demand'

    plot_load_duration(
        demand_heat,
        legend=False,
        plot_original=True,
        title='Heat demand',
        ylabel='Hourly heat demand [MWh]',
    )

    filename = os.path.join(dirs['plots'], 'heat_demand.pdf')

    plt.savefig(filename)

    plt.close()

    print(f"Saved plot to {filename}")


if __name__ == '__main__':
    plot()
