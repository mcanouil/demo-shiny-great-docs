# demo-shiny-great-docs

A minimal demo showing how to serve [great-docs](https://posit-dev.github.io/great-docs/) compiled documentation alongside a [Shiny for Python](https://shiny.posit.co/py/) app from a single process.

The Palmer Penguins analysis here is only the subject being documented.
The point of the repository is the integration: a Python module documented with great-docs, and a Shiny app that serves both its interface and that documentation under one server.

## How the integration works

great-docs renders a static HTML site (`great-docs/_site/`) which is copied to `docs/`.
Shiny serves static files literally and returns 404 for directory URLs such as `/docs/reference/`, while great-docs emits clean directory links.
To bridge that, the Shiny app is wrapped in a Starlette app that mounts the docs with `StaticFiles(..., html=True)` so directory URLs resolve to `index.html`:

```python
app = Starlette(
    routes=[
        Mount("/docs", app=StaticFiles(directory=DOCS_DIR, html=True)),
        Mount("/", app=shiny_app),
    ]
)
```

`shiny run app.py` still works because uvicorn accepts any ASGI app.
The app links to the documentation from its navbar, so both are reachable from the same origin.

## Project structure

```text
src/penguin_analysis/   # the module being documented (data, analysis, viz)
app.py                  # Shiny app + Starlette wrapper mounting docs at /docs
great-docs.yml          # great-docs configuration
scripts/build-docs.sh   # great-docs build, then copy _site -> docs/
docs/                   # generated site (gitignored, built before running)
```

## Quick start

```bash
uv sync --extra app --extra dev
bash scripts/build-docs.sh
uv run shiny run app.py --port 8000
```

Then open <http://localhost:8000> for the app and <http://localhost:8000/docs/> for the documentation.

The package must be installed (`uv sync`) before building, because great-docs introspects it to discover the public API.
`docs/` is generated output and is gitignored, so rebuild it with `scripts/build-docs.sh` whenever the module changes.

## The documented module

`penguin_analysis` loads the dataset with polars, computes summaries, and draws plotnine plots:

- `load_penguins()` loads the dataset as a polars DataFrame.
- `summarise_by_species()` returns mean body mass and flipper length per species.
- `species_counts()` counts observations per species and island.
- `mass_flipper_corr()` computes the body mass vs flipper length correlation.
- `mass_vs_flipper()` and `body_mass_distribution()` return plotnine plots.
