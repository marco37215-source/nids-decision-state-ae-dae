# Decision-state uncertainty in autoencoder intrusion detection: reproducibility code

This repository reproduces the results, tables and figures of the manuscript

> J. M. Kamara, D. M. Kaburu and M. W. Kimwele, "When Model Choice Changes with the Seed: Decision-State Uncertainty and Break-Even Costs in Autoencoder Intrusion Detection", manuscript prepared for submission to *Journal of Communications and Networks*.

The manuscript is a secondary decision-analytic analysis. It uses the frozen final-test predictions of a selected autoencoder (AE) and a selected denoising autoencoder (DAE) from Experiment 1 v2 of my MSc research, on CICIDS2017 and UNSW-NB15, under five paired seeds (101, 202, 303, 404, 505). I deposited those predictions on Zenodo. This repository starts from that deposit and recomputes everything the manuscript reports about them.

**The guiding rule of this repository is that it contains nothing that cannot be reproduced from the deposited data.** Every table and figure in `results/` was produced by the code here. The run ends by comparing 233 numbers printed in the manuscript with the numbers it has just recomputed, and it fails if any of them differs.

---

## Contents

1. [What this repository reproduces](#1-what-this-repository-reproduces)
2. [What it does not reproduce, and why](#2-what-it-does-not-reproduce-and-why)
3. [Data](#3-data)
4. [How to reproduce the results](#4-how-to-reproduce-the-results)
5. [How the analysis works](#5-how-the-analysis-works)
6. [Verification and determinism](#6-verification-and-determinism)
7. [Repository structure](#7-repository-structure)
8. [Citation, licence and contact](#8-citation-licence-and-contact)

---

## 1. What this repository reproduces

| Manuscript item | Output file in `results/` | Code |
| :-- | :-- | :-- |
| Final-test populations and attack prevalence (Sections 3.2, 3.5, 4.4) | `tables/input_integrity_checks.csv` | `inputs.integrity_report` |
| Seed-level confusion counts and metrics (basis of Section 4.1) | `tables/seed_level_metrics.csv` | `metrics.seed_level_metrics` |
| Table 4.1: five-seed performance and mean counts | `tables/table_4_1_five_seed_performance.csv` | `metrics.table_4_1` |
| Section 4.1: paired differences, d_z, bootstrap and paired *t* intervals | `tables/paired_seed_effects.csv` | `paired_stats.paired_summary` |
| Table 4.2: seed-level ΔTP, ΔFP, decision states and ρ\* | `tables/table_4_2_seed_decision_states.csv` | `decision.table_4_2` |
| Table 4.3 and Section 4.3: the 3,125 enumerated paths | `tables/table_4_3_path_composition.csv`, `tables/path_composition_by_seed_202.csv` | `decision.table_4_3` |
| Section 4.4: break-even thresholds, ratio of means, fold range | `computed_values.json` | `decision.ratio_of_means` |
| Table 4.4: observed-seed decision map over ρ | `tables/table_4_4_decision_map_unsw_nb15.csv` | `decision.table_4_4` |
| Section 4.5: exact McNemar tests | `tables/mcnemar_by_seed.csv` | `diagnostics.mcnemar_by_seed` |
| Table 4.5 and Section 4.6: reconstruction-score diagnostics | `tables/table_4_5_score_diagnostics.csv`, `tables/score_diagnostics_by_run.csv` | `diagnostics` |
| Section 5.2: false-positive changes in percentage points of FPR | `computed_values.json` | `scripts/reproduce_all.py` |
| Section 5.3: prevalence-rescaling illustration at π = 0.01 | `tables/prevalence_rescaling_illustration_unsw_nb15.csv` | `decision.prevalence_rescaled` |
| Figure 4.1: decision-state plane | `figures/fig4_1_decision_state_plane.{pdf,png}` | `figures.figure_4_1` |
| Figure 4.2: path composition | `figures/fig4_2_path_composition.{pdf,png}` | `figures.figure_4_2` |
| Figure 4.3: cost-ratio staircase | `figures/fig4_3_cost_ratio_staircase.{pdf,png}` | `figures.figure_4_3` |
| Every number above, checked against the manuscript | `manuscript_comparison.csv` | `check.compare_with_manuscript` |

The same quantities appear again in the Abstract, Section 5 and Section 6, and are covered by the same check.

## 2. What it does not reproduce, and why

The deposit contains the final-test predictions only. I therefore left out every part of the manuscript that rests on artefacts that are not in the deposit. I did not copy those numbers into this repository, because you could not reproduce them from it. They are:

- **Model training, search, selection and evaluation.** This covers Notebooks 01–07 of Experiment 1 v2, which ran on Google Colab with an NVIDIA A100 GPU, and the settings in Table 3.1 that came out of them. Trained weights and training data are not part of the deposit.
- **Training-horizon records** used in Section 5.8.4: the best epochs and search-level epoch counts.
- **Development-partition results** used in Sections 5.8.1 and 5.8.6: the confirmation-seed decision states and the Notebook 05 threshold-sensitivity states.
- **Partition construction and leakage control.** These are reported in the companion manuscript and its own repository.
- **The computational environment of the training runs** (Section 3.12).

The decision analysis does not depend on any of these. It starts from the frozen predictions, and every quantity it reports is reproduced here.

## 3. Data

| Item | Value |
| :-- | :-- |
| Source | Zenodo, doi:[10.5281/zenodo.23559367](https://doi.org/10.5281/zenodo.23559367) |
| Licence | Creative Commons Attribution 4.0 International |
| Files used | 20 Parquet files: 2 datasets × 2 models × 5 seeds |
| Rows | 668,562 per CICIDS2017 file; 525,584 per UNSW-NB15 file |
| Checksums | `data/input_manifest.csv` (MD5 and SHA-256 of every file) |

Each file holds one model under one seed on the full final test of one dataset. The code reads these columns: `row_id`, `y_true`, `reconstruction_error`, `threshold`, `y_pred`, `model`, `seed`, `config_hash`, `run_hash` and `attack_family`.

I do not redistribute the data in this repository. Download them from Zenodo into `data/raw/`, as described in Section 4. The code identifies each file by its checksum, not by its name, so you may keep whatever file names the download gives you. Any extra files in the folder are ignored.

## 4. How to reproduce the results

### Option A: Google Colab (no installation)

1. Open `notebooks/reproduce_manuscript2_colab.ipynb` in Google Colab.
2. Set `REPO_URL` in the first code cell to the address of this repository.
3. Run all cells. The notebook downloads the Zenodo record, runs the full reproduction and shows the tables, the figures and the manuscript check.

A CPU runtime is sufficient.

### Option B: your own computer

You need Python 3.11 or later; I tested the code with Python 3.13. You also need about 3 GB of free memory (the reference run peaked at 2.4 GB) and 0.4 GB of disk space for the data.

```bash
git clone https://github.com/marco37215-source/nids-decision-state-ae-dae.git && cd nids-decision-state-ae-dae
python -m venv .venv && source .venv/bin/activate      # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Download the 20 Parquet files from the Zenodo record into `data/raw/`. Either download them by hand from the record page, or run:

```bash
pip install zenodo_get
zenodo_get 10.5281/zenodo.23559367 -o data/raw
```

Then run the reproduction:

```bash
python scripts/reproduce_all.py --data-dir data/raw
```

The run takes about 30 seconds on a two-core machine and should end with:

```
233 of 233 manuscript values reproduced.
All values printed in the manuscript that derive from the deposited predictions were reproduced.
```

The outputs are written to `results/`, overwriting the copies stored in the repository. To keep the stored copies, pass another folder with `--out-dir`.

## 5. How the analysis works

I describe each step in the order in which `scripts/reproduce_all.py` runs it. Section numbers refer to the manuscript.

**Authentication of the inputs.** I match every Parquet file to `data/input_manifest.csv` by its MD5 checksum, and confirm the match with SHA-256. I then check, inside each file, that the model, seed, configuration hash and run hash are the expected ones and that the file carries a single threshold. The run stops if any of the 20 files is missing or does not match.

**The paired design.** Within each dataset, I check that all ten runs contain the same final-test observations with the same labels. I also check that the stored prediction equals the frozen rule ŷ = 1 if e > T₉₉, and 0 otherwise, on every observation (Equation 3). The smallest distance between an error and its threshold is reported per run in `input_integrity_checks.csv`; it is at least 2.4 × 10⁻⁷, so no prediction is sensitive to floating-point rounding.

**Seed-level metrics (Section 3.4).** I recompute TP, FP, FN and TN from the stored labels and predictions, then compute from them:
- MCC, recall, precision, F1;
- FPR, false positives per 1,000 benign observations;
- balanced accuracy.

PR-AUC is the trapezoidal area under the precision–recall curve, `sklearn.metrics.auc(recall, precision)` on the points of `precision_recall_curve`. This is the definition used in Experiment 1, and it is not the same quantity as average precision.

**Paired statistics (Section 3.11).** The inferential unit is the paired final seed, so n = 5. For each metric I compute:
- the five differences DAE − AE, with their mean, median and sample standard deviation;
- d_z = mean / SD;
- the direction consistency;
- a percentile bootstrap interval;
- the paired *t* interval and *p*-value.

The bootstrap follows Notebook 08 exactly:
- 10,000 resamples;
- one `numpy.random.default_rng(2026)` stream per dataset, shared by the metrics in a fixed order (MCC, recall, F1, precision, PR-AUC, FPR, FP per 1,000 benign, balanced accuracy);
- `numpy.percentile` at 2.5 and 97.5.

Because the stream is shared, a metric's interval depends on its position in the order. For that reason I also compute F1, precision and balanced accuracy, although the manuscript does not report them.

**Decision states (Section 3.6).** For each seed I classify (ΔTP, ΔFP) as:
- State I (DAE dominance);
- State II (genuine trade-off);
- State III (AE dominance);
- State IV (inverse trade-off);
- or an exact tie.

The boundaries are at exactly zero, and no materiality tolerance is applied.

**Break-even thresholds (Section 3.7).** For State II seeds only, ρ\* = ΔTP/ΔFP on the cost ratio ρ = C_FP/C_FN. I keep the exact count ratios as fractions and round them only in the tables. The aggregate point estimate is the ratio of the mean differences (Equation 9).

**Path enumeration (Section 3.8).** I list all 5⁵ = 3,125 ordered five-seed paths drawn with replacement from the observed seeds, sum the seed-level differences along each path and classify the sums. The paths are deterministic recombinations of five observed realisations. They are not new experiments, and I compute no interval or *p*-value from them.

**Decision map (Section 3.9).** The finite thresholds divide the positive ρ-axis into open intervals. I evaluate each seed's preferred model at an interior point of each interval, never at a boundary, and count the seeds that favour the DAE (Table 4.4, Figure 4.3).

**McNemar tests (Section 3.11).** For each dataset and seed I pair the AE and DAE predictions observation by observation. I then apply an exact two-sided binomial test to the discordant observations. The net discordance equals ΔTP − ΔFP, so these tests speak only to the equal-cost case ρ = 1.

**Score diagnostics (Section 3.10).** For each run separately I compute two summaries, using that run's own T₉₉ and its own benign median:
- the median of e / T₉₉ over missed attacks;
- the percentage of attacks whose error is below the median benign error.

Table 4.5 reports the mean over seeds and the range across seeds.

**Figures.** The three figures are drawn only from the reproduced tables.

## 6. Verification and determinism

**Check against the manuscript.** `data/manuscript_reported_values.json` lists 233 values exactly as the manuscript prints them, with their location and printed precision. I transcribed them from the manuscript. A value matches when the recomputed number, rounded to the printed precision, equals the printed number. Where the manuscript states a bound (for example *p* < 10⁻⁴¹), the bound is checked instead. The comparison is written to `results/manuscript_comparison.csv`.

**A correction found by this check.** The first run found one value that did not match: the upper limit of the paired *t* interval for the CICIDS2017 false-positive difference. The draft printed +0.468 FP per 1,000; the recomputed value is +0.4675, which rounds to +0.467. I corrected the manuscript to +0.467. The entry in `manuscript_reported_values.json` records this correction.

**Determinism.** The only random step is the bootstrap, which uses a fixed seed. With the pinned versions in `requirements.txt`, two consecutive runs produced byte-identical tables, figures and comparison files. `run_environment.json` records the versions and input checksums of each run.

I also ran the code with newer libraries: NumPy 2.5.3, pandas 3.0.5, SciPy 1.18.1, scikit-learn 1.9.1, PyArrow 26.0.0 and Matplotlib 3.11.2. The recomputed values then differed from the stored outputs by at most 2 × 10⁻¹³ in relative terms, and all 233 manuscript values were still reproduced.

## 7. Repository structure

```
.
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── data/
│   ├── input_manifest.csv               # checksums of the 20 deposited Parquet files
│   ├── manuscript_reported_values.json  # values printed in the manuscript, for the final check
│   └── raw/                             # place the downloaded Parquet files here (not tracked)
├── notebooks/
│   └── reproduce_manuscript2_colab.ipynb
|   └── colab notebooks of Experiment 1 v2 # produce every artefact in this manuscript
├── external_artifacts  # Contains README files with Zenodo links to the 20 externally archived final-test prediction Parquet files.
├── scripts/
│   └── reproduce_all.py                 # runs the whole analysis and the check
├── src/decision_state/
│   ├── constants.py                     # seeds, configuration hashes, bootstrap settings
│   ├── inputs.py                        # authentication, loading and integrity checks
│   ├── metrics.py                       # counts, metrics, Table 4.1
│   ├── paired_stats.py                  # paired differences, bootstrap, t intervals
│   ├── decision.py                      # states, thresholds, enumeration, decision map
│   ├── diagnostics.py                   # McNemar tests, score diagnostics
│   ├── figures.py                       # Figures 4.1-4.3
│   └── check.py                         # comparison with the manuscript
└── results/                             # outputs of the reference run
    ├── tables/  figures/
    ├── computed_values.json  manuscript_comparison.csv  run_environment.json
```

`results/README.md` describes every output file.

## 8. Citation, licence and contact

If you use this code, please cite the manuscript and the data deposit. The data deposit is:

> J. M. Kamara, M. Kimwele and D. M. Kaburu, "Observation-level final-test predictions of autoencoder and denoising-autoencoder intrusion detectors on CICIDS2017 and UNSW-NB15 (Experiment 1 v2, known attacks)", Zenodo, 2026, doi:10.5281/zenodo.23559367.

`CITATION.cff` gives the citation in machine-readable form.

The code is released under the licence in `LICENSE`. The data remain under their own Creative Commons Attribution 4.0 International licence on Zenodo.

The datasets behind the predictions are CICIDS2017 (Canadian Institute for Cybersecurity) and UNSW-NB15 (UNSW Canberra). Please cite and respect their original terms of use if you work with the underlying traffic records.

**Contact:** Joseph Marco Kamara, Department of Mathematical Sciences, Pan African University Institute for Basic Sciences, Technology and Innovation (PAUSTI), Nairobi, Kenya, jkamara@pau-au.africa, ORCID [0009-0009-2455-1222](https://orcid.org/0009-0009-2455-1222).
