import matplotlib.pyplot as plt
import pandas as pd

from helper import get_config_file
from plotting import map_handles_labels, map_names_to_labels


COLOR_DICT = get_config_file('colors.yml')

LABELS = get_config_file('labels.yml')

COLORS_BY_LABEL = {LABELS[key]: value for key, value in COLOR_DICT.items()}


def plot_stacked_bar(df_in, scenario_order, title=None,
                     ylabel=None, ax=None, legend=True,
                     colors=None, yticks=None):

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

    if colors is None:
        colors = [COLORS_BY_LABEL[i] for i in df.columns.get_level_values('name')]

    if ax:
        pass
    else:
        fig, ax = plt.subplots()

    df.plot.bar(ax=ax, color=colors, stacked=True, rot=270)

    ax.grid(axis='y', c='k', linestyle=':')

    ax.set_title(title)

    ax.set_ylabel(ylabel)

    if yticks is not None:
        ax.set_yticks(yticks)

    ax.legend().remove()

    if legend:
        draw_legend(ax, df)


def plot_load_duration(timeseries, legend=True, plot_original=False, title=None, ylabel=None, **kwargs):
    fig, ax = plt.subplots(figsize=(5, 5))

    if plot_original:
        timeseries.plot.line(ax=ax, color=c_list(timeseries, COLOR_DICT), use_index=False, **kwargs)

    # sort timeseries
    if isinstance(timeseries, pd.DataFrame):
        sorted_ts = pd.DataFrame()
        for column in timeseries.columns:
            sorted_ts[column] = sorted(timeseries[column], reverse=True)

    elif isinstance(timeseries, pd.Series):
        sorted_ts = pd.DataFrame({timeseries.name: sorted(timeseries, reverse=True)})

    # keep only nonzero
    sorted_ts = sorted_ts.loc[:, (sorted_ts != 0).any(axis=0)]

    colors = c_list(sorted_ts, COLOR_DICT)
    if plot_original:
        colors = darken_color(colors)

    sorted_ts.plot.line(ax=ax, color=colors, **kwargs)

    ax.set_ylabel(ylabel)
    ax.set_title(title)

    if legend:
        handles, labels = map_handles_labels()
        ax.legend(
            handles=handles,
            labels=labels,
            loc='center left',
            bbox_to_anchor=(1.0, 0.5)
        )
    else:
        plt.legend().remove()

    plt.tight_layout()


def c_list(data, colors):
    if isinstance(data, pd.Series):
        return [colors[data.name]]

    if isinstance(data, pd.DataFrame):
        return [colors[k] for k in data.columns]


def darken_color(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    if isinstance(color, list):
        return [darken_color(c) for c in color]
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))

    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])


def draw_legend(ax, df):
    handles, labels = plt.gca().get_legend_handles_labels()

    labels = list(df.columns.get_level_values('name'))

    d = {l: h for h, l in zip(handles, labels)}

    labels = d.keys()

    handles = d.values()

    ax.legend(
        handles=handles,
        labels=labels,
        loc='center left',
        bbox_to_anchor=(1.0, 0.5)
    )
    plt.tight_layout()


def remove_scenario_index_name(df):

    index_names = list(df.index.names)

    index_names[0] = None

    df.index.names = index_names
