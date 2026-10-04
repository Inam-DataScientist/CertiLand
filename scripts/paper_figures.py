"""Paper figures from logged results only. Usage: python scripts/paper_figures.py"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import yaml  # noqa: E402

R = Path("results")
OUT = Path("paper/figures")
OUT.mkdir(parents=True, exist_ok=True)
STYLE = {  # color + marker + dash: identity never relies on color alone
    "unshielded": dict(color="#c0392b", marker="o", ls="-", label="Unshielded Q-learning"),
    "prob_shield": dict(color="#2e86c1", marker="s", ls="--", label="Probabilistic shield"),
    "sure_shield": dict(color="#1e8449", marker="^", ls="-.", label="Sure shield (ours)"),
}
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.3, "legend.frameon": False})


def wind_sweep():
    dirs = ["wind_0.1", "main", "wind_0.3", "wind_0.4"]
    rows = []
    for d in dirs:
        p = yaml.safe_load((R / d / "config.yaml").read_text())["world"]["wind_prob"]
        rows.append((p, json.loads((R / d / "summary.json").read_text())))
    ps = [r[0] for r in rows]
    fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.6))
    for m, st in STYLE.items():
        tv = [r[1][m]["train_violations"]["mean"] for r in rows]
        ax[0].plot(ps, tv, ms=5, lw=1.6, **st)
        ws = [r[1][m]["P_safe_landing_min_start"]["mean"] for r in rows]
        ax[1].plot(ps, ws, ms=5, lw=1.6, **st)
    ax[0].set_yscale("symlog", linthresh=1)
    ax[0].set_ylim(-0.3, 2e5)
    ax[0].set(xlabel="gust probability $p_w$", ylabel="training violations",
              title="(a) Safety during learning")
    ax[0].annotate("0 for every seed", (0.25, 0), (0.19, 8), fontsize=8, color="#1e8449",
                   arrowprops=dict(arrowstyle="->", color="#1e8449", lw=0.8))
    ax[1].set(xlabel="gust probability $p_w$", ylabel="worst-start $P$(safe landing)",
              title="(b) Worst-case start state", ylim=(0.55, 1.02))
    ax[1].legend(loc="lower left", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "wind_sweep.pdf")


def deadline_and_scale():
    cs = json.loads((R / "case_studies.json").read_text())
    dl = [d for d in cs["deadline"] if d["k"] is not None]
    dl.sort(key=lambda d: d["k"])
    k = [d["k"] for d in dl]
    fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.6))
    ax[0].plot(k, [d["mean_reserve"] for d in dl], color="#2e86c1", marker="o", lw=1.6, label="mean over cells")
    ax[0].plot(k, [d["max_reserve"] for d in dl], color="#c0392b", marker="s", ls="--", lw=1.6, label="worst cell")
    nodl = next(d for d in cs["deadline"] if d["k"] is None)
    ax[0].axhline(nodl["mean_reserve"], color="#7f8c8d", lw=1, ls=":")
    ax[0].text(k[-1], nodl["mean_reserve"] + 0.35, "no deadline (mean)", ha="right", fontsize=7, color="#555")
    ax[0].set(xlabel="landing deadline $k$ in $\\mathbf{G}(low\\rightarrow\\mathbf{F}_{\\leq k} landed)$",
              ylabel="certified battery reserve", title="(a) Specification tightness")
    ax[0].legend(fontsize=8)
    sc = cs["scale"]
    n = [s["product_states"] for s in sc]
    ax[1].plot(n, [s["synth_s"] for s in sc], color="#1e8449", marker="^", lw=1.6, label="shield synthesis")
    ax[1].plot(n, [s["cert_s"] + s["verify_s"] for s in sc], color="#2e86c1", marker="o", ls="--", lw=1.6,
               label="certificate + CTL/PCTL")
    for s in sc:
        ax[1].annotate(f"{s['grid']}$\\times${s['grid']}", (s["product_states"], s["synth_s"]),
                       textcoords="offset points", xytext=(-6, 6), fontsize=7, color="#555")
    ax[1].set(xscale="log", yscale="log", xlabel="product states", ylabel="wall-clock time [s]",
              title="(b) Scalability (single CPU core)")
    ax[1].legend(fontsize=8, loc="center right")
    fig.tight_layout()
    fig.savefig(OUT / "deadline_scale.pdf")


if __name__ == "__main__":
    wind_sweep()
    deadline_and_scale()
    for f in ("training.pdf", "reserve_map.pdf"):
        shutil.copy(R / "main" / f, OUT / f)
    print(sorted(p.name for p in OUT.iterdir()))
