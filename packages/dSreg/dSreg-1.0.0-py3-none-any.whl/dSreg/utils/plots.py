#!/usr/bin/env python
from matplotlib.gridspec import GridSpec
from pandas.util.testing import isiterable
from seaborn.distributions import _statsmodels_univariate_kde

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Define parameters labels
PARAMS_LABELS = {}


# Functions
def init_fig(nrow=1, ncol=1, figsize=None, style='white',
             colsize=3, rowsize=3):
    sns.set_style(style)
    if figsize is None:
        figsize = (colsize * ncol, rowsize * nrow)
    fig, axes = plt.subplots(nrow, ncol, figsize=figsize)
    return(fig, axes)


def savefig(fig, fpath):
    fig.tight_layout()
    fig.savefig(fpath, format=fpath.split('.')[-1], dpi=180)
    plt.close()


def create_patches_legend(axes, colors_dict, loc=1, **kwargs):
    axes.legend(handles=[mpatches.Patch(color=color, label=label)
                         for label, color in sorted(colors_dict.items())],
                loc=loc, **kwargs)


def arrange_plot(axes, xlims=None, ylims=None, xlabel=None, ylabel=None,
                 showlegend=False, legend_loc=None, hline=None,
                 rotate_xlabels=False, cols_legend=1, rotation=90,
                 legend_frame=False, title=None, ticklabels_size=None,
                 yticklines=False, xticklines=False, fontsize=None, vline=None,
                 despine=True, despine_left=False, despine_bottom=False,
                 show_yticklabels=True, show_xticklabels=True):
    if xlims is not None:
        axes.set_xlim(xlims)
    if ylims is not None:
        axes.set_ylim(ylims)
    if title is not None:
        axes.set_title(title)

    if xlabel is not None:
        axes.set_xlabel(xlabel, fontsize=fontsize)
    if ylabel is not None:
        axes.set_ylabel(ylabel, fontsize=fontsize)

    if showlegend:
        axes.legend(loc=legend_loc, ncol=cols_legend,
                    frameon=legend_frame, fancybox=legend_frame)
    elif axes.legend_ is not None:
        axes.legend_.set_visible(False)

    if hline is not None:
        xlims = axes.get_xlim()
        axes.plot(xlims, (hline, hline), linewidth=1, color='grey',
                  linestyle='--')
        axes.set_xlim(xlims)

    if vline is not None:
        if not isiterable(vline):
            vline = [vline]
        ylims = axes.get_ylim()
        for x in vline:
            axes.plot((x, x), ylims, linewidth=0.7, color='grey',
                      linestyle='--')
        axes.set_ylim(ylims)

    if rotate_xlabels:
        axes.set_xticklabels(axes.get_xticklabels(), rotation=rotation)
    if not show_xticklabels:
        axes.set_xticklabels([])
    if ticklabels_size is not None:
        for tick in axes.xaxis.get_major_ticks():
            tick.label.set_fontsize(ticklabels_size)
        for tick in axes.yaxis.get_major_ticks():
            tick.label.set_fontsize(ticklabels_size)
    if yticklines:
        xlims = axes.get_xlim()
        for y in axes.get_yticks():
            axes.plot(xlims, (y, y), lw=0.4, alpha=0.2, c='grey')
    if not show_yticklabels:
        axes.set_yticklabels([])
        axes.set_yticks([])

    if xticklines:
        ylims = axes.get_ylim()
        for x in axes.get_xticks():
            axes.plot((x, x), ylims, lw=0.4, alpha=0.2, c='grey')

    if despine:
        sns.despine(ax=axes, left=despine_left, bottom=despine_bottom)


def _plot_post_pred_ax(x, q, axes, color):
    axes.fill_between(x, q[0, :], q[-1, :], facecolor=color,
                      interpolate=True, alpha=0.1)
    axes.fill_between(x, q[1, :], q[-2, :], facecolor=color,
                      interpolate=True, alpha=0.1)
    axes.fill_between(x, q[2, :], q[-3, :], facecolor=color,
                      interpolate=True, alpha=0.1)
    axes.fill_between(x, q[3, :], q[-4, :], facecolor=color,
                      interpolate=True, alpha=0.1)
    axes.fill_between(x, q[4, :], q[-5, :], facecolor=color,
                      interpolate=True, alpha=0.2)
    axes.plot(x, q[5, :], color=color, linewidth=2)


