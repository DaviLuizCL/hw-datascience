
import matplotlib.pyplot as plt
from services import fig_a4, title, save
import pandas as pd

def gerar_pizzas(df: pd.DataFrame, outdir: str):
    y = int(df["year"].max())


    class_y = df[df["year"] == y].groupby("classe_simplificada", as_index=False)["focuses"].sum()
    fig = fig_a4()
    title(fig, f"Pizza 1 — Proporção por classe ({y})")
    ax = fig.add_axes([0.2, 0.25, 0.6, 0.6])
    ax.pie(class_y["focuses"], labels=class_y["classe_simplificada"], autopct="%1.1f%%")
    save(fig, outdir, f"pizza_1_classe_{y}.png")


    reg_y = df[df["year"] == y].groupby("regiao", as_index=False)["focuses"].sum().dropna()
    fig = fig_a4()
    title(fig, f"Pizza 2 — Proporção por região ({y})")
    ax = fig.add_axes([0.2, 0.25, 0.6, 0.6])
    ax.pie(reg_y["focuses"], labels=reg_y["regiao"], autopct="%1.1f%%")
    save(fig, outdir, f"pizza_2_regiao_{y}.png")


    uf_y = df[df["year"] == y].groupby("uf", as_index=False)["focuses"].sum().sort_values("focuses", ascending=False)
    top5 = uf_y.head(5)
    resto = float(uf_y["focuses"].iloc[5:].sum())
    labels = list(top5["uf"]) + ["Outras"]
    values = list(top5["focuses"]) + [resto]
    fig = fig_a4()
    title(fig, f"Pizza 3 — Top 5 UFs vs demais ({y})")
    ax = fig.add_axes([0.2, 0.25, 0.6, 0.6])
    ax.pie(values, labels=labels, autopct="%1.1f%%")
    save(fig, outdir, f"pizza_3_top5_{y}.png")
