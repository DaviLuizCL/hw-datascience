# 3 gráficos de barras
import matplotlib.pyplot as plt
from services import fig_a4, title, save
import pandas as pd

def gerar_barras(df: pd.DataFrame, outdir: str):
    y = int(df["year"].max())
    last_full = y - 1

    top10 = (
        df[df["year"] == last_full]
        .groupby("uf", as_index=False)["focuses"].sum()
        .sort_values("focuses", ascending=False)
        .head(10)
    )
    if top10.empty:
        last_full = y
        top10 = (
            df[df["year"] == last_full]
            .groupby("uf", as_index=False)["focuses"].sum()
            .sort_values("focuses", ascending=False)
            .head(10)
        )

    fig = fig_a4()
    title(fig, f"Barras 1 — Top 10 UFs ({last_full})")
    ax = fig.add_axes([0.12, 0.2, 0.8, 0.7])
    ax.barh(top10["uf"][::-1], top10["focuses"][::-1])
    ax.set_xlabel("Focos"); ax.set_ylabel("UF")
    save(fig, outdir, f"barra_1_top10_ufs_{last_full}.png")


    mensal_y = df[df["year"] == y].groupby("month", as_index=False)["focuses"].sum()
    fig = fig_a4()
    title(fig, f"Barras 2 — Total mensal ({y})")
    ax = fig.add_axes([0.12, 0.2, 0.8, 0.7])
    ax.bar(mensal_y["month"], mensal_y["focuses"])
    ax.set_xlabel("Mês"); ax.set_ylabel("Focos no Brasil")
    save(fig, outdir, f"barra_2_mensal_{y}.png")


    class_y = (
        df[df["year"] == y]
        .groupby("classe_simplificada", as_index=False)["focuses"]
        .sum()
        .sort_values("focuses", ascending=True)
    )
    fig = fig_a4()
    title(fig, f"Barras 3 — Focos por classe ({y})")
    ax = fig.add_axes([0.12, 0.2, 0.8, 0.7])
    ax.barh(class_y["classe_simplificada"], class_y["focuses"])
    ax.set_xlabel("Focos"); ax.set_ylabel("Classe")
    save(fig, outdir, f"barra_3_classe_{y}.png")
