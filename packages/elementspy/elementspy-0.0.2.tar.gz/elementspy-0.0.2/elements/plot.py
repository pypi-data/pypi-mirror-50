import collections
import logging

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


CURVE = dict()
AREA = dict(alpha=0.15, linewidths=0)
SCATTER = dict(alpha=0.15, linewidths=0, s=20)
DIST = dict(interpolation='none')
LINE = dict(ls='--', color='#444444')
COLORS = (
    '#377eb8', '#4daf4a', '#e41a1c', '#984ea3', '#ff7f00', '#ffff33',
    '#a65628', '#f781bf', '#888888')
LEGEND = dict(fontsize='medium', labelspacing=0, numpoints=1)


class Plot:

  def __init__(
      self, title=None, xlabel=None, ylabel=None, size=(4, 3), ax=None):
    self._ax = ax or plt.subplots(figsize=size)[1]
    title and self._ax.set_title(title)
    xlabel and self._ax.set_xlabel(xlabel)
    ylabel and self._ax.set_ylabel(ylabel)
    self._index = 0
    self._xlim = (np.inf, -np.inf)
    self._random = np.random.RandomState(seed=0)
    self._logger = logging.getLogger('plot')

  def curve(
      self, name, xs, ys,
      bins=None,
      curve=np.mean,
      area=lambda x: (np.mean(x) - np.std(x), np.mean(x) + np.std(x)),
      scatter=False,
      smooth=None):
    assert len(xs.shape) == 1 and len(ys.shape) == 1
    self._update_xlim(xs)
    xs, ys, bins = self._sort_series(xs, ys, bins)
    binned_xs, binned_ys = self._bin_series(xs, ys, bins)
    curve_ys = np.array([curve(y) for y in ys])
    binned_curve_ys = np.array([curve(y) for y in binned_ys])
    if curve:
      config = CURVE.copy()
      config['color'] = self._current_color()
      config['zorder'] = 1000 - 10 * self._index
      config['label'] = name
      if smooth:
        data = self._smooth(xs, curve_ys, smooth)
      else:
        data = binned_xs, binned_curve_ys
      self._ax.plot(*data, **config)
    if scatter:
      config = SCATTER.copy()
      config['color'] = self._current_color()
      config['zorder'] = 1000 - 10 * self._index - 1
      config['label'] = name if not curve else None
      self._ax.scatter(xs, ys, **config)
    if area:
      config = AREA.copy()
      config['color'] = self._current_color()
      config['zorder'] = 1000 - 10 * self._index - 2
      config['label'] = name if (not curve and not scatter) else None
      below, above = np.array([area(y) for y in binned_ys]).T
      self._ax.fill_between(binned_xs, below, above, **config)
    self._index += 1

  def dist(self, name, xs, ys, resolution=20, xlim=None, ylim=None):
    assert len(xs.shape) == 1 and len(ys.shape) == 1
    self._update_xlim(xs)
    xs, ys, _ = self._sort_series(xs, ys, None)
    xlim = xs.min(), xs.max()
    ylim = ys.min(), ys.max()
    xbins = np.linspace(*xlim, resolution)
    ybins = np.linspace(*ylim, resolution)
    xi, yi = np.meshgrid(xbins, ybins)
    xbins = np.linspace(*xlim, resolution + 1, endpoint=True)
    ybins = np.linspace(*ylim, resolution + 1, endpoint=True)
    zi = np.histogram2d(xs, ys, [xbins, ybins])[0].T.reshape(xi.shape)
    color = self._current_color()
    make_cmap = mpl.colors.LinearSegmentedColormap.from_list
    config = DIST.copy()
    config['cmap'] = make_cmap('name', [color + '00', color + 'ff'])
    config['zorder'] = 1000 - 10 * self._index
    config['aspect'] = 'auto'
    config['extent'] = (*xlim, *ylim)
    self._ax.matshow(zi.reshape((resolution, resolution)), **config)
    # Add empty area to create legend entry.
    self._ax.fill_between([], [], [], color=color, label=name)
    self._index += 1

  def line(self, name, ys):
    config = LINE.copy()
    config['color'] = self._current_color()
    config['zorder'] = 1000 - 10 * self._index
    config['label'] = name
    self._ax.axhline(ys, **config)
    self._index += 1

  def legend(self):
    config = LEGEND.copy()
    legend = self._ax.legend(**config)
    legend.set_zorder(2000)
    legend.get_frame().set_edgecolor('white')
    for line in legend.get_lines():
      line.set_alpha(1)

  def save(self, filename):
    fig = self._ax.figure
    fig.tight_layout()
    config = {}
    config['transparent'] = str(filename).endswith('png')
    fig.savefig(filename, **config)

  def _sort_series(self, xs, ys, bins):
    order = np.argsort(xs)
    xs = np.array(xs)[order]
    ys = np.array(ys)[order]
    if bins is not None and len(bins) == len(xs):
      bins = np.array(bins)[order]
    return xs, ys, bins

  def _bin_series(self, xs, ys, bins):
    # Assume input arguments are already sorted.
    if bins is None:
      binned_xs = np.array(sorted(set(xs)))
    elif isinstance(bins, int):
      binned_xs = np.linspace(*self._xlim, bins + 1)
    elif len(bins) == len(xs):
      binned_xs = []
      current = None
      for x, bin_ in zip(xs, bins):
        if not current or current != bin_:
          current = bin_
          binned_xs.append(x)
      binned_xs.append(xs[-1])
      binned_xs = np.array(binned_xs)
    else:
      message = 'Bins should be None, int, or an int list of data size.'
      raise ValueError(message)
    binned_ys = []
    for start, stop in zip([-np.inf] + list(binned_xs), binned_xs):
      left = (xs < start).sum()
      right = (xs <= stop).sum()
      if not (left < right):
        message = 'Empty segment from {} to {} in curve.'
        self._logger.warn(message.format(left, right))
        continue
      binned_ys.append(ys[left:right])
    return binned_xs, binned_ys

  def _update_xlim(self, xs):
    self._xlim = min(self._xlim[0], xs.min()), max(self._xlim[1], xs.max())
    self._ax.set_xlim(self._xlim)

  def _current_color(self):
    return COLORS[min(self._index, len(COLORS) - 1)]

  def _smooth(self, xs, ys, amount):
    # Add noise to avoid duplicate X values.
    epsilon = 1e-6 * (xs.min() - xs.max())
    xs += self._random.uniform(-epsilon, epsilon, xs.shape)
    xs, ys, _ = self._sort_series(xs, ys, None)
    import scipy.interpolate
    assert 0 <= amount <= 1, amount
    strength2 = (len(xs) ** (1 - amount) - 1) / (len(xs) - 1)
    amount = 2 + int(strength2 * (len(xs) - 4))
    indices = np.linspace(1, len(xs) - 2, amount).astype(int)
    knots = xs[indices]
    # The degree k makes a big difference. Degree 1 results in piece-wise
    # linear interpolation but works well for all smoothing factors. Degree 2
    # gives a piece-wise quadratic interpolation that looks nicer but overfits
    # for small smoothing amounts.
    spline = scipy.interpolate.LSQUnivariateSpline(xs, ys, knots, k=2)
    smooth_xs = np.linspace(xs[1], xs[-2], 10 * len(xs))
    smooth_ys = spline(smooth_xs)
    smooth_ys = np.clip(smooth_ys, ys.min(), ys.max())
    return smooth_xs, smooth_ys
