import os

import pandas as pd

from helper import get_experiment_dirs


def main():
    print("Creating table of scenario results")

    dirs = get_experiment_dirs('all_scenarios')

    input_file_path = os.path.join(dirs['postprocessed'], 'scalars.csv')

    all_scalars = pd.read_csv(input_file_path)

    def filter_and_round(filter):
        scenarios = [
            'SQ',
            'SQ-HP-50',
            'SQ-HP-50-COP-150',
            'SQ-Std-150',
            'SQ-Std-200',
            'FF-20',
            'FF-40',
            'FF-60',
            'FF-80',
            'FF',
            'FF-COP-75',
            'FF-Mean-150',
            'FF-Std-200',
        ]

        df = all_scalars.loc[all_scalars['var_name'] == filter]

        df = df[['scenario', 'var_value']].set_index('scenario')

        df = df.loc[scenarios, :]

        df = df.round(2)

        return df

    def save_df(df, name):

        output_file_path = os.path.join(dirs['tables'], name)

        df.to_csv(output_file_path)

    share_el_heat = filter_and_round('share_el_heat')

    save_df(share_el_heat, name='share_el_heat.csv')

    spec_cost_of_heat = filter_and_round('spec_cost_of_heat')

    save_df(spec_cost_of_heat, name='spec_cost_of_heat.csv')


if __name__ == '__main__':
    main()
