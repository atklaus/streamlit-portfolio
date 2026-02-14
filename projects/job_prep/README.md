# Job Prep (Utility)

## Problem
Generate customized cover letters from a DOCX template by replacing placeholders.

## Data Sources
- `projects/job_prep/assets/Cover_Letter.docx`
- Manual inputs in `projects/job_prep/job_prep.py`

## Pipeline
1. Load the DOCX template.
2. Replace placeholder tokens with job-specific values.
3. Save a new DOCX and convert to PDF.

## Key Tradeoffs
- Requires local DOCX/PDF tooling (`docx2pdf`) that depends on platform support.
- Input values are edited in code rather than a UI.

## How To Run
1. Edit variables near the top of `projects/job_prep/job_prep.py`.
2. Run: `python projects/job_prep/job_prep.py`
