"""Plotnine visualisations for the Palmer Penguins dataset."""

from __future__ import annotations

import plotnine as p9
import polars as pl


def mass_vs_flipper(df: pl.DataFrame) -> p9.ggplot:
    """Scatter plot of body mass against flipper length, coloured by species.

    Parameters
    ----------
    df
        A penguins DataFrame as returned by
        :func:`penguin_analysis.load_penguins`.

    Returns
    -------
    plotnine.ggplot
        A scatter plot ready to be drawn or rendered in a Shiny output.

    Examples
    --------
    >>> from penguin_analysis import load_penguins, mass_vs_flipper
    >>> isinstance(mass_vs_flipper(load_penguins()), object)
    True
    """
    return (
        p9.ggplot(df.to_pandas())
        + p9.aes(x="flipper_length_mm", y="body_mass_g", colour="species")
        + p9.geom_point(alpha=0.8)
        + p9.labs(
            x="Flipper length (mm)",
            y="Body mass (g)",
            colour="Species",
            title="Body mass vs flipper length",
        )
        + p9.theme_minimal()
    )


def body_mass_distribution(df: pl.DataFrame) -> p9.ggplot:
    """Density plot of body mass per species.

    Parameters
    ----------
    df
        A penguins DataFrame as returned by
        :func:`penguin_analysis.load_penguins`.

    Returns
    -------
    plotnine.ggplot
        A density plot ready to be drawn or rendered in a Shiny output.

    Examples
    --------
    >>> from penguin_analysis import load_penguins, body_mass_distribution
    >>> isinstance(body_mass_distribution(load_penguins()), object)
    True
    """
    return (
        p9.ggplot(df.to_pandas())
        + p9.aes(x="body_mass_g", fill="species")
        + p9.geom_density(alpha=0.5)
        + p9.labs(
            x="Body mass (g)",
            y="Density",
            fill="Species",
            title="Body mass distribution by species",
        )
        + p9.theme_minimal()
    )
