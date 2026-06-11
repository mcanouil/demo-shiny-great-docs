"""Analyse the Palmer Penguins dataset.

A small dummy package that loads the Palmer Penguins dataset, computes a few
summary statistics and produces plotnine visualisations. It exists to
demonstrate documenting a Python module with great-docs and serving that
documentation from a Shiny app.
"""

from __future__ import annotations

from penguin_analysis.analysis import (
    mass_flipper_corr,
    species_counts,
    summarise_by_species,
)
from penguin_analysis.data import load_penguins
from penguin_analysis.viz import body_mass_distribution, mass_vs_flipper

__all__ = [
    "load_penguins",
    "summarise_by_species",
    "species_counts",
    "mass_flipper_corr",
    "mass_vs_flipper",
    "body_mass_distribution",
]
