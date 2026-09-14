"""Génère les visuels (PNG) utilisés dans les docx et le deck : radar de maturité,
Gantt du plan, graphique d'impact business. Sortie : assets/."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

GREEN = "#1DB954"
DARK = "#191414"
GREY = "#8A8A8A"
LIGHT = "#E6E6E6"
ORANGE = "#E8871E"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": GREY,
    "axes.labelcolor": DARK,
    "text.color": DARK,
})

DIMENSIONS = [
    ("Data Governance", 2, 4),
    ("Data Quality", 3, 4),
    ("Data Architecture", 5, 5),
    ("Compliance", 3, 4),
    ("Usage &\nAccessibility", 3, 4),
    ("Data Security", 4, 4),
    ("Data Literacy", 3, 4),
    ("Data Integration", 3, 4),
    ("Analytics & BI", 5, 5),
]


def radar(dark=False):
    labels = [d[0] for d in DIMENSIONS]
    cur = [d[1] for d in DIMENSIONS]
    tgt = [d[2] for d in DIMENSIONS]
    n = len(labels)
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    cur_c, tgt_c, ang_c = cur + cur[:1], tgt + tgt[:1], ang + ang[:1]

    bg = DARK if dark else "white"
    fg = "white" if dark else DARK
    fig = plt.figure(figsize=(7.6, 7.0), facecolor=bg)
    ax = fig.add_subplot(111, polar=True, facecolor=bg)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.plot(ang_c, tgt_c, color=GREEN, lw=2, ls="--", label="Cible M12 — 4,2 / 5")
    ax.fill(ang_c, tgt_c, color=GREEN, alpha=0.12)
    ax.plot(ang_c, cur_c, color=ORANGE, lw=2.5, label="Actuel — 3,4 / 5")
    ax.fill(ang_c, cur_c, color=ORANGE, alpha=0.25)
    for a, c in zip(ang, cur):
        # décalage radial (vers l'intérieur) pour ne pas chevaucher les libellés
        dx, dy = -10 * np.sin(a), -10 * np.cos(a)
        ax.annotate(str(c), (a, c), textcoords="offset points", xytext=(dx, dy),
                    ha="center", va="center", fontsize=10, fontweight="bold", color=ORANGE,
                    bbox=dict(boxstyle="circle,pad=0.15", fc=bg, ec="none"))
    ax.set_xticks(ang)
    ax.set_xticklabels(labels, fontsize=10, color=fg)
    ax.tick_params(axis="x", pad=18)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=8, color=GREY)
    ax.set_ylim(0, 5)
    ax.grid(color=GREY if dark else LIGHT, lw=0.8)
    ax.spines["polar"].set_color(GREY)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.16), ncol=2, frameon=False,
              labelcolor=fg, fontsize=10)
    fig.subplots_adjust(left=0.14, right=0.86, top=0.9, bottom=0.14)
    name = "radar-maturite-dark.png" if dark else "radar-maturite.png"
    fig.savefig(OUT / name, dpi=200, facecolor=bg)
    plt.close(fig)


PHASES = [
    ("Phase 1 — Fondations", 1, 2, "CDO, CoE, stewards, DPO, politique v1.0, OneTrust, audit de l'existant"),
    ("Phase 2 — Pilote User Data", 3, 6, "Périmètre UE · Go/No-Go M6"),
    ("Phase 3 — Généralisation", 7, 12, "Content → Marketing → Payments → Ads"),
    ("Phase 4 — Industrialisation", 13, 18, "Observabilité, lineage, audits complets, politique v2.0"),
]
MILESTONES = [(1, "Nomination CDO"), (6, "Go/No-Go pilote"), (12, "5 domaines gouvernés"), (18, "Mode opérationnel")]


def gantt(dark=False):
    bg = DARK if dark else "white"
    fg = "white" if dark else DARK
    fig, ax = plt.subplots(figsize=(11, 3.7), facecolor=bg)
    ax.set_facecolor(bg)
    shades = [GREEN, "#17A34A", "#138A3E", "#0F6E32"]
    for i, (name, s, e, desc) in enumerate(PHASES):
        y = len(PHASES) - 1 - i
        ax.barh(y, e - s + 1, left=s - 0.5, height=0.5, color=shades[i], edgecolor=bg)
        ax.text(s - 0.5, y + 0.3, name, va="bottom", ha="left", color=fg,
                fontsize=10.5, fontweight="bold")
        ax.text(e + 0.7, y, desc, va="center", ha="left", color=fg, fontsize=9)
    for m, label in MILESTONES:
        x = 0.5 if m == 1 else m + 0.5
        ax.axvline(x, color=ORANGE, lw=1, ls=":")
        ax.text(x, len(PHASES) - 0.2, label, ha="left" if m == 1 else "center",
                va="bottom", fontsize=8.5, color=ORANGE)
    ax.set_xlim(0.5, 18.5 + 9)
    ax.set_ylim(-0.5, len(PHASES) + 0.3)
    ax.set_xticks(range(1, 19))
    ax.set_xticklabels([f"M{m}" for m in range(1, 19)], fontsize=9, color=fg)
    ax.set_yticks([])
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GREY)
    ax.tick_params(axis="x", colors=fg)
    fig.tight_layout()
    name = "gantt-plan-dark.png" if dark else "gantt-plan.png"
    fig.savefig(OUT / name, dpi=200, facecolor=bg)
    plt.close(fig)


def impact(dark=False):
    bg = DARK if dark else "white"
    fg = "white" if dark else DARK
    items = [
        ("Exposition max. GDPR (4 % du CA 2023)", 530, GREY),
        ("Sanction IMY 2023 (déjà payée)", 5, ORANGE),
        ("Coût du programme (18 mois, hyp.)", 6.5, GREEN),
        ("Gain d'efficacité (par an, hyp.)", 3, GREEN),
    ][::-1]
    fig, ax = plt.subplots(figsize=(7.5, 4.0), facecolor=bg)
    ax.set_facecolor(bg)
    ys = range(len(items))
    vals = [v for _, v, _ in items]
    ax.barh(list(ys), vals, color=[c for _, _, c in items], height=0.55)
    ax.set_xscale("log")
    ax.set_xlim(1, 2000)
    for y, v in zip(ys, vals):
        ax.text(v * 1.15, y, f"≈ {v:g} M€".replace(".", ","), va="center", fontsize=11,
                fontweight="bold", color=fg)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([n.replace(" (", "\n(") for n, _, _ in items], fontsize=10, color=fg)
    ax.set_xticks([1, 10, 100, 1000])
    ax.set_xticklabels(["1 M€", "10 M€", "100 M€", "1 000 M€"], fontsize=8.5, color=GREY)
    ax.grid(axis="x", color=GREY if dark else LIGHT, lw=0.6, alpha=0.5)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GREY)
    ax.tick_params(axis="y", length=0)
    fig.suptitle("Le programme coûte ≈ 1 % de l'exposition maximale (échelle logarithmique)", fontsize=11.5,
                 color=fg, x=0.02, ha="left")
    ax.set_xlim(1, 3000)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    name = "impact-business-dark.png" if dark else "impact-business.png"
    fig.savefig(OUT / name, dpi=200, facecolor=bg)
    plt.close(fig)


if __name__ == "__main__":
    for d in (False, True):
        radar(d)
        gantt(d)
        impact(d)
    print("assets générés dans", OUT)