def plot_post_pred(axes, y_preds, x_pred=None, xs=None, ys=None,
                   color='purple'):
    percs = [2.5, 5, 10, 25, 40, 50, 60, 75, 90, 95, 97.5]
    q = np.percentile(y_preds, q=percs, axis=0)

    if x_pred is None:
        x_pred = np.arange(q.shape[1])

    _plot_post_pred_ax(x_pred, q, axes, color=color)
    if xs is not None and ys is not None:
        axes.plot(xs, ys, color='black', lw=1.5)


def add_panel_label(axes, label, fontsize=20, yfactor=0.03, xfactor=0.215):
    xlims, ylims = axes.get_xlim(), axes.get_ylim()
    x = xlims[0] - (xlims[1] - xlims[0]) * xfactor
    y = ylims[1] + (ylims[1] - ylims[0]) * yfactor
    axes.text(x, y, label, fontsize=fontsize)


def plot_traces(traces, params, fpath):
    fig, subplots = init_fig(nrow=len(params), ncol=2, colsize=4,
                             rowsize=2, style='white')
    for i, param in enumerate(params):
        sample = np.array(traces[param])
        if len(set(sample)) > 1:
            sns.kdeplot(sample, shade=False, ax=subplots[i][0])

        x = np.arange(sample.shape[0])
        subplots[i][1].plot(x, sample,
                            linewidth=0.2)
        subplots[i][0].set_ylabel('Density')
        subplots[i][0].set_xlabel(param)
        subplots[i][1].set_xlabel('Iteration')
        subplots[i][1].set_ylabel(param)
    savefig(fig, fpath)


def joyplots(x, y, data, fig, gs, gs_xs, gs_ys, hue=None, yoverlap=1,
             palette=None, color='purple', alpha=1, showlabels=True,
             label_xfactor=0, label_yfactor=0.3, showlegend=True,
             xlabel=None, ylabel=None, panel_label=None, panel_label_xfactor=0,
             whiteline=True, lw=1.2, groups=None, xlims=None,
             xticks=None, title=None):
    if groups is None:
        groups = data[y].unique()
    n_axes = groups.shape[0]
    total_size = gs_ys[1] - gs_ys[0]
    axes_h = (total_size + yoverlap * (n_axes - 1)) / n_axes

    if palette is None and hue is not None:
        hue_values = data[hue].unique()
        palette = dict(zip(hue_values,
                           sns.color_palette(n_colors=hue_values.shape[0])))

    ystart = gs_ys[0]
    all_xlims = None
    axes_list = []
    for label in groups:
        yend = int(ystart + axes_h) - 1
        try:
            axes = fig.add_subplot(gs[ystart:yend, gs_xs[0]:gs_xs[1]])
        except IndexError:
            axes = fig.add_subplot(gs[ystart:yend - 1, gs_xs[0]:gs_xs[1]])
        ystart = yend - yoverlap

        if hue is None:
            xs = data.loc[data[y] == label, x].dropna()
            if xs.shape[0] > 2:
                sns.kdeplot(xs, shade=True, ax=axes, alpha=alpha, color=color,
                            lw=0.5)
                if whiteline:
                    sns.kdeplot(xs, shade=False, ax=axes, color='white',
                                lw=lw, label='_nolegend_', legend=False)
            ymax = axes.get_ylim()[1]
        else:
            ymax = 0
            for group, color in palette.items():
                sel_rows = np.logical_and(data[y] == label, data[hue] == group)
                xs = data.loc[sel_rows, x].dropna()
                if xs.shape[0] > 2:
                    sns.kdeplot(xs, shade=True, ax=axes, alpha=alpha,
                                color=color, label=group, lw=0)
                    if whiteline:
                        sns.kdeplot(xs, shade=False, ax=axes, color='white',
                                    lw=lw, label='_nolegend_', legend=False)
                    ymax = max(ymax, max(_statsmodels_univariate_kde(np.array(xs), kernel="gau", bw="scott", gridsize=100, cut=3, clip=[-0.3, 0.3])[1]))

        if xlims is None:
            xlims = axes.get_xlim()
        if ymax == 0:
            ymax = axes.get_ylim()
        ylims = (0, 1.1 * ymax)
        axes.set_ylim(ylims)
        axes.set_xlabel('')
        axes.set_ylabel('')
        axes.set_xticklabels([])
        axes.set_yticklabels([])

        if axes.legend_ is not None:
            axes.legend_.set_visible(False)
        if all_xlims is None:
            all_xlims = xlims
        else:
            all_xlims = (min(all_xlims[0], xlims[0]),
                         max(all_xlims[1], xlims[1]))
        sns.despine(ax=axes, left=True)
        axes_list.append(axes)

    for axes, label in zip(axes_list, groups):
        axes.plot(all_xlims, (0, 0), lw=1.5, color='black')
        axes.set_xlim(all_xlims)
        ylims = axes.get_ylim()
        if showlabels:
            x = all_xlims[0] + label_xfactor * (all_xlims[1] - all_xlims[0])
            y = ylims[0] + label_yfactor * (ylims[1] - ylims[0])
            axes.text(x, y, label, fontsize=9)

    if xticks is not None:
        axes_list[-1].set_xticks(xticks)
    else:
        xticks = axes_list[-1].get_xticks()
    axes_list[-1].set_xticklabels(['{:.1f}'.format(x) for x in xticks],
                                  fontsize=7)
    if showlegend and hue is not None:
        create_patches_legend(axes_list[0], palette, loc=(0, 1), ncol=2,
                              fontsize=8)
    if xlabel is not None:
        axes_list[-1].set_xlabel(xlabel)
    if ylabel is not None:
        axes_list[int(len(axes_list) / 2)].set_ylabel(ylabel)
    if title is not None:
        axes_list[0].set_title(title, fontsize=7)
    if panel_label is not None:
        add_panel_label(axes_list[0], panel_label, xfactor=panel_label_xfactor)


