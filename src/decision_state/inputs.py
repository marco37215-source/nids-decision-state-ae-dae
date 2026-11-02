"""Locate, authenticate and load the deposited final-test prediction files.

I identify every file by its MD5 checksum against data/input_manifest.csv, not
by its file name, so the analysis does not depend on how the files are named
after download. A file that is not in the manifest is ignored and reported; a
manifest entry without a matching file stops the run.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .constants import (CONFIG_HASHES, N_ROWS, REQUIRED_COLUMNS, SEEDS, DATASETS, MODELS)


def file_digest(path: Path, algorithm: str = "md5", chunk: int = 1 << 20) -> str:
    """Return the hexadecimal digest of a file, read in chunks."""
    h = hashlib.new(algorithm)
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def locate_inputs(data_dir: Path, manifest_path: Path) -> pd.DataFrame:
    """Match the Parquet files under data_dir to the manifest by checksum.

    Returns the manifest with an added 'path' column. Raises if any of the 20
    expected files is missing or if a checksum appears more than once.
    """
    manifest = pd.read_csv(manifest_path)
    found = {}
    unmatched = []
    for path in sorted(Path(data_dir).rglob("*.parquet")):
        md5 = file_digest(path, "md5")
        if md5 in set(manifest["md5"]):
            if md5 in found:
                raise RuntimeError(f"Two files share the checksum {md5}: {found[md5]} and {path}")
            found[md5] = path
        else:
            unmatched.append(path)
    missing = manifest.loc[~manifest["md5"].isin(found), ["dataset", "model", "seed", "md5"]]
    if len(missing):
        raise FileNotFoundError(
            "These deposited files were not found (matched by MD5) under "
            f"{data_dir}:\n{missing.to_string(index=False)}"
        )
    manifest = manifest.copy()
    manifest["path"] = manifest["md5"].map(found)
    manifest["sha256_observed"] = [file_digest(p, "sha256") for p in manifest["path"]]
    if not (manifest["sha256_observed"] == manifest["sha256"]).all():
        raise RuntimeError("An input file matched by MD5 does not match its SHA-256 checksum.")
    for p in unmatched:
        print(f"[inputs] Ignoring {p.name}: its checksum is not in the manifest.")
    return manifest


@dataclass
class Run:
    """One trained model under one seed, evaluated on the final test."""

    dataset: str
    model: str
    seed: int
    row_id: np.ndarray
    y_true: np.ndarray
    error: np.ndarray
    threshold: float
    y_pred: np.ndarray


def load_runs(manifest: pd.DataFrame) -> dict[tuple[str, str, int], Run]:
    """Load the 20 runs, sorted by row_id so that runs of a dataset align row for row."""
    runs = {}
    for rec in manifest.itertuples(index=False):
        df = pd.read_parquet(rec.path, columns=list(REQUIRED_COLUMNS))
        for col, expected in (("model", rec.model), ("seed", rec.seed),
                              ("config_hash", rec.config_hash), ("run_hash", rec.run_hash)):
            values = df[col].unique()
            if len(values) != 1 or values[0] != expected:
                raise ValueError(f"{rec.path.name}: column {col} = {values!r}, expected {expected!r}")
        if CONFIG_HASHES[(rec.dataset, rec.model)] != rec.config_hash:
            raise ValueError(f"{rec.path.name}: configuration hash does not belong to {rec.dataset} {rec.model}")
        thresholds = df["threshold"].unique()
        if len(thresholds) != 1:
            raise ValueError(f"{rec.path.name}: expected one threshold, found {len(thresholds)}")
        df = df.sort_values("row_id", kind="mergesort").reset_index(drop=True)
        runs[(rec.dataset, rec.model, int(rec.seed))] = Run(
            dataset=rec.dataset, model=rec.model, seed=int(rec.seed),
            row_id=df["row_id"].to_numpy(), y_true=df["y_true"].to_numpy().astype(np.int8),
            error=df["reconstruction_error"].to_numpy(dtype=float),
            threshold=float(thresholds[0]), y_pred=df["y_pred"].to_numpy().astype(np.int8),
        )
    return runs


def integrity_report(runs: dict) -> pd.DataFrame:
    """Check the properties that every later calculation relies on.

    For each run I check the population size, that row identifiers are unique,
    that the row identifiers and labels are identical to those of the other runs
    of the same dataset (the paired design), and that the stored prediction
    equals the frozen rule y_hat = 1 if e > T_99 else 0 on every observation.
    """
    rows = []
    for dataset in DATASETS:
        ref = runs[(dataset, "AE", SEEDS[0])]
        for model in MODELS:
            for seed in SEEDS:
                r = runs[(dataset, model, seed)]
                rule = (r.error > r.threshold).astype(np.int8)
                rows.append(dict(
                    dataset=dataset, model=model, seed=seed, n_rows=len(r.row_id),
                    n_rows_expected=N_ROWS[dataset],
                    row_ids_unique=bool(pd.Index(r.row_id).is_unique),
                    same_rows_as_reference=bool(np.array_equal(r.row_id, ref.row_id)),
                    same_labels_as_reference=bool(np.array_equal(r.y_true, ref.y_true)),
                    n_benign=int((r.y_true == 0).sum()), n_attack=int((r.y_true == 1).sum()),
                    threshold_T99=r.threshold,
                    prediction_rule_holds=bool(np.array_equal(rule, r.y_pred)),
                    min_abs_error_minus_threshold=float(np.min(np.abs(r.error - r.threshold))),
                ))
    report = pd.DataFrame(rows)
    checks = ["row_ids_unique", "same_rows_as_reference", "same_labels_as_reference", "prediction_rule_holds"]
    report["all_checks_pass"] = report[checks].all(axis=1) & (report.n_rows == report.n_rows_expected)
    if not report["all_checks_pass"].all():
        raise RuntimeError("Input integrity checks failed:\n" + report.to_string(index=False))
    return report
