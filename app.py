"""Shiny app exploring the Palmer Penguins dataset.

The app imports the :mod:`penguin_analysis` module for all analysis and serves
its great-docs documentation at ``/docs`` from the same process.
"""

from __future__ import annotations

from pathlib import Path

import polars as pl
from shiny import App, reactive, render, ui
from shiny.ui import Theme
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

import penguin_analysis as pa

_DATA = pa.load_penguins()
_SPECIES = sorted(_DATA["species"].unique().to_list())
_DOCS_DIR = Path(__file__).parent / "docs"

_LOGO_SVG = ui.HTML(
    '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28"'
    ' style="vertical-align:middle;margin-right:8px" aria-hidden="true">'
    '<rect x="0" y="0" width="28" height="28" rx="6" fill="rgba(255,255,255,0.15)"/>'
    '<circle cx="8" cy="20" r="2.5" fill="white"/>'
    '<circle cx="14" cy="12" r="2.5" fill="white"/>'
    '<circle cx="20" cy="16" r="2.5" fill="#fbbf24"/>'
    '</svg>'
)

_THEME = (
    Theme("shiny")
    .add_rules("""
    $primary: #0f766e;
    $secondary: #d97706;
    $light: #f0fdfa;
    """)
    .add_rules("""
    .navbar {
      background-color: #0f766e !important;
    }
    .navbar-brand,
    .navbar-brand span,
    .navbar .nav-link {
      color: rgba(255, 255, 255, 0.85) !important;
    }
    .navbar-brand:hover,
    .navbar .nav-link:hover,
    .navbar .nav-link.active {
      color: #ffffff !important;
    }
    .navbar .nav-link.active {
      border-bottom-color: #fbbf24 !important;
    }
    .bslib-sidebar-layout > .sidebar {
      background-color: #f0fdfa !important;
      border-right: 1px solid #99f6e4 !important;
    }
    """
    )
)

app_ui = ui.page_navbar(
    ui.nav_panel(
        "Explore",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_selectize(
                    "species",
                    "Species",
                    choices=_SPECIES,
                    selected=_SPECIES,
                    multiple=True,
                ),
            ),
            ui.output_text("correlation"),
            ui.output_data_frame("table"),
        ),
    ),
    ui.nav_panel(
        "Plots",
        ui.output_plot("scatter"),
        ui.output_plot("distribution"),
    ),
    ui.nav_panel(
        "Summary",
        ui.output_data_frame("summary"),
    ),
    ui.nav_spacer(),
    ui.nav_control(
        ui.a("Documentation", href="/docs/", target="_blank"),
    ),
    title=ui.tags.span(_LOGO_SVG, "Palmer Penguins"),
    theme=_THEME,
    id="navbar",
)


def server(input, output, session):
    @reactive.calc
    def filtered() -> pl.DataFrame:
        selected = input.species()
        if not selected:
            return _DATA.clear()
        return _DATA.filter(pl.col("species").is_in(selected))

    @render.text
    def correlation() -> str:
        df = filtered()
        if df.height < 2:
            return "Select at least one species to compute a correlation."
        corr = pa.mass_flipper_corr(df)
        return f"Body mass vs flipper length correlation: {corr}"

    @render.data_frame
    def table():
        return render.DataGrid(filtered().to_pandas(), height="400px")

    @render.data_frame
    def summary():
        return render.DataGrid(pa.summarise_by_species(_DATA).to_pandas())

    @render.plot
    def scatter():
        return pa.mass_vs_flipper(filtered()).draw()

    @render.plot
    def distribution():
        return pa.body_mass_distribution(filtered()).draw()


shiny_app = App(app_ui, server)

# Wrap the Shiny app so the great-docs site is served at /docs with html=True,
# which resolves directory URLs (e.g. /docs/reference/) to index.html. Shiny's
# own static_assets mount serves files literally and 404s on such URLs.
app = Starlette(
    routes=[
        Mount("/docs", app=StaticFiles(directory=_DOCS_DIR, html=True), name="docs"),
        Mount("/", app=shiny_app, name="shiny"),
    ]
)
