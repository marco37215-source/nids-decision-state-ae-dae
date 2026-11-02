# UNSW-NB15 Experiment 1 v2 — Corrected Source-Stratified Restart

## Scientific restart boundary

Retain the authoritative merged UNSW-NB15 master and PRE-00. The original PRE-01, PRE-02, Notebook 01 AE search, and partial Notebook 02 DAE search are superseded for scientific inference because the original fingerprint-atomic allocator produced severe source-capture imbalance across benign roles.

The corrected branch is isolated under model branch version:

`v2_source_stratified_20260918`

No old PRE-01/PRE-02/model result is reused in the corrected scientific branch.

## Execution order

0. **Optional audit only:** `00_UNSW_NB15_Superseded_Branch_Audit.ipynb`
   - Non-destructive.
   - Writes an incident/supersession manifest.
   - Does not move or delete old files.

1. **Corrected PRE-01:** `PRE_01_UNSW_NB15_Source_Stratified_Partitioning_CORRECTED.ipynb`
   - Reuses PRE-00 row identities and fingerprints.
   - Keeps fingerprint groups indivisible.
   - Adds source-capture composition vectors and source-stratified benign targets.
   - Balances all five benign roles against the global benign source-file composition.
   - Retains family-aware attack allocation and strict benign-majority constraints.
   - Writes `source_composition_audit.csv`, `source_balance_summary.csv`, and the source-stratification amendment record.
   - **STOP if the source-balance gate is not PASS.**

2. **Corrected PRE-02:** `PRE_02_UNSW_NB15_Source_Stratified_Preprocessing_CORRECTED.ipynb`
   - Explicitly binds to the corrected PRE-01 directory.
   - Refits numerical imputation/scaling and categorical vocabulary/rare/unknown/OHE using the new `benign_weight_train` only.
   - Retransforms all five roles.
   - Produces a new representation/upstream identity.
   - **STOP if PRE-02 does not PASS.**

3. **One-configuration benign-only smoke gate:** `00B_UNSW_NB15_Preformal_Benign_Score_Smoke_Gate.ipynb`
   - Trains one prospectively fixed AE configuration.
   - Computes reconstruction scores only for calibration benign and development benign.
   - Does **not** compute MCC, recall, PR-AUC, ROC-AUC, family recall, or any attack outcome.
   - Gates on calibration fidelity and a broad pre-frozen quantile/exceedance transfer guardrail.
   - **STOP if this smoke gate does not PASS. Do not start formal Notebook 01.**

4. **Notebook 01:** `01_UNSW_NB15_AE_Search_SOURCE_STRATIFIED.ipynb`
   - Fresh formal AE search: 20 unique COMPLETE configurations.
   - Requires the smoke gate to PASS under the same corrected upstream identity.
   - Old AE runs are not counted.

5. **Notebook 02:** `02_UNSW_NB15_DAE_Search_SOURCE_STRATIFIED.ipynb`
   - Fresh formal DAE search: 20 unique COMPLETE configurations.
   - Old partial DAE runs are not counted.
   - Resume-safe for Colab disconnections.

6. **Notebook 03:** `03_UNSW_NB15_Multiseed_Confirmation_SOURCE_STRATIFIED.ipynb`
   - Common seeds 101/202/303.
   - Freezes selected AE and DAE configurations.

7. **Notebook 04:** `04_UNSW_NB15_Matched_Denoising_Ablation_SOURCE_STRATIFIED.ipynb`
   - Matched corruption ablation using seeds 101/202/303.

8. **Notebook 05:** `05_UNSW_NB15_Threshold_Sensitivity_SOURCE_STRATIFIED.ipynb`
   - Development-only threshold sensitivity.
   - Primary 99th-percentile rule remains frozen.

9. **Notebook 06:** `06_UNSW_NB15_Hyperparameter_Sensitivity_SOURCE_STRATIFIED_OPTIMIZED.ipynb`
   - Consolidated AE+DAE post-selection OFAT sensitivity.
   - Uses the optimized/resume-safe implementation.
   - This is robustness analysis, not reselection.

10. **Notebook 07:** `07_UNSW_NB15_Final_Known_Attack_Evaluation_SOURCE_STRATIFIED.ipynb`
    - First authorized final-test model outcomes.
    - Five seeds: 101/202/303/404/505.
    - No post-test tuning.

11. **Notebook 08:** `08_UNSW_NB15_Final_Statistics_Family_Diagnostics_SOURCE_STRATIFIED.ipynb`
    - Paired final statistics, family diagnostics, and practical comparison.

## Important stop rules

- PRE-01 source balance fails → stop; do not run PRE-02.
- PRE-02 fails → stop; do not run the smoke gate.
- Smoke benign-score exchangeability fails → stop; do not run formal Notebook 01.
- Notebook 01 formal search incomplete → do not run Notebook 02.
- Notebook 02 formal search incomplete → do not run Notebook 03.
- Do not use final-test outcomes before Notebook 07.

## What remains authoritative from the previous branch

- Merged master dataset and its SHA-256.
- PRE-00 taxonomy and canonical labels.
- PRE-00 stable row identity.
- PRE-00 raw feature policy.
- PRE-00 feature fingerprints and duplicate audit.
- Global model/search/threshold/metric contracts, provided their frozen hashes verify.

## What is superseded and must not be reused scientifically

- Original PRE-01 partition membership.
- Original PRE-02 fitted preprocessing and transformed matrices.
- Original Notebook 01 AE rankings/results/checkpoints/thresholds.
- Original partial Notebook 02 DAE runs and Optuna study as formal evidence.
- Any downstream result bound to the superseded upstream identity.

Do not delete these old artifacts; retain them for audit only.