def get_panel_subplots(fig, gs, nrow, ncol, xs, ys, yspace=2, xspace=2):
    subplots = []

    ysize = (ys[1] - ys[0] - yspace * (nrow - 1)) / (nrow)
    y_intervals = [[int(ys[0] + ysize * i + yspace * i),
                    int(ys[0] + ysize * i + yspace * i + ysize)]
                   for i in range(nrow)]

    xsize = (xs[1] - xs[0] - xspace * (ncol - 1)) / (ncol)
    x_intervals = [[int(xs[0] + xsize * i + xspace * i),
                    int(xs[0] + xsize * i + xspace * i + xsize)]
                   for i in range(ncol)]

    for ystart, yend in y_intervals:
        for xstart, xend in x_intervals:
            subplots.append(fig.add_subplot(gs[ystart:yend, xstart:xend]))
    return(subplots)


def plot_dsreg_pw_results(posterior, data, means, out_fpath, plot_top_n=5,
                          axes_size=15, spacing=3, figsize=(10, 6),
                          add_traces=False):
    # Figure
    sns.set(style="white")
    ysize = axes_size * plot_top_n
    xsize = 65
    if add_traces:
        xsize += 35
        figsize = (figsize[0], figsize[1] + 2)
    fig = plt.figure(figsize=figsize)
    gs = GridSpec(ysize, xsize)

    # Boxplots with posterior differences in activities
    axes = fig.add_subplot(gs[:, :30])
    order = means.sort_values().index
    sns.boxplot(y='variable', x='value', data=data, showfliers=False,
                ax=axes, orient='horizontal', linewidth=0.5, order=order)
    axes.set_yticklabels([])
    arrange_plot(axes, ylabel='Regulator $w$', xticklines=True, despine=True,
                 xlabel=r'Regulator $\theta_{w}$', showlegend=False)
    xlims = axes.get_xlim()

    # Add density plots for top N hits
    sel_rbps = np.abs(means).sort_values().index[-plot_top_n:]
    sel_rbps = means[sel_rbps].sort_values().index
    for i, rbp in enumerate(sel_rbps):
        ystart = i * axes_size
        yend = ystart + axes_size

        # Histogram
        axes = fig.add_subplot(gs[(ystart + spacing):yend, 35:65])
        x = posterior[rbp]
        x = x[np.logical_and(x < xlims[1], x > xlims[0])]

        sns.distplot(x, bins=30, hist=True, kde=False,
                     norm_hist=True, ax=axes)
        arrange_plot(axes, ylabel=r'P($\theta_{w}$| I, T, S)',
                     xlabel='', vline=0, despine=True,
                     xlims=xlims, show_yticklabels=False,
                     show_xticklabels=False)
        ylims = axes.get_ylim()
        axes.text(xlims[0] + 0.1 * (xlims[1] - xlims[0]),
                  ylims[1] - 0.1 * (ylims[1] - ylims[0]), rbp)
        axes.set_xlim(xlims)

        # Traces
        if add_traces:
            axes2 = fig.add_subplot(gs[(ystart + spacing):yend, 75:])
            axes2.plot(np.arange(posterior.shape[0]), posterior[rbp], lw=0.3)
            arrange_plot(axes2, ylabel=r'$\theta_{i}$',
                         xlabel='', hline=0, ylims=xlims)

        ystart = yend

    axes.set_xlabel(r'$\theta_{w}$')
    if add_traces:
        axes2.set_xlabel('Iteration')

    # Save figure
    fig.savefig(out_fpath, format=out_fpath.split('.')[-1], dpi=240)


