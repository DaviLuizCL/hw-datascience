# 4 histogramas
import matplotlib.pyplot as plt  # importa o módulo de plotagem matplotlib.pyplot
from services import fig_a4, title, save  # importa funções utilitárias para criar figura A4, adicionar título e salvar imagem
import pandas as pd  # importa pandas para manipulação de dados tabulares

def gerar_histogramas(df: pd.DataFrame, outdir: str):  # define a função gerar_histogramas que recebe um DataFrame e um diretório de saída
    fig = fig_a4()  # cria uma figura no formato A4 para o primeiro histograma
    title(fig, "Histograma 1 — Focos por observação")  # adiciona título à figura
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])  # adiciona um eixo à figura
    ax.hist(df["focuses"], bins=40)  # plota um histograma da coluna focuses com 40 intervalos (bins)
    ax.set_xlabel("Focos"); ax.set_ylabel("Frequência")  # define os rótulos dos eixos x e y
    save(fig, outdir, "hist_1_focos_observacoes.png")  # salva a figura no diretório de saída com o nome especificado

    mensal = df.groupby(["year", "month"], as_index=False)["focuses"].sum()  # agrupa os dados por ano e mês e soma os focos
    fig = fig_a4()  # cria uma nova figura A4 para o segundo histograma
    title(fig, "Histograma 2 — Total mensal (Brasil)")  # adiciona título à figura
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])  # adiciona um eixo
    ax.hist(mensal["focuses"], bins=30)  # plota um histograma com os totais mensais de focos e 30 bins
    ax.set_xlabel("Focos mensais (Brasil)"); ax.set_ylabel("Frequência")  # define os rótulos dos eixos
    save(fig, outdir, "hist_2_total_mensal.png")  # salva a figura no diretório de saída

    uf_total = df.groupby("uf", as_index=False)["focuses"].sum()  # agrupa os dados por UF e soma os focos
    fig = fig_a4()  # cria uma nova figura A4 para o terceiro histograma
    title(fig, "Histograma 3 — Total por UF (acumulado)")  # adiciona título à figura
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])  # adiciona um eixo
    ax.hist(uf_total["focuses"], bins=25)  # plota um histograma do total de focos por UF com 25 bins
    ax.set_xlabel("Focos por UF"); ax.set_ylabel("UFs")  # define os rótulos dos eixos
    save(fig, outdir, "hist_3_total_uf.png")  # salva a figura no diretório de saída

    fig = fig_a4()  # cria uma nova figura A4 para o quarto histograma
    title(fig, "Histograma 4 — Focos por classe (sobrepostos)")  # adiciona título à figura
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])  # adiciona um eixo
    for cls in df["classe_simplificada"].dropna().unique():  # percorre cada classe simplificada existente (não nula)
        ax.hist(df.loc[df["classe_simplificada"] == cls, "focuses"], bins=30, alpha=0.5)  # plota um histograma para os focos dessa classe com transparência 0.5
    ax.set_xlabel("Focos"); ax.set_ylabel("Frequência")  # define os rótulos dos eixos
    save(fig, outdir, "hist_4_classes.png")  # salva a figura no diretório de saída
