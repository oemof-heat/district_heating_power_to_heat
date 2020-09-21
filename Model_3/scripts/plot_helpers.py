import matplotlib.pyplot as plt

from helper import get_config_file
from plotting import map_handles_labels, map_names_to_labels


COLOR_DICT = get_config_file('colors.yml')

LABELS = get_config_file('labels.yml')

COLORS_BY_LABEL = {LABELS[key]: value for key, value in COLOR_DICT.items()}


def plot_stacked_bar(df_in, scenario_order, title=None, ylabel=None, ax=None, legend=True):
    df = df_in.copy()

    df = df.loc[(abs(df['var_value']) > 1e-9)]

    df.index = df.index.droplevel([2, 3, 4])

    df = df.unstack(level=[1, 2])

    df = df.loc[scenario_order]

    # exclude values that are close to zero
    df = df.loc[:, (abs(df) > 1e-9).any(axis=0)]

    df.columns = df.columns.remove_unused_levels()

    df.columns = df.columns.set_levels(map_names_to_labels(df.columns.levels[1]), level=1)

    df = df.reindex(['CHP', 'HOB', 'TES cen.', 'HP', 'TES dec.'], level='name', axis=1)

    colors = [COLORS_BY_LABEL[i] for i in df.columns.get_level_values('name')]

    if ax:
        pass
    else:
        fig, ax = plt.subplots()

    df.plot.bar(ax=ax, color=colors, stacked=True, rot=270)

    ax.grid(axis='y', c='k', linestyle=':')

    ax.set_title(title)

    ax.set_ylabel(ylabel)

    ax.legend().remove()

    if legend:
        draw_legend(ax, df)


def draw_legend(ax, df):
    handles, labels = plt.gca().get_legend_handles_labels()

    ax.legend(
        handles=handles,
        labels=list(df.columns.get_level_values('name')),
        loc='center left',
        bbox_to_anchor=(1.0, 0.5)
    )
    plt.tight_layout()
