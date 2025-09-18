# 3 gráficos de barras
import matplotlib.pyplot as plt  # importa o módulo de plotagem matplotlib.pyplot comumente apelidado de plt
from services import fig_a4, title, save  # importa funções utilitárias (criar figura A4, adicionar título e salvar) do módulo services
import pandas as pd  # importa pandas e o apelida como pd

def gerar_barras(df: pd.DataFrame, outdir: str):  # define a função gerar_barras que recebe um DataFrame e um diretório de saída
    y = int(df["year"].max())  # obtém o maior ano presente no DataFrame e converte para inteiro (ano mais recente presente nos dados)
    last_full = y - 1  # assume que o ano completo anterior é o ano mais recente menos 1 (último ano completo)

    top10 = (  # calcula o top 10 de UFs por soma de 'focuses' no ano last_full
        df[df["year"] == last_full]  # filtra o DataFrame para o ano last_full
        .groupby("uf", as_index=False)["focuses"].sum()  # agrupa por 'uf' e soma a coluna 'focuses', mantendo 'uf' como coluna
        .sort_values("focuses", ascending=False)  # ordena dos maiores para os menores focos
        .head(10)  # pega os 10 primeiros (top 10)
    )
    if top10.empty:  # verifica se o resultado do top10 está vazio (por exemplo, se não há dados para last_full)
        last_full = y  # se estiver vazio, usa o ano mais recente presente nos dados (y)
        top10 = (  # recalcula o top10 usando o ano y
            df[df["year"] == last_full]  # filtra para o ano atualizado (y)
            .groupby("uf", as_index=False)["focuses"].sum()  # agrupa por 'uf' e soma 'focuses'
            .sort_values("focuses", ascending=False)  # ordena em ordem decrescente de focos
            .head(10)  # seleciona os 10 primeiros
        )

    fig = fig_a4()  # cria uma figura no formato A4 usando a função utilitária fig_a4
    title(fig, f"Barras 1 — Top 10 UFs ({last_full})")  # adiciona título à figura informando o ano usado (last_full)
    ax = fig.add_axes([0.12, 0.2, 0.8, 0.7])  # adiciona um eixo à figura com posição e dimensões especificadas (left, bottom, width, height)
    ax.barh(top10["uf"][::-1], top10["focuses"][::-1])  # plota um gráfico de barras horizontal; [::-1] inverte as séries para ordenar visualmente do maior ao menor
    ax.set_xlabel("Focos"); ax.set_ylabel("UF")  # define o rótulo do eixo x como "Focos" e do eixo y como "UF"
    save(fig, outdir, f"barra_1_top10_ufs_{last_full}.png")  # salva a figura no diretório outdir com nome que inclui o ano last_full


    mensal_y = df[df["year"] == y].groupby("month", as_index=False)["focuses"].sum()  # agrupa os dados do ano y por mês somando 'focuses' para obter totais mensais
    fig = fig_a4()  # cria nova figura A4 para o segundo gráfico
    title(fig, f"Barras 2 — Total mensal ({y})")  # adiciona título que indica que é o total mensal do ano y
    ax = fig.add_axes([0.12, 0.2, 0.8, 0.7])  # adiciona eixo com as mesmas proporções usadas anteriormente
    ax.bar(mensal_y["month"], mensal_y["focuses"])  # plota um gráfico de barras vertical com meses no eixo x e focos no eixo y
    ax.set_xlabel("Mês"); ax.set_ylabel("Focos no Brasil")  # define rótulos dos eixos para o gráfico mensal
    save(fig, outdir, f"barra_2_mensal_{y}.png")  # salva a figura mensal no diretório outdir com nome que inclui o ano y


    class_y = (  # calcula a soma de 'focuses' por classe simplificada para o ano y
        df[df["year"] == y]  # filtra o DataFrame para o ano y
        .groupby("classe_simplificada", as_index=False)["focuses"]  # agrupa por 'classe_simplificada' e seleciona a coluna 'focuses'
        .sum()  # soma os valores de 'focuses' por classe
        .sort_values("focuses", ascending=True)  # ordena as classes em ordem crescente de focos (útil para barh visual)
    )
    fig = fig_a4()  # cria nova figura A4 para o terceiro gráfico
    title(fig, f"Barras 3 — Focos por classe ({y})")  # adiciona título indicando que mostra focos por classe no ano y
    ax = fig.add_axes([0.12, 0.2, 0.8, 0.7])  # adiciona eixo à figura com posição e tamanho definidos
    ax.barh(class_y["classe_simplificada"], class_y["focuses"])  # plota um gráfico de barras horizontal com classes no eixo y e focos no eixo x
    ax.set_xlabel("Focos"); ax.set_ylabel("Classe")  # define os rótulos dos eixos para o gráfico por classe
    save(fig, outdir, f"barra_3_classe_{y}.png")  # salva a figura final no diretório outdir com nome que inclui o ano y
