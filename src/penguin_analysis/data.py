"""Data loading utilities for the Palmer Penguins dataset."""

from __future__ import annotations

import palmerpenguins
import polars as pl


def load_penguins(*, drop_nulls: bool = True) -> pl.DataFrame:
    """Load the Palmer Penguins dataset as a polars DataFrame.

    Wraps :func:`palmerpenguins.load_penguins`, which returns a pandas
    DataFrame, and converts the result to polars.

    Parameters
    ----------
    drop_nulls
        If ``True`` (default), rows containing any missing value are removed
        so downstream summaries and plots have complete cases.

    Returns
    -------
    polars.DataFrame
        The penguins dataset with columns ``species``, ``island``,
        ``bill_length_mm``, ``bill_depth_mm``, ``flipper_length_mm``,
        ``body_mass_g``, ``sex`` and ``year``.

    Examples
    --------
    >>> from penguin_analysis import load_penguins
    >>> df = load_penguins()
    >>> df.columns[:2]
    ['species', 'island']
    """
    df = pl.from_pandas(palmerpenguins.load_penguins())
    if drop_nulls:
        df = df.drop_nulls()
    return df
