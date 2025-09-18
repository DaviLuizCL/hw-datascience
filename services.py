import os                          # Biblioteca para manipulação de caminhos e diretórios
import textwrap                    # Biblioteca para quebrar textos longos em várias linhas
import matplotlib.pyplot as plt    # Biblioteca para criação de gráficos e figuras


# Garante que um diretório existe (e o cria se não existir)
def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)   # Cria a pasta (não dá erro se já existir)
    return path                        # Retorna o caminho criado


# Salva uma figura em um arquivo PNG e fecha a figura
def save(fig, outdir, name):
    ensure_dir(outdir)                                       # Garante que a pasta de saída existe
    p = os.path.join(outdir, name)                            # Cria o caminho completo do arquivo
    fig.savefig(p, bbox_inches="tight", dpi=150)              # Salva a figura com alta resolução
    plt.close(fig)                                            # Fecha a figura para liberar memória
    print(f"[ok] {p}")                                        # Mostra no terminal o caminho salvo


# Cria uma figura no tamanho de uma folha A4 (em polegadas)
def fig_a4():
    return plt.figure(figsize=(8.27, 11.69))                   # Retorna a figura no formato A4


# Adiciona título e subtítulo em uma figura
def title(fig, t, st=None):
    fig.suptitle(t, fontsize=16, y=0.98)                       # Define o título principal (mais acima)
    if st:                                                     # Se existir subtítulo
        fig.text(0.5, 0.95, st, ha="center", fontsize=10)      # Adiciona o subtítulo centralizado


# Escreve um texto longo dentro da figura, quebrando em várias linhas automaticamente
def wrap_text(fig, txt, y=0.9, lh=0.035, size=10, width=110):
    for line in textwrap.wrap(txt, width):                     # Quebra o texto em várias linhas
        fig.text(0.08, y, line, ha="left", fontsize=size)      # Escreve cada linha na figura
        y -= lh                                                # Ajusta a posição vertical para a próxima linha
    return y                                                   # Retorna a última posição Y usada
