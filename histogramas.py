# 4 histogramas
import matplotlib.pyplot as plt
from services import fig_a4, title, save
import pandas as pd

def gerar_histogramas(df: pd.DataFrame, outdir: str):
    fig = fig_a4()
    title(fig, "Histograma 1 — Focos por observação")
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])
    ax.hist(df["focuses"], bins=40)
    ax.set_xlabel("Focos"); ax.set_ylabel("Frequência")
    save(fig, outdir, "hist_1_focos_observacoes.png")

    mensal = df.groupby(["year", "month"], as_index=False)["focuses"].sum()
    fig = fig_a4()
    title(fig, "Histograma 2 — Total mensal (Brasil)")
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])
    ax.hist(mensal["focuses"], bins=30)
    ax.set_xlabel("Focos mensais (Brasil)"); ax.set_ylabel("Frequência")
    save(fig, outdir, "hist_2_total_mensal.png")

    uf_total = df.groupby("uf", as_index=False)["focuses"].sum()
    fig = fig_a4()
    title(fig, "Histograma 3 — Total por UF (acumulado)")
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])
    ax.hist(uf_total["focuses"], bins=25)
    ax.set_xlabel("Focos por UF"); ax.set_ylabel("UFs")
    save(fig, outdir, "hist_3_total_uf.png")

    fig = fig_a4()
    title(fig, "Histograma 4 — Focos por classe (sobrepostos)")
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])
    for cls in df["classe_simplificada"].dropna().unique():
        ax.hist(df.loc[df["classe_simplificada"] == cls, "focuses"], bins=30, alpha=0.5)
    ax.set_xlabel("Focos"); ax.set_ylabel("Frequência")
    save(fig, outdir, "hist_4_classes.png")
