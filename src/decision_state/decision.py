"""Decision states, break-even thresholds, path enumeration and the cost-ratio decision map.

Everything in this module is deterministic arithmetic on the seed-level counts
TP and FP. All differences are DAE minus AE, and the cost ratio is always
rho = C_FP / C_FN. I keep exact count ratios as fractions and round only when
writing tables.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

import numpy as np
import pandas as pd

from .constants import DATASETS, SEEDS

STATE_LABELS = {
    "I": "State I - DAE dominance",
    "II": "State II - genuine trade-off",
    "III": "State III - AE dominance",
    "IV": "State IV - inverse trade-off",
    "tie": "Exact tie",
}


def classify_state(d_tp: int, d_fp: int) -> str:
    """Assign the operational decision state of a paired difference (Section 3.6).

    The dominance states admit equality on one count; the trade-off states need
    strictly opposing changes; an exact tie is its own category. No materiality
    tolerance is applied.
    """
    if d_tp == 0 and d_fp == 0:
        return "tie"
    if d_tp >= 0 and d_fp <= 0:
        return "I"
    if d_tp > 0 and d_fp > 0:
        return "II"
    if d_tp <= 0 and d_fp >= 0:
        return "III"
    return "IV"


def seed_counts(seed_metrics: pd.DataFrame, dataset: str) -> pd.DataFrame:
    """Per-seed paired count differences Delta TP_s and Delta FP_s (Equation 4)."""
    g = seed_metrics[seed_metrics.dataset == dataset].set_index(["model", "seed"])
    rows = []
    for s in SEEDS:
        d_tp = int(g.loc[("DAE", s), "TP"] - g.loc[("AE", s), "TP"])
        d_fp = int(g.loc[("DAE", s), "FP"] - g.loc[("AE", s), "FP"])
        rows.append(dict(dataset=dataset, seed=s, dTP=d_tp, dFP=d_fp))
    return pd.DataFrame(rows)


def table_4_2(seed_metrics: pd.DataFrame) -> pd.DataFrame:
    """Table 4.2: seed-level differences, decision states and rho* where defined (State II only)."""
    out = []
    for dataset in DATASETS:
        for rec in seed_counts(seed_metrics, dataset).itertuples(index=False):
            state = classify_state(rec.dTP, rec.dFP)
            rho = Fraction(rec.dTP, rec.dFP) if state == "II" else None
            out.append(dict(dataset=dataset, seed=rec.seed, dTP=rec.dTP, dFP=rec.dFP, state=state,
                            state_label=STATE_LABELS[state],
                            rho_star_exact=str(rho) if rho is not None else "",
                            rho_star=float(rho) if rho is not None else np.nan))
    return pd.DataFrame(out)


def enumerate_paths(counts: pd.DataFrame) -> pd.DataFrame:
    """All 5^5 = 3,125 ordered paths drawn with replacement from the five observed seeds (Section 3.8).

    For each path I sum the seed-level differences and classify the sums. The
    paths are deterministic recombinations of the five observed realisations,
    not new experiments, and I compute no interval or p-value from them.
    """
    lookup = counts.set_index("seed")[["dTP", "dFP"]].to_dict("index")
    rows = []
    for path in itertools.product(SEEDS, repeat=len(SEEDS)):
        d_tp = sum(lookup[s]["dTP"] for s in path)
        d_fp = sum(lookup[s]["dFP"] for s in path)
        rows.append(dict(path=path, dTP_sum=d_tp, dFP_sum=d_fp, state=classify_state(d_tp, d_fp),
                         contains_202=202 in path))
    return pd.DataFrame(rows)


def table_4_3(seed_metrics: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Table 4.3: decision-state composition of the 3,125 enumerated paths, plus the seed-202 breakdown."""
    comp, detail = [], []
    for dataset in DATASETS:
        paths = enumerate_paths(seed_counts(seed_metrics, dataset))
        total = len(paths)
        row = dict(dataset=dataset, total_paths=total)
        for st in ("I", "II", "III", "IV", "tie"):
            n = int((paths.state == st).sum())
            row[f"n_{st}"] = n
            row[f"pct_{st}"] = 100 * n / total
        comp.append(row)
        for contains, g in paths.groupby("contains_202"):
            detail.append(dict(dataset=dataset, contains_seed_202=bool(contains), n_paths=len(g),
                               **{f"n_{st}": int((g.state == st).sum()) for st in ("I", "II", "III", "IV")}))
    return pd.DataFrame(comp), pd.DataFrame(detail)


def ratio_of_means(counts: pd.DataFrame) -> Fraction | None:
    """Aggregate ratio of means rho*_mean = mean(Delta TP) / mean(Delta FP) (Equation 9), if both are positive."""
    m_tp = Fraction(int(counts.dTP.sum()), len(counts))
    m_fp = Fraction(int(counts.dFP.sum()), len(counts))
    return m_tp / m_fp if (m_tp > 0 and m_fp > 0) else None


def preference_at(d_tp: int, d_fp: int, rho: Fraction) -> str:
    """Preferred model at cost ratio rho from Delta L / C_FN = rho * Delta FP - Delta TP (Equation 13)."""
    dl = rho * d_fp - d_tp
    return "DAE" if dl < 0 else ("AE" if dl > 0 else "Tie")


def table_4_4(seed_metrics: pd.DataFrame, dataset: str = "UNSW-NB15") -> pd.DataFrame:
    """Table 4.4: observed-seed decision map over open intervals of rho (Section 3.9).

    The boundaries are the exact seed-specific break-even ratios. Within each
    open interval every seed's preference is constant, so I evaluate it at an
    interior rational point of the interval and never at a boundary.
    """
    counts = seed_counts(seed_metrics, dataset)
    bounds = sorted({Fraction(r.dTP, r.dFP) for r in counts.itertuples()
                     if classify_state(r.dTP, r.dFP) in ("II", "IV")})
    edges = [Fraction(0)] + bounds + [None]
    rows = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        probe = (lo + hi) / 2 if hi is not None else lo + 1
        prefs = {r.seed: preference_at(r.dTP, r.dFP, probe) for r in counts.itertuples()}
        dae = [s for s, p in prefs.items() if p == "DAE"]
        ae = [s for s, p in prefs.items() if p == "AE"]
        tie = [s for s, p in prefs.items() if p == "Tie"]
        rows.append(dict(dataset=dataset,
                         rho_lower_exact=str(lo), rho_upper_exact=str(hi) if hi is not None else "inf",
                         rho_lower=float(lo), rho_upper=float(hi) if hi is not None else np.inf,
                         DAE_preferred_seeds=", ".join(map(str, dae)),
                         AE_preferred_seeds=", ".join(map(str, ae)),
                         tied_seeds=", ".join(map(str, tie)),
                         DAE_preference_count=len(dae), n_seeds=len(prefs)))
    return pd.DataFrame(rows)


def prevalence_rescaled(rho: Fraction, n_benign: int, n_attack: int, pi: Fraction) -> Fraction:
    """Equation 10: rho*(pi) = pi/(1-pi) * N_benign/N_attack * rho*, under the stated transfer assumption.

    This is an arithmetic illustration (Section 5.3), not an observed result.
    """
    return pi / (1 - pi) * Fraction(n_benign, n_attack) * rho
