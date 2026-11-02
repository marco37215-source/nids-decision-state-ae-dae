# Raw data (not included)

The raw corpora are **not redistributed** in this repository. Obtain them from their providers, accept their terms of use, and cite them:

| Corpus | Official page | Citation |
|---|---|---|
| CICIDS2017 | https://www.unb.ca/cic/datasets/ids-2017.html (the *MachineLearningCSV* files) | Sharafaldin, Habibi Lashkari and Ghorbani (2018), ICISSP |
| UNSW-NB15 | https://research.unsw.edu.au/projects/unsw-nb15-dataset (the four `UNSW-NB15_1.csv` … `_4.csv` files) | Moustafa and Slay (2015), MilCIS |

Nothing in `scripts/` or `tests/` reads raw data. The raw files are needed only to re-run the Colab notebooks (Level 3 in `docs/REPRODUCIBILITY.md`).

Each dataset folder contains:

* `source_manifest.csv`: the source files that formed the merged master (names as they appear in the frozen `row_id` values), with columns for the row count and SHA-256 of each file. Those per-file values were not recorded in the evidence used to build this repository; fill them in from the PRE-00 ingestion log.
* `SHA256SUMS.txt`: the SHA-256 of the merged master dataset recorded by PRE-00 (`fingerprint_audit.json → master_dataset_sha256`), in `sha256sum` format.

Suggested local layout (git-ignored):

```
data/cicids2017/raw/*.pcap_ISCX.csv
data/unsw_nb15/raw/UNSW-NB15_[1-4].csv
```
