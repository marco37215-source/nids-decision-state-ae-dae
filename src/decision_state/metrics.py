"""Seed-level confusion counts and metrics, recomputed from the observation-level predictions.

I recompute every metric from the stored labels, predictions and reconstruction
errors. Nothing is read from a precomputed metrics file.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import auc, matthews_corrcoef, precision_recall_curve

from .constants import DATASETS, MODELS, SEEDS


def pr_auc_trapezoidal(y_true: np.ndarray, score: np.ndarray) -> float:
    """PR-AUC as used in Experiment 1: the trapezoidal area under the precision-recall curve.

    I use sklearn.metrics.auc(recall, precision) on the points returned by
    precision_recall_curve. This is not the same quantity as average precision,
    which is a step-wise sum; the manuscript reports the trapezoidal area.
    """
    precision, recall, _ = precision_recall_curve(y_true, score)
    return float(auc(recall, precision))


def seed_level_metrics(runs: dict) -> pd.DataFrame:
    """Return one row per dataset, model and seed with counts and metrics."""
    rows = []
    for dataset in DATASETS:
        for model in MODELS:
            for seed in SEEDS:
                r = runs[(dataset, model, seed)]
                y, p = r.y_true, r.y_pred
                tp = int(((p == 1) & (y == 1)).sum())
                fp = int(((p == 1) & (y == 0)).sum())
                fn = int(((p == 0) & (y == 1)).sum())
                tn = int(((p == 0) & (y == 0)).sum())
                recall = tp / (tp + fn)
                precision = tp / (tp + fp)
                fpr = fp / (fp + tn)
                rows.append(dict(
                    dataset=dataset, model=model, seed=seed, TP=tp, FP=fp, FN=fn, TN=tn,
                    N_attack=tp + fn, N_benign=fp + tn,
                    MCC=float(matthews_corrcoef(y, p)),
                    Recall=recall,
                    F1=2 * precision * recall / (precision + recall),
                    Precision=precision,
                    **{"PR-AUC": pr_auc_trapezoidal(y, r.error)},
                    FPR=fpr,
                    FP_per_1000_benign=1000 * fpr,
                    Balanced_Accuracy=(recall + (1 - fpr)) / 2,
                    threshold_T99=r.threshold,
                ))
    return pd.DataFrame(rows)


def table_4_1(seed_metrics: pd.DataFrame) -> pd.DataFrame:
    """Table 4.1: five-seed mean and sample SD of the metrics, and mean confusion counts."""
    out = []
    for (dataset, model), g in seed_metrics.groupby(["dataset", "model"], sort=False):
        row = dict(dataset=dataset, model=model)
        for m in ("MCC", "Recall", "PR-AUC", "FPR"):
            row[f"{m}_mean"] = g[m].mean()
            row[f"{m}_sd"] = g[m].std(ddof=1)
        row["FP_per_1000_benign_mean"] = g["FP_per_1000_benign"].mean()
        for c in ("TP", "FP", "FN"):
            row[f"mean_{c}"] = g[c].mean()
        row["N_benign"] = int(g["N_benign"].iloc[0])
        row["N_attack"] = int(g["N_attack"].iloc[0])
        out.append(row)
    return pd.DataFrame(out)
