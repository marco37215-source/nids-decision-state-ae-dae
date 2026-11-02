"""Compare the reproduced values with the values printed in the manuscript.

data/manuscript_reported_values.json lists every number of the manuscript that
derives from the deposited predictions, with the place where it is printed and
the precision at which it is printed. A value matches when the reproduced number,
rounded to that precision, equals the printed number. For bounds that the
manuscript states as inequalities (for example 'p < 10^-41') I check the
inequality instead.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def _matches(value, entry) -> bool:
    kind = entry.get("kind", "rounded")
    reported = entry["reported"]
    if kind == "exact":
        return value == reported
    if kind == "less_than":
        return value < reported
    if kind == "at_most":
        return value <= reported
    scale = entry.get("scale", 1)
    decimals = entry["decimals"]
    return round(value * scale, decimals) == round(reported, decimals)


def compare_with_manuscript(computed: dict, reported_path: Path) -> pd.DataFrame:
    entries = json.loads(Path(reported_path).read_text(encoding="utf-8"))["values"]
    rows = []
    for e in entries:
        if e["key"] not in computed:
            rows.append(dict(where=e["where"], key=e["key"], reported=e["reported"], reproduced=None, match=False))
            continue
        value = computed[e["key"]]
        rows.append(dict(where=e["where"], key=e["key"], reported=e["reported"],
                         reproduced=value, kind=e.get("kind", "rounded"), match=bool(_matches(value, e))))
    return pd.DataFrame(rows)
