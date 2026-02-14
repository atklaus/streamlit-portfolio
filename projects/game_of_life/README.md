# Game of Life (Lab)

## Problem
Visualize Conway's Game of Life and explore common starting patterns.

## Data Sources
- Synthetic grid initialization and preset seeds

## Pipeline
1. Initialize a board based on user-selected size and probability.
2. Apply Game of Life rules iteratively.
3. Render frames as a Plotly heatmap animation.

## Key Tradeoffs
- Focuses on visualization, not performance for very large grids.

## How To Run
- Streamlit page: `poetry run streamlit run pages/4_game_of_life.py`
