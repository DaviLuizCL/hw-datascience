# 4 gráficos de dispersão
import matplotlib.pyplot as plt  # importa o módulo de plotagem matplotlib.pyplot
import numpy as np  # importa o módulo numpy para operações numéricas
from services import fig_a4, title, save  # importa funções utilitárias para criar figura A4, adicionar título e salvar imagem
import pandas as pd  # importa pandas para manipulação de dados tabulares

def gerar_dispersoes(df: pd.DataFrame, outdir: str):  # define a função gerar_dispersoes que recebe um DataFrame e um diretório de saída
    mensal = df.groupby(["year", "month"], as_index=False)["focuses"].sum().rename(  # agrupa os dados por ano e mês, soma os focos e renomeia a coluna
        columns={"focuses": "focuses_mensal_brasil"}  # renomeia a coluna 'focuses' para 'focuses_mensal_brasil'
    )
    anual = df.groupby("year", as_index=False)["focuses"].sum().rename(  # agrupa os dados por ano, soma os focos e renomeia a coluna
        columns={"focuses": "focuses_anual_brasil"}  # renomeia a coluna 'focuses' para 'focuses_anual_brasil'
    )


    fig = fig_a4()  # cria uma figura no formato A4 para o primeiro gráfico
    title(fig, "Dispersão 1 — Mês × Total mensal (Brasil)")  # adiciona um título à figura
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])  # adiciona um eixo na figura com posição e tamanho especificados
    ax.scatter(mensal["month"], mensal["focuses_mensal_brasil"], s=10)  # plota um gráfico de dispersão de mês vs total de focos mensais, com tamanho dos pontos 10
    ax.set_xlabel("Mês"); ax.set_ylabel("Total mensal de focos")  # define os rótulos dos eixos x e y
    save(fig, outdir, "disp_1_mes_vs_total_mensal.png")  # salva a figura gerada no diretório de saída com o nome especificado


    fig = fig_a4()  # cria nova figura A4 para o segundo gráfico
    title(fig, "Dispersão 2 — Ano × Total anual (Brasil)")  # adiciona um título à figura
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])  # adiciona um eixo na figura
    ax.scatter(anual["year"], anual["focuses_anual_brasil"], s=12)  # plota um gráfico de dispersão de ano vs total de focos anuais, com tamanho dos pontos 12
    ax.set_xlabel("Ano"); ax.set_ylabel("Total anual de focos")  # define os rótulos dos eixos
    save(fig, outdir, "disp_2_ano_vs_total_anual.png")  # salva a figura no diretório de saída com o nome especificado


    uf_mensal = df.groupby(["uf", "year", "month"], as_index=False)["focuses"].sum()  # agrupa por uf, ano e mês, somando os focos
    aux = uf_mensal.groupby("uf", as_index=False).agg(total=("focuses", "sum"),  # agrupa por uf novamente e calcula o total e a média mensal de focos
                                                      media_mensal=("focuses", "mean"))
    fig = fig_a4()  # cria nova figura A4 para o terceiro gráfico
    title(fig, "Dispersão 3 — Total por UF × Média mensal por UF")  # adiciona título à figura
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])  # adiciona um eixo
    ax.scatter(aux["total"], aux["media_mensal"], s=12)  # plota gráfico de dispersão de total acumulado vs média mensal por UF
    ax.set_xlabel("Total por UF (acumulado)"); ax.set_ylabel("Média mensal por UF")  # define os rótulos dos eixos
    save(fig, outdir, "disp_3_total_uf_vs_media_mensal.png")  # salva a figura no diretório de saída


    pivot = df.pivot_table(index=["year", "month"],  # cria uma tabela dinâmica com índices ano e mês
                           columns="classe_simplificada",  # cria colunas para cada classe simplificada
                           values="focuses",  # usa os valores da coluna focuses
                           aggfunc="sum",  # soma os valores para cada combinação de ano, mês e classe
                           fill_value=0).reset_index()  # substitui valores ausentes por 0 e reseta o índice
    pivot["total"] = pivot.filter(regex="Desmatamento|Vegetação").sum(axis=1)  # cria coluna 'total' com a soma de todas as colunas que contenham 'Desmatamento' ou 'Vegetação'
    pivot["share_nativa"] = pivot.get("Vegetação nativa", 0) / pivot["total"].replace(0, np.nan)  # calcula a participação de vegetação nativa dividindo pela soma total
    pivot["share_desmatamento"] = (  # calcula a participação de desmatamento
        pivot.get("Desmatamento consolidado", 0) + pivot.get("Desmatamento recente", 0)  # soma as duas categorias de desmatamento
    ) / pivot["total"].replace(0, np.nan)  # divide pelo total (substituindo 0 por NaN para evitar divisão por zero)

    m = pivot["share_nativa"].notna() & pivot["share_desmatamento"].notna()  # cria uma máscara booleana para linhas que não têm valores ausentes em ambas as colunas de share
    fig = fig_a4()  # cria nova figura A4 para o quarto gráfico
    title(fig, "Dispersão 4 — Share nativa × Share desmatamento (mensal)")  # adiciona título à figura
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])  # adiciona um eixo à figura
    ax.scatter(pivot.loc[m, "share_nativa"], pivot.loc[m, "share_desmatamento"], s=10)  # plota gráfico de dispersão entre share_nativa e share_desmatamento para linhas válidas
    ax.set_xlabel("Share nativa"); ax.set_ylabel("Share desmatamento")  # define os rótulos dos eixos
    save(fig, outdir, "disp_4_share_nativa_vs_desmatamento.png")  # salva a figura final no diretório de saída
