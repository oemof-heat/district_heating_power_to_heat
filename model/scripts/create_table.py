import os

import pandas as pd

from helper import get_experiment_dirs, get_scenario_assumptions


def main():
    print("Creating table of scenario assumptions and results")

    dirs = get_experiment_dirs('all_scenarios')

    input_file_path = os.path.join(dirs['postprocessed'], 'scalars.csv')

    all_scalars = pd.read_csv(input_file_path)

    scenario_select = [
        'SQ',
        'SQ-HP-50',
        'SQ-HP-50-COP-175',
        'SQ-HP-50-COP-200',
        'SQ-Std-200',
        'FF-50',
        'FF-70',
        'FF-80',
        'FF-90',
        'FF',
        'FF-COP-75',
        'FF-Mean-150',
        'FF-Std-150',
        'FF-Mean-150-Std-150',
    ]

    def filter_and_round(df, filter, decimals):

        _df = df.copy()

        _df = _df.loc[all_scalars['var_name'] == filter]

        _df = _df[['scenario', 'var_value']].set_index('scenario')

        _df = _df.loc[scenario_select, :]

        _df = _df.round(decimals)

        return _df

    def save_df(df, name):

        output_file_path = os.path.join(dirs['tables'], name)

        df.to_csv(output_file_path)

    share_el_heat = filter_and_round(all_scalars, 'share_el_heat', 2)

    share_el_heat *= 100  # decimals to percent

    spec_cost_of_heat = filter_and_round(all_scalars, 'spec_cost_of_heat', 0)

    results = pd.concat([share_el_heat, spec_cost_of_heat], 1)

    results = results.astype('int')

    save_df(results, name='results.csv')


if __name__ == '__main__':
    scenario_assumptions = get_scenario_assumptions()
    main()
