import os

import pandas as pd

from helper import get_experiment_dirs, get_scenario_assumptions


dirs =get_experiment_dirs('all_scenarios')

input_file_path = os.path.join(dirs['postprocessed'], 'scalars.csv')

all_scalars = pd.read_csv(input_file_path)


def filter_and_round(df, filter, scenario_select, decimals):
    _df = df.copy()

    _df = _df.loc[all_scalars['var_name'] == filter]

    _df = _df[['scenario', 'var_value']].set_index('scenario')

    _df = _df.loc[scenario_select, :]

    _df = _df.round(decimals)

    return _df


def filter_assumptions(scenario_assumptions, scenario_select, assumption_select):
    assumptions = scenario_assumptions.loc[
        scenario_assumptions['scenario'].isin(scenario_select)]

    assumptions = assumptions.set_index('scenario')

    assumptions = assumptions[assumption_select]

    return assumptions


def relative_values(assumptions):
    assumptions['overnight_cost_heat_pump'] *= \
        100 / assumptions.loc['SQ', 'overnight_cost_heat_pump']

    assumptions['overnight_cost_heat_pump'] = \
        assumptions['overnight_cost_heat_pump'].round(0).astype('int')

    assumptions['cop_heat_pump'] *= \
        100 / assumptions.loc['SQ', 'cop_heat_pump']

    assumptions['cop_heat_pump'] = \
        assumptions['cop_heat_pump'].round(0).astype('int')

    return assumptions


def save_df(df, name):
    output_file_path = os.path.join(dirs['tables'], name)

    df.to_csv(output_file_path)


def main(scenario_assumptions):
    print("Creating table of scenario assumptions and results")

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

    assumption_select = [
        'charges_tax_levies_gas',
        'charges_tax_levies_el',
        'market_price_el',
        'standard_dev_el',
        'overnight_cost_heat_pump',
        'cop_heat_pump',
    ]

    assumptions = filter_assumptions(scenario_assumptions, scenario_select, assumption_select)

    assumptions = relative_values(assumptions)

    share_el_heat = \
        filter_and_round(all_scalars, 'share_el_heat', scenario_select, decimals=2).astype('int')

    share_el_heat *= 100  # decimals to percent

    spec_cost_of_heat = \
        filter_and_round(all_scalars, 'spec_cost_of_heat', scenario_select, decimals=0) \
            .astype('int')

    results = pd.concat([assumptions, share_el_heat, spec_cost_of_heat], 1, sort=True)

    save_df(results, name='results.csv')


if __name__ == '__main__':
    scenario_assumptions = get_scenario_assumptions()
    main(scenario_assumptions)
