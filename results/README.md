# Outputs of the reference run

I produced every file in this folder by running `python scripts/reproduce_all.py --data-dir data/raw` with the pinned versions in `requirements.txt`. If you run the script again, these files are overwritten with your own outputs, which you can compare with the ones stored here.

In every file, differences are DAE minus AE, and the cost ratio is ρ = C_FP / C_FN.

## Tables (`tables/`)

| File | Contents | Manuscript |
| :-- | :-- | :-- |
| `input_integrity_checks.csv` | One row per run with the following: <br>• the population size and the class counts; <br>• whether the row identifiers and labels match the other runs of the dataset; <br>• the threshold T₉₉; <br>• whether the stored predictions follow ŷ = 1 if e > T₉₉; <br>• the smallest distance between an error and the threshold. | Sections 3.2, 3.5 |
| `seed_level_metrics.csv` | TP, FP, FN, TN, MCC, recall, F1, precision, PR-AUC, FPR, FP per 1,000 benign and balanced accuracy, for each dataset, model and seed. | Basis of Section 4 |
| `table_4_1_five_seed_performance.csv` | The five-seed mean and sample SD of MCC, recall, PR-AUC and FPR; the mean FP per 1,000 benign; and the mean TP, FP and FN. | Table 4.1 |
| `paired_seed_effects.csv` | For each metric: <br>• the mean, median and SD of the five paired differences; <br>• d_z; <br>• how many seeds favour each model; <br>• the bootstrap and paired *t* intervals; <br>• the paired *t* *p*-value. | Section 4.1 |
| `table_4_2_seed_decision_states.csv` | ΔTP, ΔFP, the decision state and ρ\* (exact fraction and decimal) for every seed. | Table 4.2 |
| `table_4_3_path_composition.csv` | The number and percentage of the 3,125 enumerated paths in each state. | Table 4.3 |
| `path_composition_by_seed_202.csv` | The same counts, split by whether a path contains seed 202. | Section 4.3 |
| `table_4_4_decision_map_unsw_nb15.csv` | For each open interval of ρ: the seeds favouring the DAE, the seeds favouring the AE, and the count favouring the DAE. | Table 4.4 |
| `prevalence_rescaling_illustration_unsw_nb15.csv` | Seed-specific and ratio-of-means thresholds, and their values under Equation 10 at π = 0.01. This is an arithmetic illustration, not an observed result. | Section 5.3 |
| `mcnemar_by_seed.csv` | Discordant counts, the net gain of the DAE and the exact two-sided *p*-value, per dataset and seed. | Section 4.5 |
| `score_diagnostics_by_run.csv` | For each run: <br>• the median and maximum of e / T₉₉ over missed attacks; <br>• the benign median error; <br>• the number and percentage of attacks below that median. | Section 4.6 |
| `table_4_5_score_diagnostics.csv` | The mean over seeds, with the range across seeds, of the two diagnostics. | Table 4.5 |

## Figures (`figures/`)

Each figure is saved as a vector PDF and as a 300 dpi PNG.

| File | Manuscript |
| :-- | :-- |
| `fig4_1_decision_state_plane` | Figure 4.1 |
| `fig4_2_path_composition` | Figure 4.2 |
| `fig4_3_cost_ratio_staircase` | Figure 4.3 |

## Other files

| File | Contents |
| :-- | :-- |
| `computed_values.json` | Every recomputed quantity under the name that `data/manuscript_reported_values.json` uses. |
| `manuscript_comparison.csv` | One row per value printed in the manuscript, showing where it is printed, the printed value, the reproduced value and whether they match. |
| `run_environment.json` | The Python and library versions of the run, and the MD5 checksum of each input file. |
