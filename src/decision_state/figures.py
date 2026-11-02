"""Figures 4.1-4.3, drawn only from the reproduced tables.

Every plotted value is a recomputed count, a path count from the enumeration,
or an exact ratio of counts. I save each figure as a vector PDF (for the
manuscript) and as a 300 dpi PNG (for quick viewing).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

BLUE, ORANGE, AQUA, INK, MUTED = "#2a78d6", "#eb6834", "#1baf7a", "#222222", "#888888"
STATE_COLOUR = {"I": BLUE, "II": ORANGE, "III": AQUA, "IV": MUTED}

plt.rcParams.update({
    "font.family": "serif", "font.size": 8, "pdf.fonttype": 42,
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.6,
    "axes.edgecolor": "#555555", "xtick.color": "#333333", "ytick.color": "#333333",
})


def _save(fig, out_dir: Path, stem: str) -> None:
    fig.tight_layout()
    fig.savefig(out_dir / f"{stem}.pdf", metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(out_dir / f"{stem}.png", dpi=300)
    plt.close(fig)


def figure_4_1(t42: pd.DataFrame, out_dir: Path) -> None:
    """Decision-state plane: Delta FP (x) against Delta TP (y), one panel per dataset with its own scale."""
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8))
    for ax, (dataset, g) in zip(axes, t42.groupby("dataset", sort=False)):
        xr = g.dFP.abs().max() * 1.7
        yr = g.dTP.abs().max() * 1.75
        ax.set_xlim(-xr, xr)
        ax.set_ylim(-yr, yr)
        ax.axhline(0, color=MUTED, lw=0.6)
        ax.axvline(0, color=MUTED, lw=0.6)
        style = dict(color=MUTED, fontsize=7, style="italic")
        ax.text(-xr * 0.95, yr * 0.9, "State I\nDAE dominance", ha="left", va="top", **style)
        ax.text(xr * 0.95, yr * 0.9, "State II\ngenuine trade-off", ha="right", va="top", **style)
        ax.text(xr * 0.95, -yr * 0.9, "State III\nAE dominance", ha="right", va="bottom", **style)
        ax.text(-xr * 0.95, -yr * 0.9, "State IV\ninverse trade-off", ha="left", va="bottom", **style)
        for r in g.itertuples(index=False):
            ax.scatter(r.dFP, r.dTP, s=30, color=STATE_COLOUR[r.state], edgecolor="white", linewidth=1.0, zorder=3)
            ax.annotate(str(r.seed), (r.dFP, r.dTP), xytext=(4, 3), textcoords="offset points", fontsize=7, color=INK)
        ax.set_xlabel(r"$\Delta$FP (DAE $-$ AE)")
        ax.set_ylabel(r"$\Delta$TP (DAE $-$ AE)")
        ax.set_title(dataset, fontsize=8.5, color=INK, loc="left")
        ax.grid(color="#e6e6e6", lw=0.4)
        ax.set_axisbelow(True)
    _save(fig, out_dir, "fig4_1_decision_state_plane")


def figure_4_2(t43: pd.DataFrame, out_dir: Path) -> None:
    """Decision-state composition of the 3,125 enumerated ordered paths per dataset."""
    fig, ax = plt.subplots(figsize=(3.5, 1.75))
    order = ["UNSW-NB15", "CICIDS2017"]
    for yi, dataset in enumerate(order):
        r = t43.set_index("dataset").loc[dataset]
        total = int(r.total_paths)
        left = 0
        for st in ("I", "II", "III", "IV"):
            v = int(r[f"n_{st}"])
            if not v:
                continue
            ax.barh(yi, v, left=left, color=STATE_COLOUR[st], height=0.55, edgecolor="white", linewidth=1.0)
            label = f"State {st}: {v:,} ({100 * v / total:.2f}%)"
            if v > 900:
                ax.text(left + v / 2, yi, label, ha="center", va="center", fontsize=7, color="white")
            else:
                ax.text(left, yi - 0.36, label, ha="left", va="top", fontsize=7, color=INK)
            left += v
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order)
    ax.set_xlim(0, total)
    ax.set_xticks([0, 625, 1250, 1875, 2500, 3125])
    ax.set_xlabel(f"Enumerated ordered paths (of {total:,})")
    ax.set_ylim(-0.85, 1.45)
    _save(fig, out_dir, "fig4_2_path_composition")


def figure_4_3(t44: pd.DataFrame, rho_mean: float, out_dir: Path) -> None:
    """Number of observed UNSW-NB15 seeds favouring the DAE as a step function of rho (log scale)."""
    fig, ax = plt.subplots(figsize=(3.5, 2.2))
    x_min, x_max = 0.1, 1000.0
    rows = list(t44.itertuples(index=False))
    for i, r in enumerate(rows):
        lo = max(r.rho_lower, x_min)
        hi = min(r.rho_upper, x_max)
        ax.hlines(r.DAE_preference_count, lo, hi, color=BLUE, lw=2)
        if i + 1 < len(rows):
            nxt = rows[i + 1]
            ax.vlines(r.rho_upper, nxt.DAE_preference_count, r.DAE_preference_count, color=BLUE, lw=0.8, linestyle=":")
            ax.annotate(f"{r.rho_upper:.3f}", (r.rho_upper, nxt.DAE_preference_count), xytext=(3, -4),
                        textcoords="offset points", fontsize=6.5, color=INK, va="top")
    ax.vlines(rho_mean, 0.6, 5.4, color=INK, lw=0.8, linestyle="--")
    ax.text(rho_mean * 1.1, 5.25, f"ratio of means {rho_mean:.3f}", fontsize=6.5, color=INK, va="center")
    ax.set_xscale("log")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(0.3, 5.5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_xlabel(r"Cost ratio $\rho = C_{\mathrm{FP}}/C_{\mathrm{FN}}$ (log scale)")
    ax.set_ylabel("Observed seeds favouring DAE")
    ax.grid(axis="y", color="#e6e6e6", lw=0.4)
    ax.set_axisbelow(True)
    _save(fig, out_dir, "fig4_3_cost_ratio_staircase")
