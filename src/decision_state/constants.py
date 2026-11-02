"""Fixed constants of the frozen Experiment 1 v2 final evaluation.

I keep every constant that the analysis depends on in this one module, so that a
reader can see at a glance which settings were fixed before the analysis began.
None of these values is tuned by the code.
"""

from pathlib import Path

# The five common final seeds. AE_s and DAE_s share seed s and were evaluated on
# the same final-test observations, which makes each seed a paired realisation.
SEEDS = (101, 202, 303, 404, 505)

DATASETS = ("CICIDS2017", "UNSW-NB15")
MODELS = ("AE", "DAE")

# Configuration hashes of the four selected models (Notebook 03 selected-model
# manifests). I use them only to check that each prediction file belongs to the
# model it claims to belong to.
CONFIG_HASHES = {
    ("CICIDS2017", "AE"): "b86121d82bf5f2c18336369fc4043727cc5a19985dc9e98848d1016998f44d3a",
    ("CICIDS2017", "DAE"): "16838232aebb6211bb93d1c698985b35164410bd4d081ddb5d23ce011b70a536",
    ("UNSW-NB15", "AE"): "f2ff449180ad3503c1da18b58b04dd4f84991ae3babf6994f4c07bc0c40122db",
    ("UNSW-NB15", "DAE"): "efc7b06f35beb5ad266889160fe77a2ebab33277817995889846dfd0512431e9",
}
DATASET_OF_CONFIG = {h: d for (d, _m), h in CONFIG_HASHES.items()}

# Final-test population sizes. I check them against the files rather than trust them.
N_ROWS = {"CICIDS2017": 668_562, "UNSW-NB15": 525_584}

# Columns that each deposited Parquet file must contain.
REQUIRED_COLUMNS = (
    "row_id", "y_true", "reconstruction_error", "threshold", "y_pred",
    "model", "seed", "config_hash", "run_hash", "attack_family",
)

# Paired seed bootstrap, exactly as executed in Notebook 08: 10,000 resamples of
# the five paired seed differences, a single numpy.random.default_rng(2026)
# stream per dataset, shared across the metrics in the order below, and
# percentile limits from numpy.percentile (linear interpolation).
BOOTSTRAP_RESAMPLES = 10_000
BOOTSTRAP_SEED = 2026
BOOTSTRAP_METRIC_ORDER = (
    "MCC", "Recall", "F1", "Precision", "PR-AUC", "FPR",
    "FP_per_1000_benign", "Balanced_Accuracy",
)
CONFIDENCE_LEVEL = 0.95

# Default locations, relative to the repository root.
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = REPO_ROOT / "data" / "raw"
DEFAULT_MANIFEST = REPO_ROOT / "data" / "input_manifest.csv"
DEFAULT_RESULTS_DIR = REPO_ROOT / "results"
REPORTED_VALUES = REPO_ROOT / "data" / "manuscript_reported_values.json"