def plot_dsreg_ts_results(max_diffs, theta, rbp_names, out_fpath,
                          plot_top_n=5, figsize=(8, 8), axes_size=15,
                          spacing=3, add_traces=False):
    # Figure
    sns.set(style="white")
    ysize = axes_size * plot_top_n
    xsize = 105
    if add_traces:
        xsize += 35
        figsize = (figsize[0] + 4, figsize[1])
    fig = plt.figure(figsize=figsize)
    gs = GridSpec(ysize, xsize)

    # Plot deltas distribution
    means = max_diffs.groupby('rbp')['delta'].mean()
    order = means.sort_values().index
    axes = fig.add_subplot(gs[:, :28])
    sns.boxplot(x='delta', y='rbp', data=max_diffs,
                order=order, orient='h', showfliers=False, ax=axes)
    arrange_plot(axes, xlabel=r'$\Delta\theta$',
                 ylabel=r'Regulator $w$', show_yticklabels=False,
                 xticklines=True)
    xlims = axes.get_xlim()

    # Plot estimated activities over time
    sel_rbps = np.abs(means).sort_values().index[-plot_top_n:]
    sel_rbps = means[sel_rbps].sort_values().index
    sel_idxs = [i for i, rbp in enumerate(rbp_names) if rbp in sel_rbps]

    for i, (idx, rbp) in enumerate(zip(sel_idxs, sel_rbps)):
        ystart = i * axes_size
        yend = ystart + axes_size

        # Histogram
        axes = fig.add_subplot(gs[(ystart + spacing):yend, 38:63])
        values = max_diffs.loc[max_diffs['rbp'] == rbp, 'delta']
        values = values[np.logical_and(values < xlims[1], values > xlims[0])]
        sns.distplot(values, bins=30, hist=True, kde=False,
                     norm_hist=True, ax=axes)
        arrange_plot(axes, ylabel=r'P($\Delta\theta_{w}$| I, T, S)',
                     xlabel='' if i < (plot_top_n - 1) else r'$\Delta\theta$',
                     vline=0, despine=True,
                     xlims=xlims, show_yticklabels=False,
                     show_xticklabels=i == (plot_top_n - 1))

        # Posterior predictive distribution along time
        axes = fig.add_subplot(gs[(ystart + spacing):yend, -27:])
        y = theta[:, :, idx]
        plot_post_pred(axes, y)
        arrange_plot(axes, xlabel='' if i < (plot_top_n - 1) else 'Time',
                     ylabel=r'{}-$\theta$'.format(rbp),
                     hline=0, show_xticklabels=False)

        # Add traces for delta theta
        if add_traces:
            axes2 = fig.add_subplot(gs[(ystart + spacing):yend, 78:102])
            axes2.plot(np.arange(values.shape[0]), values, lw=0.3)
            arrange_plot(axes2, ylabel=r'{}-$\Delta\theta$'.format(rbp),
                         xlabel='' if i < (plot_top_n - 1) else 'Iteration',
                         hline=0, show_xticklabels=i == (plot_top_n - 1))

        ystart = yend

    # Save figure
    fig.savefig(out_fpath, format=out_fpath.split('.')[-1], dpi=240)
