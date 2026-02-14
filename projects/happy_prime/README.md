# Happy Prime (Lab)

## Problem
Determine whether an integer is a happy number and whether it is prime.

## Data Sources
- User-provided integers

## Pipeline
1. Iterate sum-of-squares-of-digits until convergence or a loop is detected.
2. Run a primality check on the input.
3. Display the result in the Streamlit UI.

## Key Tradeoffs
- Optimized for interactive use on small to medium integers.

## How To Run
- Streamlit page: `poetry run streamlit run pages/6_happy_prime.py`
