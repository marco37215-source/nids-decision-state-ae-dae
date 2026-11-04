# Notebooks

| Path | What it is |
|---|---|
| `reproduce_manuscript_colab.ipynb` | Reproduces every table, figure and reported value of the manuscript that derives from the deposited final-test predictions. It clones this repository, downloads the Zenodo record and runs `scripts/reproduce_all.py`. A CPU runtime is sufficient. |
| `cicids2017/` | The original Experiment 1 v2 notebooks for CICIDS2017. |
| `unsw_nb15/` | The original Experiment 1 v2 notebooks for UNSW-NB15. |

## Original Experiment 1 v2 notebooks

These notebooks trained, selected and evaluated the models whose final-test predictions are deposited on Zenodo. They ran in Google Colab against the raw corpora and the intermediate files they wrote to the author's Google Drive. Those inputs and intermediate files are not part of this repository, so the notebooks are included as the code of record and are not expected to run from here as they stand. The manuscript's results are reproduced from the deposited predictions with `reproduce_manuscript_colab.ipynb` or `scripts/reproduce_all.py`.

### Stages

| Stage | CICIDS2017 (`cicids2017/`) | UNSW-NB15 (`unsw_nb15/`) |
|---|---|---|
| PRE-00: ingestion, stable `row_id`, raw model view, feature fingerprints, duplicate audit | `PRE_00_CICIDS2017_Governance_Audit_ModelView_FIXED_UPSTREAM_GATES.ipynb` | Not included in this repository |
| PRE-01: fingerprint-group partitioning and leakage control | `PRE_01_CICIDS2017_Partitioning_Leakage_Control_FIXED_VERIFIED_DISCOVERY.ipynb` | `PRE_01_UNSW_NB15_Source_Multiplicity_Stratified_Partitioning_V3_4_SINGLETON_TOLERANCE_FIX (1).ipynb` |
| PRE-02: preprocessing fitted on benign training data only | `PRE_02_CICIDS2017_Preprocessing_Representation_FIXED_COMPLETE_CONFIG.ipynb` | `PRE_02_UNSW_NB15_Source_Multiplicity_Preprocessing_V3_5_DIRECT_PRE00_BINDING (1).ipynb` |
| Notebook 01: AE configuration search | `01_CICIDS2017_AE_Search.ipynb` | `01_UNSW_NB15_AE_Search_V3_SOURCE_MULTIPLICITY.ipynb` |
| Notebook 02: DAE configuration search | `02_CICIDS2017_DAE_Search.ipynb` | `02_UNSW_NB15_DAE_Search_V3_SOURCE_MULTIPLICITY.ipynb` |
| Notebook 03: multi-seed confirmation and model selection (seeds 101, 202, 303) | `03_CICIDS2017_Multiseed_Confirmation.ipynb` | `03_UNSW_NB15_Multiseed_Confirmation_V3_SOURCE_MULTIPLICITY.ipynb` |
| Notebook 04: matched denoising ablation | `04_CICIDS2017_Matched_Denoising_Ablation.ipynb` | `04_UNSW_NB15_Matched_Denoising_Ablation_V3_SOURCE_MULTIPLICITY.ipynb` |
| Notebook 05: threshold sensitivity (development partition) | `05_CICIDS2017_Threshold_Sensitivity.ipynb` | `05_UNSW_NB15_Threshold_Sensitivity_V3_SOURCE_MULTIPLICITY.ipynb` |
| Notebook 06: hyperparameter sensitivity | `06_CICIDS2017_Hyperparameter_Sensitivity.ipynb` | `06_UNSW_NB15_Hyperparameter_Sensitivity_V3_SOURCE_MULTIPLICITY.ipynb` |
| Notebook 07: final evaluation on the sealed final test (seeds 101–505) | `07_CICIDS2017_Final_Known_Attack_Evaluation.ipynb` | `07_UNSW_NB15_Final_Known_Attack_Evaluation_V3_SOURCE_MULTIPLICITY.ipynb` |
| Notebook 08: paired final statistics and attack-family diagnostics | `08_CICIDS2017_Final_Statistics_Family_Diagnostics.ipynb` | `08_UNSW_NB15_Final_Statistics_Family_Diagnostics_V3_SOURCE_MULTIPLICITY.ipynb` |

### UNSW-NB15 audit and diagnostic notebooks

| Notebook | Purpose |
|---|---|
| `00_UNSW_NB15_Superseded_Branch_Audit.ipynb` | Audit of the superseded partitioning branch |
| `00B_UNSW_NB15_V3_5_Benign_Quantile_Transfer_Smoke_Gate (1).ipynb` | Benign-only smoke gate run before the formal model search |
| `00C_UNSW_NB15_PRE02_Error_Decomposition_and_Numerical_Range_Diagnostic_FIXED_ADDITIVITY.ipynb` | Error decomposition and numerical-range diagnostic for PRE-02 |
| `00D_UNSW_NB15_Mixed_Label_Fingerprint_Benign_Shift_Diagnostic_CT7.ipynb` | Mixed-label fingerprint and benign-shift diagnostic |
| `00E_UNSW_NB15_Fingerprint_Multiplicity_Feasibility_Audit (1).ipynb` | Feasibility audit for the fingerprint-multiplicity allocation |

The history of the UNSW-NB15 partition amendment is described in Section 3.12 of the manuscript and in the companion manuscript cited there.

### Recorded environment

The run manifests of Notebooks 01–05, 07 and 08 record the same environment for both datasets: Python 3.13.15, PyTorch 2.11.0 with CUDA 12.8, NumPy 2.1.3, pandas 2.2.3, scikit-learn 1.6.1, SciPy 1.16.3, Optuna 4.9.0 and PyArrow 23.0.1, on Linux in Google Colab. The GPU stages ran on an NVIDIA A100 GPU.
