"""LISC plots - plots for words data."""

from lisc.plts.utils import check_ax, savefig
from lisc.plts.wordcloud import create_wordcloud, conv_freqs
from lisc.core.modutils import safe_import

plt = safe_import('.pyplot', 'matplotlib')

###################################################################################################
###################################################################################################

@savefig
def plot_wordcloud(freq_dist, n_words, ax=None):
    """Plot a wordcloud.

    Parameters
    ----------
    freq_dist : nltk.FreqDist
        Frequency distribution of words to plot.
    n_words : int
        Number of top words to include in the wordcloud.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    """

    cloud = create_wordcloud(conv_freqs(freq_dist, n_words))

    ax = check_ax(ax, (8, 8))
    ax.imshow(cloud)
    ax.axis("off")


@savefig
def plot_years(years, year_range=None, ax=None):
    """Plot publications across years histogram.

    Parameters
    ----------
    years : list of tuple of (int, int)
        Data on the number of publications per year.
    year_range : list of [int, int], optional
        The range of years to plot on the x-axis.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    """

    ax = check_ax(ax, (10, 5))

    # Extract x & y data to plot
    x_dat = [xd[0] for xd in years]
    y_dat = [yd[1] for yd in years]

    # Add line and points to plot
    plt.plot(x_dat, y_dat)
    plt.plot(x_dat, y_dat, '.', markersize=16)

    # Set plot limits
    if year_range:
        plt.xlim([year_range[0], year_range[1]])
    plt.ylim([0, max(y_dat)+5])

    # Add title & labels
    plt.title('Publication History', fontsize=24, fontweight='bold')
    plt.xlabel('Year', fontsize=18)
    plt.ylabel('# Pubs', fontsize=18)
