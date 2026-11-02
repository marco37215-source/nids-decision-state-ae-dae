"""Supplementary McNemar tests (Section 4.5) and reconstruction-score diagnostics (Table 4.5).

Neither analysis enters the decision-state classification. I compute both from
the observation-level predictions, one run or one seed at a time, and I never
pool scores across models or seeds.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import binomtest

from .constants import DATASETS, MODELS, SEEDS


def mcnemar_by_seed(runs: dict) -> pd.DataFrame:
    """Exact McNemar test per dataset and seed: a two-sided binomial test on the discordant observations.

    The net discordance (AE wrong and DAE right, minus AE right and DAE wrong)
    equals Delta TP - Delta FP, so the test speaks only to the equal-cost case
    rho = 1, and it treats the observations of one seed as independent.
    """
    rows = []
    for dataset in DATASETS:
        for s in SEEDS:
            ae, dae = runs[(dataset, "AE", s)], runs[(dataset, "DAE", s)]
            assert np.array_equal(ae.row_id, dae.row_id)
            ae_ok = ae.y_pred == ae.y_true
            dae_ok = dae.y_pred == dae.y_true
            b = int((ae_ok & ~dae_ok).sum())   # AE correct, DAE wrong
            c = int((~ae_ok & dae_ok).sum())   # AE wrong, DAE correct
            res = binomtest(c, b + c, 0.5, alternative="two-sided")
            rows.append(dict(dataset=dataset, seed=s, AE_correct_DAE_wrong=b, AE_wrong_DAE_correct=c,
                             discordant_total=b + c, net_DAE_gain=c - b,
                             exact_two_sided_p_value=float(res.pvalue)))
    return pd.DataFrame(rows)


def score_diagnostics_by_run(runs: dict) -> pd.DataFrame:
    """Equations 15 and 15a for every run, using that run's own T_99 and benign median."""
    rows = []
    for dataset in DATASETS:
        for model in MODELS:
            for s in SEEDS:
                r = runs[(dataset, model, s)]
                attack = r.y_true == 1
                missed = attack & (r.y_pred == 0)
                benign_median = float(np.median(r.error[r.y_true == 0]))
                below = int((r.error[attack] < benign_median).sum())
                rows.append(dict(dataset=dataset, model=model, seed=s,
                                 median_missed_over_T99=float(np.median(r.error[missed] / r.threshold)),
                                 max_missed_over_T99=float(np.max(r.error[missed] / r.threshold)),
                                 benign_median_error=benign_median,
                                 n_attack=int(attack.sum()), n_attack_below_benign_median=below,
                                 P_overlap_pct=100 * below / int(attack.sum())))
    return pd.DataFrame(rows)


def table_4_5(by_run: pd.DataFrame) -> pd.DataFrame:
    """Table 4.5: mean over the five seeds, with the range across seeds."""
    out = []
    for (dataset, model), g in by_run.groupby(["dataset", "model"], sort=False):
        out.append(dict(dataset=dataset, model=model,
                        r_FN_median_mean=g.median_missed_over_T99.mean(),
                        r_FN_median_min=g.median_missed_over_T99.min(),
                        r_FN_median_max=g.median_missed_over_T99.max(),
                        P_overlap_pct_mean=g.P_overlap_pct.mean(),
                        P_overlap_pct_min=g.P_overlap_pct.min(),
                        P_overlap_pct_max=g.P_overlap_pct.max(),
                        max_attacks_below_benign_median_in_any_seed=int(g.n_attack_below_benign_median.max())))
    return pd.DataFrame(out)
