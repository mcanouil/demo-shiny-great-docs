"""Summary statistics for the Palmer Penguins dataset."""

from __future__ import annotations

import polars as pl


def summarise_by_species(df: pl.DataFrame) -> pl.DataFrame:
    """Summarise body mass and flipper length per species.

    Parameters
    ----------
    df
        A penguins DataFrame as returned by
        :func:`penguin_analysis.load_penguins`.

    Returns
    -------
    polars.DataFrame
        One row per species with the mean body mass (g), mean flipper
        length (mm) and the number of observations.

    Examples
    --------
    >>> from penguin_analysis import load_penguins, summarise_by_species
    >>> summarise_by_species(load_penguins()).shape[1]
    4
    """
    return (
        df.group_by("species")
        .agg(
            pl.col("body_mass_g").mean().round(1).alias("mean_body_mass_g"),
            pl.col("flipper_length_mm").mean().round(1).alias("mean_flipper_length_mm"),
            pl.len().alias("n"),
        )
        .sort("species")
    )


def species_counts(df: pl.DataFrame) -> pl.DataFrame:
    """Count observations per species and island.

    Parameters
    ----------
    df
        A penguins DataFrame as returned by
        :func:`penguin_analysis.load_penguins`.

    Returns
    -------
    polars.DataFrame
        Counts grouped by ``species`` and ``island``, sorted descending by
        count.

    Examples
    --------
    >>> from penguin_analysis import load_penguins, species_counts
    >>> "n" in species_counts(load_penguins()).columns
    True
    """
    return (
        df.group_by("species", "island")
        .agg(pl.len().alias("n"))
        .sort("n", descending=True)
    )


def mass_flipper_corr(df: pl.DataFrame) -> float:
    """Compute the Pearson correlation between body mass and flipper length.

    Parameters
    ----------
    df
        A penguins DataFrame as returned by
        :func:`penguin_analysis.load_penguins`.

    Returns
    -------
    float
        The Pearson correlation coefficient, rounded to three decimals.

    Examples
    --------
    >>> from penguin_analysis import load_penguins, mass_flipper_corr
    >>> 0.0 < mass_flipper_corr(load_penguins()) <= 1.0
    True
    """
    corr = df.select(
        pl.corr("body_mass_g", "flipper_length_mm")
    ).item()
    return round(float(corr), 3)
