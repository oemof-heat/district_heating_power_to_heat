import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from helper import get_experiment_dirs
from plot_helpers import plot_load_duration


def plot():

    dirs = get_experiment_dirs('all_scenarios')

    price_el = pd.read_csv(
        os.path.join(dirs['raw'], 'price_electricity_spot_2017.csv'),
        index_col=0
    )

    price_el.columns = ['electricity']

    plot_load_duration(
        price_el,
        legend=False,
        plot_original=True,
        title='Electricity prices (buying)',
        ylabel='Hourly price [Eur/MWh]',
    )

    filename = os.path.join(dirs['plots'], 'price_el.pdf')

    plt.savefig(filename)

    plt.close()

    print(f"Saved plot to {filename}")

if __name__ == '__main__':
    plot()
