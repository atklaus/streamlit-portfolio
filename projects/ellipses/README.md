# Random Ellipses (Lab)

## Problem
Estimate the overlapping area between two ellipses using a Monte Carlo simulation.

## Data Sources
- User-provided ellipse parameters
- Pseudo-random generator seeded with text from `war-and-peace.txt`

## Pipeline
1. Parse user inputs for two ellipses.
2. Generate random points and classify each point location.
3. Estimate overlap area from point density and visualize results.

## Key Tradeoffs
- Accuracy depends on the number of iterations.
- The RNG is deterministic for repeatability, not cryptographic quality.

## How To Run
- Streamlit page: `poetry run streamlit run pages/5_ellipses.py`
