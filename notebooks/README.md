# Notebooks

* `reproduce_manuscript_colab.ipynb: This notebook reproduces every table, figure and number of the manuscript(When Model Choice Changes with the Seed: Decision-State Uncertainty and Break-Even Costs in Autoencoder Intrusion Detection) that derives from the deposited final-test predictions.
* `cicids2017/`, `unsw_nb15/`: the original Experiment 1 v2 notebooks, which are described below.

## Original Colab notebooks 

The notebooks that produced every artefact are kept in the author's Google Drive and uploaded in this repository using the names below, so that the repository holds the code of the record of the stages it cannot re-run itself.


| File (same name in `cicids2017/` and `unsw_nb15/`) | Stage | Main outputs in this repository |
|---|---|---|
| `PRE_00_Governance_ModelView.ipynb` | Ingestion, `row_id`, raw model view, fingerprints, duplicate audit | `artifacts/*/fingerprints/*`, `artifacts/cicids2017/provenance/*` |
| `PRE_01_Partitioning.ipynb` | Fingerprint-atomic allocation, integrity report; UNSW-NB15 source balancing and the v3 amendment / MILP | `artifacts/*/partition/**` |
| `PRE_02_Preprocessing.ipynb` | Fit on `benign_weight_train` and transform all roles; benign quantile-transfer smoke gate (UNSW-NB15) | `artifacts/cicids2017/preprocessing/*`; UNSW-NB15 smoke manifests and ladder |
| `NB_01_AE_Search.ipynb`, `NB_02_DAE_Search.ipynb` | 20-configuration Optuna searches (seed 101) | top-three candidates |
| `NB_03_MultiSeed_Confirmation.ipynb` | Seeds 101/202/303, ranking, selection | `artifacts/*/model_selection/*`, development prediction archives |
| `NB_04_Matched_Ablation.ipynb` | Selected DAE with corruption disabled | not in the evidence set |
| `NB_05_Threshold_Sensitivity.ipynb`, `NB_06_Hyperparameter_Sensitivity.ipynb` | Sensitivity analyses | not in the evidence set |
| `NB_07_Final_Evaluation.ipynb` | Five final seeds on the sealed `final_test` | `artifacts/*/final_evaluation/final_seed_results.csv`, final prediction archives |
| `NB_08_Statistical_Analysis.ipynb` | Paired contrasts, bootstrap, tests | `artifacts/*/statistical_analysis/*` |

The UNSW-NB15 pre-formal diagnostics (00C block decomposition, 00D mixed-label diagnostic) live in a separate notebook.I have copied these notebooks to the unsw notebooks.


The library versions the notebooks ran with are in `requirements-notebooks.txt`.
