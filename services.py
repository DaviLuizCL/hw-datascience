
import os
import textwrap
import matplotlib.pyplot as plt

def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path

def save(fig, outdir, name):
    ensure_dir(outdir)
    p = os.path.join(outdir, name)
    fig.savefig(p, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"[ok] {p}")

def fig_a4():

    return plt.figure(figsize=(8.27, 11.69))

def title(fig, t, st=None):
    fig.suptitle(t, fontsize=16, y=0.98)
    if st:
        fig.text(0.5, 0.95, st, ha="center", fontsize=10)

def wrap_text(fig, txt, y=0.9, lh=0.035, size=10, width=110):
    for line in textwrap.wrap(txt, width):
        fig.text(0.08, y, line, ha="left", fontsize=size)
        y -= lh
    return y
