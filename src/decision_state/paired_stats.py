"""Paired seed-level statistics (Section 3.11 and Section 4.1 of the manuscript).

The inferential unit is the paired final seed, so n = 5 per dataset. I report
the per-seed differences (DAE minus AE), their mean, median and sample SD, the
direction consistency, the paired standardised effect d_z = mean / SD, a
percentile bootstrap interval and, for comparison, the paired t interval.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from .constants import (BOOTSTRAP_METRIC_ORDER, BOOTSTRAP_RESAMPLES, BOOTSTRAP_SEED,
                        CONFIDENCE_LEVEL, DATASETS, SEEDS)


def paired_differences(seed_metrics: pd.DataFrame, dataset: str) -> pd.DataFrame:
    """Per-seed differences DAE minus AE for every metric and count, indexed by seed."""
    g = seed_metrics[seed_metrics.dataset == dataset].set_index(["model", "seed"])
    cols = [c for c in g.columns if c not in ("dataset",)]
    ae = g.loc["AE"].loc[list(SEEDS), cols]
    dae = g.loc["DAE"].loc[list(SEEDS), cols]
    return dae - ae


def bootstrap_intervals(diffs: pd.DataFrame) -> dict[str, tuple[float, float]]:
    """Percentile bootstrap intervals with the Notebook 08 random stream.

    One numpy Generator, default_rng(2026), is created per dataset and shared by
    the eight metrics in BOOTSTRAP_METRIC_ORDER. For each metric I draw a
    10,000 x 5 matrix of seed indices with replacement, average each row, and
    take the 2.5th and 97.5th percentiles. Because the stream is shared, the
    interval of a metric depends on its position in the order; I therefore keep
    the order fixed even for metrics the manuscript does not report.
    """
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    alpha = (1 - CONFIDENCE_LEVEL) / 2 * 100
    out = {}
    for metric in BOOTSTRAP_METRIC_ORDER:
        d = diffs[metric].to_numpy(dtype=float)
        idx = rng.integers(0, len(d), size=(BOOTSTRAP_RESAMPLES, len(d)))
        means = d[idx].mean(axis=1)
        lo, hi = np.percentile(means, [alpha, 100 - alpha])
        out[metric] = (float(lo), float(hi))
    return out


def paired_summary(seed_metrics: pd.DataFrame) -> pd.DataFrame:
    """Paired effects for both datasets, one row per dataset and metric."""
    rows = []
    for dataset in DATASETS:
        diffs = paired_differences(seed_metrics, dataset)
        boot = bootstrap_intervals(diffs)
        for metric in BOOTSTRAP_METRIC_ORDER:
            d = diffs[metric].to_numpy(dtype=float)
            n = len(d)
            mean, sd = d.mean(), d.std(ddof=1)
            t_crit = stats.t.ppf(1 - (1 - CONFIDENCE_LEVEL) / 2, df=n - 1)
            t_res = stats.ttest_1samp(d, 0.0)
            rows.append(dict(
                dataset=dataset, metric=metric, n_seed_pairs=n,
                mean_difference=mean, median_difference=float(np.median(d)), sd_difference=sd,
                d_z=mean / sd, n_DAE_higher=int((d > 0).sum()), n_AE_higher=int((d < 0).sum()),
                bootstrap_CI_lower=boot[metric][0], bootstrap_CI_upper=boot[metric][1],
                t_CI_lower=mean - t_crit * sd / np.sqrt(n), t_CI_upper=mean + t_crit * sd / np.sqrt(n),
                t_p_value=float(t_res.pvalue),
                all_differences_share_sign=bool((d > 0).all() or (d < 0).all()),
            ))
    return pd.DataFrame(rows)


def minimum_exact_p_value(n: int = 5) -> float:
    """Smallest attainable two-sided exact sign-test p-value with n non-zero differences: 2 x 0.5^n."""
    return 2 * 0.5 ** n
