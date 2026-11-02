# External artefacts: final-test prediction archives

This directory documents the observation-level prediction archives associated with the manuscript.

## Scope

The external deposit contains **20 final-test prediction archives only**:

- **10 CICIDS2017 final-test prediction files**: AE and DAE across seeds 101, 202, 303, 404, and 505.
- **10 UNSW-NB15 final-test prediction files**: AE and DAE across seeds 101, 202, 303, 404, and 505.


## External deposit

The 20 prediction archives are too large for normal GitHub storage and will therefore be deposited separately.

- **Repository:** GitHub contains the manuscript code record, notebooks, compact artefacts, tables, figures, and documentation.
- **Large prediction archives:** Deposited on Zenodo.
- **Zenodo DOI:** **https://doi.org/10.5281/zenodo.23559367**.


## Archive coverage

| Corpus | Role | Runs | Rows per file |
|---|---|---:|---:|
| CICIDS2017 | final_test | 10 (AE and DAE × 5 seeds) | 668,562 |
| UNSW-NB15 | final_test | 10 (AE and DAE × 5 seeds) | 525,584 |

The five final-evaluation seeds are:

`101, 202, 303, 404, 505`

## Prediction-file schema

Each final-test prediction file contains the following fields:

- `row_id`
- `y_true`
- `reconstruction_error`
- `threshold`
- `y_pred`
- `model`
- `seed`
- `config_hash`
- `run_hash`
- `attack_family`
- `feature_fingerprint`

For each file, the stored binary prediction follows the experiment rule:

`y_pred = 1` when `reconstruction_error > threshold`.

Each file contains one threshold corresponding to the relevant model × seed evaluation run.

## Integrity verification

The authoritative integrity information for the external files is recorded in `prediction_archive_manifest.csv`.

After downloading the archives, verify that:

1. the filename matches the manifest;
2. the file size matches the manifest;
3. the SHA-256 checksum matches the manifest;
4. the row count matches the expected corpus-specific final-test size;
5. the model, seed, `config_hash`, and `run_hash` agree with the manifest.

No separate development prediction set is required by this repository.

## Data content and privacy

The prediction archives do **not** contain raw packet payloads, raw feature values, or IP addresses.

They contain observation identifiers, labels, attack-family labels, reconstruction errors, thresholds, predictions, model/run provenance, and hashed model-view fingerprints.


