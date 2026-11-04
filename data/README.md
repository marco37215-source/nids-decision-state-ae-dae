# Data

This folder holds the metadata that the reproduction code needs. The prediction files themselves are not stored in the repository.

## Contents

| File | Purpose |
|---|---|
| `input_manifest.csv` | One row for each of the 20 deposited Parquet files: dataset, model, seed, number of rows, configuration hash, run hash, size in bytes, MD5 and SHA-256. The code uses these checksums to identify and authenticate every input file. |
| `manuscript_reported_values.json` | The 243 values printed in the manuscript that derive from the deposited predictions, each with its location in the manuscript and its printed precision. `scripts/reproduce_all.py` recomputes each value and checks it against this list. |
| `raw/` (not tracked) | Put the 20 Parquet files downloaded from Zenodo here. Git ignores this folder. |

## Downloading the prediction files

The 20 final-test prediction files (2 datasets × 2 models × 5 seeds) are deposited on Zenodo under a Creative Commons Attribution 4.0 International licence: doi:[10.5281/zenodo.23559367](https://doi.org/10.5281/zenodo.23559367).

```bash
pip install zenodo_get
zenodo_get 10.5281/zenodo.23559367 -o data/raw
```

The code identifies each file by its checksum, not by its name, so the file names may be anything. Extra files in the folder are ignored.

## Raw benchmark corpora

The raw CICIDS2017 and UNSW-NB15 corpora are not redistributed here, and nothing in `scripts/` or `src/` reads them. They are needed only to re-run the original Experiment 1 v2 notebooks in `notebooks/cicids2017/` and `notebooks/unsw_nb15/`. Obtain them from their providers, accept their terms of use, and cite them:

| Corpus | Official page | Citation |
|---|---|---|
| CICIDS2017 | https://www.unb.ca/cic/datasets/ids-2017.html (the *MachineLearningCSV* files) | Sharafaldin, Habibi Lashkari and Ghorbani (2018), ICISSP |
| UNSW-NB15 | https://research.unsw.edu.au/projects/unsw-nb15-dataset (the four `UNSW-NB15_1.csv` to `UNSW-NB15_4.csv` files) | Moustafa and Slay (2015), MilCIS |
