"""Reproduce every result, table and figure of Manuscript 2 that derives from the deposited predictions.

Run from the repository root:

    python scripts/reproduce_all.py --data-dir data/raw

The script (1) authenticates the 20 Parquet files by checksum, (2) checks the
paired design and the frozen prediction rule, (3) recomputes all seed-level
counts and metrics, (4) runs the paired statistics, the decision-state analysis,
the path enumeration, the decision map, the McNemar tests and the score
diagnostics, (5) draws the three figures, and (6) compares every number with the
value printed in the manuscript. It stops with an error if any comparison fails.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from decision_state import constants as C  # noqa: E402
from decision_state import decision, diagnostics, figures, inputs, metrics, paired_stats  # noqa: E402
from decision_state.check import compare_with_manuscript  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data-dir", type=Path, default=C.DEFAULT_DATA_DIR,
                        help="Folder that contains the 20 Parquet files downloaded from Zenodo (searched recursively).")
    parser.add_argument("--out-dir", type=Path, default=C.DEFAULT_RESULTS_DIR, help="Output folder.")
    parser.add_argument("--manifest", type=Path, default=C.DEFAULT_MANIFEST)
    args = parser.parse_args()

    tables = args.out_dir / "tables"
    figs = args.out_dir / "figures"
    tables.mkdir(parents=True, exist_ok=True)
    figs.mkdir(parents=True, exist_ok=True)

    # 1-2. Authenticate and load the inputs, then check the paired design.
    print("[1/6] Locating and authenticating the input files ...")
    manifest = inputs.locate_inputs(args.data_dir, args.manifest)
    runs = inputs.load_runs(manifest)
    print("[2/6] Checking the paired design and the prediction rule ...")
    integrity = inputs.integrity_report(runs)
    integrity.to_csv(tables / "input_integrity_checks.csv", index=False)

    # 3. Seed-level metrics and Table 4.1.
    print("[3/6] Recomputing seed-level counts and metrics ...")
    sm = metrics.seed_level_metrics(runs)
    sm.to_csv(tables / "seed_level_metrics.csv", index=False)
    t41 = metrics.table_4_1(sm)
    t41.to_csv(tables / "table_4_1_five_seed_performance.csv", index=False)
    effects = paired_stats.paired_summary(sm)
    effects.to_csv(tables / "paired_seed_effects.csv", index=False)

    # 4. Decision analysis.
    print("[4/6] Classifying decision states, enumerating paths and building the decision map ...")
    t42 = decision.table_4_2(sm)
    t42.to_csv(tables / "table_4_2_seed_decision_states.csv", index=False)
    t43, t43_detail = decision.table_4_3(sm)
    t43.to_csv(tables / "table_4_3_path_composition.csv", index=False)
    t43_detail.to_csv(tables / "path_composition_by_seed_202.csv", index=False)
    t44 = decision.table_4_4(sm, "UNSW-NB15")
    t44.to_csv(tables / "table_4_4_decision_map_unsw_nb15.csv", index=False)

    unsw_counts = decision.seed_counts(sm, "UNSW-NB15")
    cic_counts = decision.seed_counts(sm, "CICIDS2017")
    rho_mean = decision.ratio_of_means(unsw_counts)
    trade = t42[(t42.dataset == "UNSW-NB15") & (t42.state == "II")].sort_values("rho_star")
    n_b = int(t41.set_index("dataset").loc["UNSW-NB15", "N_benign"].iloc[0])
    n_a = int(t41.set_index("dataset").loc["UNSW-NB15", "N_attack"].iloc[0])
    pi = Fraction(1, 100)
    rescaled = [dict(quantity=f"seed {r.seed}", rho_star=r.rho_star,
                     rho_star_at_pi_0_01=float(decision.prevalence_rescaled(Fraction(r.rho_star_exact), n_b, n_a, pi)))
                for r in trade.itertuples(index=False)]
    rho_mean_pi = decision.prevalence_rescaled(rho_mean, n_b, n_a, pi)
    rescaled.append(dict(quantity="ratio of means", rho_star=float(rho_mean), rho_star_at_pi_0_01=float(rho_mean_pi)))
    pd.DataFrame(rescaled).to_csv(tables / "prevalence_rescaling_illustration_unsw_nb15.csv", index=False)

    # 5. Supplementary tests and diagnostics.
    print("[5/6] Running the McNemar tests and the score diagnostics ...")
    mcn = diagnostics.mcnemar_by_seed(runs)
    mcn.to_csv(tables / "mcnemar_by_seed.csv", index=False)
    diag_runs = diagnostics.score_diagnostics_by_run(runs)
    diag_runs.to_csv(tables / "score_diagnostics_by_run.csv", index=False)
    t45 = diagnostics.table_4_5(diag_runs)
    t45.to_csv(tables / "table_4_5_score_diagnostics.csv", index=False)

    figures.figure_4_1(t42, figs)
    figures.figure_4_2(t43, figs)
    figures.figure_4_3(t44, float(rho_mean), figs)

    # 6. Collect every number the manuscript prints and compare.
    print("[6/6] Comparing the reproduced values with the manuscript ...")
    computed = collect_values(sm, t41, effects, t42, t43, t43_detail, t44, unsw_counts, cic_counts,
                              rho_mean, rho_mean_pi, rescaled, mcn, t45, diag_runs, integrity, n_b, n_a)
    with open(args.out_dir / "computed_values.json", "w") as fh:
        json.dump(computed, fh, indent=2, sort_keys=True)
    with open(args.out_dir / "run_environment.json", "w") as fh:
        json.dump(environment_record(manifest), fh, indent=2)

    report = compare_with_manuscript(computed, C.REPORTED_VALUES)
    report.to_csv(args.out_dir / "manuscript_comparison.csv", index=False)
    n_fail = int((~report["match"]).sum())
    print(f"\n{len(report) - n_fail} of {len(report)} manuscript values reproduced.")
    if n_fail:
        print(report[~report["match"]].to_string(index=False))
        return 1
    print("All values printed in the manuscript that derive from the deposited predictions were reproduced.")
    return 0


def collect_values(sm, t41, effects, t42, t43, t43_detail, t44, unsw_counts, cic_counts,
                   rho_mean, rho_mean_pi, rescaled, mcn, t45, diag_runs, integrity, n_b, n_a) -> dict:
    """Flatten the reproduced quantities into named values that data/manuscript_reported_values.json refers to."""
    v: dict[str, float | int | str] = {}
    for ds in C.DATASETS:
        k = "cic" if ds == "CICIDS2017" else "unsw"
        ig = integrity[integrity.dataset == ds].iloc[0]
        v[f"{k}.n_rows"] = int(ig.n_rows)
        v[f"{k}.n_benign"] = int(ig.n_benign)
        v[f"{k}.n_attack"] = int(ig.n_attack)
        v[f"{k}.attack_prevalence"] = ig.n_attack / ig.n_rows
        for r in t41[t41.dataset == ds].to_dict("records"):
            m = r["model"].lower()
            for col in ("MCC_mean", "MCC_sd", "Recall_mean", "Recall_sd", "PR-AUC_mean", "PR-AUC_sd",
                        "FPR_mean", "FPR_sd", "FP_per_1000_benign_mean", "mean_TP", "mean_FP", "mean_FN"):
                v[f"{k}.{m}.{col}"] = float(r[col])
        for r in effects[effects.dataset == ds].itertuples(index=False):
            p = f"{k}.diff.{r.metric}"
            v[f"{p}.mean"] = r.mean_difference
            v[f"{p}.d_z"] = r.d_z
            v[f"{p}.boot_lo"] = r.bootstrap_CI_lower
            v[f"{p}.boot_hi"] = r.bootstrap_CI_upper
            v[f"{p}.t_lo"] = r.t_CI_lower
            v[f"{p}.t_hi"] = r.t_CI_upper
            v[f"{p}.t_p"] = r.t_p_value
            v[f"{p}.n_DAE_higher"] = r.n_DAE_higher
        counts = cic_counts if ds == "CICIDS2017" else unsw_counts
        v[f"{k}.mean_dTP"] = counts.dTP.mean()
        v[f"{k}.mean_dFP"] = counts.dFP.mean()
        for r in t42[t42.dataset == ds].itertuples(index=False):
            v[f"{k}.seed{r.seed}.dTP"] = r.dTP
            v[f"{k}.seed{r.seed}.dFP"] = r.dFP
            v[f"{k}.seed{r.seed}.state"] = r.state
            if r.state == "II":
                v[f"{k}.seed{r.seed}.rho_star"] = r.rho_star
        row = t43.set_index("dataset").loc[ds]
        for st in ("I", "II", "III", "IV"):
            v[f"{k}.paths.n_{st}"] = int(row[f"n_{st}"])
            v[f"{k}.paths.pct_{st}"] = float(row[f"pct_{st}"])
        v[f"{k}.paths.total"] = int(row.total_paths)
        no202 = t43_detail[(t43_detail.dataset == ds) & (~t43_detail.contains_seed_202)].iloc[0]
        with202 = t43_detail[(t43_detail.dataset == ds) & (t43_detail.contains_seed_202)].iloc[0]
        v[f"{k}.paths.without_202.n"] = int(no202.n_paths)
        v[f"{k}.paths.without_202.n_II"] = int(no202.n_II)
        v[f"{k}.paths.with_202.n_I"] = int(with202.n_I)
        for r in mcn[mcn.dataset == ds].itertuples(index=False):
            v[f"{k}.mcnemar.seed{r.seed}.net_DAE_gain"] = r.net_DAE_gain
            v[f"{k}.mcnemar.seed{r.seed}.p"] = r.exact_two_sided_p_value
        for r in t45[t45.dataset == ds].itertuples(index=False):
            m = r.model.lower()
            for col in ("r_FN_median_mean", "r_FN_median_min", "r_FN_median_max",
                        "P_overlap_pct_mean", "P_overlap_pct_min", "P_overlap_pct_max",
                        "max_attacks_below_benign_median_in_any_seed"):
                v[f"{k}.{m}.{col}"] = float(getattr(r, col))
    # Paired differences of PR-AUC by seed (which seeds favour the DAE).
    d = paired_stats.paired_differences(sm, "UNSW-NB15")["PR-AUC"]
    v["unsw.diff.PR-AUC.seeds_DAE_higher"] = ", ".join(str(s) for s in d.index if d[s] > 0)
    # Break-even thresholds and derived text quantities (UNSW-NB15).
    finite = sorted(v[f"unsw.seed{s}.rho_star"] for s in C.SEEDS if f"unsw.seed{s}.rho_star" in v)
    v["unsw.rho_star.min"] = finite[0]
    v["unsw.rho_star.max"] = finite[-1]
    v["unsw.rho_star.fold_range"] = finite[-1] / finite[0]
    v["unsw.rho_mean"] = float(rho_mean)
    v["unsw.rho_mean_at_pi_0_01"] = float(rho_mean_pi)
    v["unsw.inverse_rho_mean_at_pi_0_01"] = float(1 / rho_mean_pi)
    for r in rescaled:
        if r["quantity"].startswith("seed"):
            v[f"unsw.{r['quantity'].replace(' ', '')}.rho_star_at_pi_0_01"] = r["rho_star_at_pi_0_01"]
    v["unsw.seed202.dFP_pct_points_of_FPR"] = 100 * abs(v["unsw.seed202.dFP"]) / n_b
    v["unsw.seed505.dFP_pct_points_of_FPR"] = 100 * abs(v["unsw.seed505.dFP"]) / n_b
    v["unsw.mean_dFP_per_1000_benign"] = 1000 * v["unsw.mean_dFP"] / n_b
    v["cic.mean_dFP_per_1000_benign"] = 1000 * v["cic.mean_dFP"] / v["cic.n_benign"]
    for r in t44.itertuples(index=False):
        v[f"unsw.map.{r.rho_lower:.3f}_{r.rho_upper:.3f}.DAE_count"] = r.DAE_preference_count
        v[f"unsw.map.{r.rho_lower:.3f}_{r.rho_upper:.3f}.DAE_seeds"] = r.DAE_preferred_seeds
    v["min_exact_p_value_n5"] = paired_stats.minimum_exact_p_value(5)
    return v


def environment_record(manifest: pd.DataFrame) -> dict:
    import matplotlib
    import scipy
    import sklearn
    return dict(python=platform.python_version(), platform=platform.platform(), numpy=np.__version__,
                pandas=pd.__version__, scipy=scipy.__version__, scikit_learn=sklearn.__version__,
                matplotlib=matplotlib.__version__,
                inputs=[dict(dataset=r.dataset, model=r.model, seed=int(r.seed), md5=r.md5)
                        for r in manifest.itertuples(index=False)])


if __name__ == "__main__":
    sys.exit(main())
