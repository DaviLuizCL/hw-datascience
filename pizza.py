import matplotlib.pyplot as plt          # Biblioteca para criação de gráficos
from services import fig_a4, title, save  # Funções auxiliares do projeto
import pandas as pd                       # Biblioteca para manipulação de dados em tabelas (DataFrames)

def gerar_pizzas(df: pd.DataFrame, outdir: str):
    # Obtém o último ano presente no DataFrame (para focar apenas nele nos gráficos)
    y = int(df["year"].max())


    # --- Pizza 1: Proporção de focos por classe no ano mais recente ---
    # Agrupa os dados do ano mais recente por classe e soma os focos
    class_y = df[df["year"] == y].groupby("classe_simplificada", as_index=False)["focuses"].sum()
    # Cria uma figura no formato A4
    fig = fig_a4()
    # Define o título do gráfico
    title(fig, f"Pizza 1 — Proporção por classe ({y})")
    # Cria os eixos onde o gráfico será desenhado (posição x,y,largura,altura normalizados)
    ax = fig.add_axes([0.2, 0.25, 0.6, 0.6])
    # Gera o gráfico de pizza
    ax.pie(class_y["focuses"], labels=class_y["classe_simplificada"], autopct="%1.1f%%")
    # Salva a figura como arquivo PNG na pasta de saída
    save(fig, outdir, f"pizza_1_classe_{y}.png")


    # --- Pizza 2: Proporção de focos por região no ano mais recente ---
    # Agrupa por região e soma os focos do ano mais recente (removendo valores nulos)
    reg_y = df[df["year"] == y].groupby("regiao", as_index=False)["focuses"].sum().dropna()
    fig = fig_a4()
    title(fig, f"Pizza 2 — Proporção por região ({y})")
    ax = fig.add_axes([0.2, 0.25, 0.6, 0.6])
    ax.pie(reg_y["focuses"], labels=reg_y["regiao"], autopct="%1.1f%%")
    save(fig, outdir, f"pizza_2_regiao_{y}.png")


    # --- Pizza 3: Top 5 UFs com mais focos vs demais ---
    # Agrupa por UF e soma os focos, depois ordena da maior para a menor quantidade
    uf_y = df[df["year"] == y].groupby("uf", as_index=False)["focuses"].sum().sort_values("focuses", ascending=False)
    # Separa as 5 UFs com mais focos
    top5 = uf_y.head(5)
    # Soma os valores das demais UFs
    resto = float(uf_y["focuses"].iloc[5:].sum())
    # Cria lista de rótulos (nomes das UFs + "Outras")
    labels = list(top5["uf"]) + ["Outras"]
    # Cria lista com os valores (focos das top5 + soma das outras)
    values = list(top5["focuses"]) + [resto]
    # Cria a figura e gera o gráfico
    fig = fig_a4()
    title(fig, f"Pizza 3 — Top 5 UFs vs demais ({y})")
    ax = fig.add_axes([0.2, 0.25, 0.6, 0.6])
    ax.pie(values, labels=labels, autopct="%1.1f%%")
    save(fig, outdir, f"pizza_3_top5_{y}.png")
