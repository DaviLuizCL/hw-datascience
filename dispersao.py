# 4 gráficos de dispersão
import matplotlib.pyplot as plt
import numpy as np
from services import fig_a4, title, save
import pandas as pd

def gerar_dispersoes(df: pd.DataFrame, outdir: str):
    mensal = df.groupby(["year", "month"], as_index=False)["focuses"].sum().rename(
        columns={"focuses": "focuses_mensal_brasil"}
    )
    anual = df.groupby("year", as_index=False)["focuses"].sum().rename(
        columns={"focuses": "focuses_anual_brasil"}
    )


    fig = fig_a4()
    title(fig, "Dispersão 1 — Mês × Total mensal (Brasil)")
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])
    ax.scatter(mensal["month"], mensal["focuses_mensal_brasil"], s=10)
    ax.set_xlabel("Mês"); ax.set_ylabel("Total mensal de focos")
    save(fig, outdir, "disp_1_mes_vs_total_mensal.png")


    fig = fig_a4()
    title(fig, "Dispersão 2 — Ano × Total anual (Brasil)")
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])
    ax.scatter(anual["year"], anual["focuses_anual_brasil"], s=12)
    ax.set_xlabel("Ano"); ax.set_ylabel("Total anual de focos")
    save(fig, outdir, "disp_2_ano_vs_total_anual.png")


    uf_mensal = df.groupby(["uf", "year", "month"], as_index=False)["focuses"].sum()
    aux = uf_mensal.groupby("uf", as_index=False).agg(total=("focuses", "sum"),
                                                      media_mensal=("focuses", "mean"))
    fig = fig_a4()
    title(fig, "Dispersão 3 — Total por UF × Média mensal por UF")
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])
    ax.scatter(aux["total"], aux["media_mensal"], s=12)
    ax.set_xlabel("Total por UF (acumulado)"); ax.set_ylabel("Média mensal por UF")
    save(fig, outdir, "disp_3_total_uf_vs_media_mensal.png")


    pivot = df.pivot_table(index=["year", "month"],
                           columns="classe_simplificada",
                           values="focuses",
                           aggfunc="sum",
                           fill_value=0).reset_index()
    pivot["total"] = pivot.filter(regex="Desmatamento|Vegetação").sum(axis=1)
    pivot["share_nativa"] = pivot.get("Vegetação nativa", 0) / pivot["total"].replace(0, np.nan)
    pivot["share_desmatamento"] = (
        pivot.get("Desmatamento consolidado", 0) + pivot.get("Desmatamento recente", 0)
    ) / pivot["total"].replace(0, np.nan)

    m = pivot["share_nativa"].notna() & pivot["share_desmatamento"].notna()
    fig = fig_a4()
    title(fig, "Dispersão 4 — Share nativa × Share desmatamento (mensal)")
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])
    ax.scatter(pivot.loc[m, "share_nativa"], pivot.loc[m, "share_desmatamento"], s=10)
    ax.set_xlabel("Share nativa"); ax.set_ylabel("Share desmatamento")
    save(fig, outdir, "disp_4_share_nativa_vs_desmatamento.png")
