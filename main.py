#!/usr/bin/env python3
# Shebang: permite executar este script diretamente no terminal (Linux/Mac),
# usando o interpretador python3 do sistema.

import argparse  # Biblioteca para criar e tratar argumentos de linha de comando
import os        # Biblioteca para manipulação de caminhos e arquivos
from datetime import datetime  # Para gerar timestamps (data/hora atuais)

# Importa funções personalizadas do projeto
from loader import carregar_dados         # Função para ler e preparar os dados do CSV
from histogramas import gerar_histogramas # Função que gera gráficos de histograma
from dispersao import gerar_dispersoes    # Função que gera gráficos de dispersão
from pizza import gerar_pizzas            # Função que gera gráficos de pizza
from barra import gerar_barras             # Função que gera gráficos de barras
from services import ensure_dir            # Função auxiliar que garante a existência de uma pasta

def main():
    # Cria o parser de argumentos para linha de comando
    ap = argparse.ArgumentParser(
        description="Gera TODOS os gráficos a partir de um CSV (p/ montar PDF)."
    )
    # Adiciona argumento obrigatório --path (caminho para o CSV de entrada)
    ap.add_argument("--path", required=True, help="Caminho para o CSV.")
    # Adiciona argumento opcional --outdir (pasta de saída dos gráficos)
    ap.add_argument("--outdir", default=None, help="Pasta de saída (default: ./outputs/<timestamp>/)")
    
    # Faz o parsing dos argumentos passados pelo usuário no terminal
    args = ap.parse_args()

    # Salva o caminho do CSV em uma variável
    csv_path = args.path
    # Verifica se o arquivo realmente existe
    if not os.path.exists(csv_path):
        # Encerra o programa com erro se não existir
        raise SystemExit(f"Arquivo não encontrado: {csv_path}")

    # Gera um timestamp no formato AAAAMMDD-HHMMSS para nomear a pasta de saída
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    # Se o usuário não especificou a pasta de saída, cria uma nova em ./outputs/<timestamp>
    outdir = args.outdir or os.path.join("outputs", ts)
    # Cria a pasta (se não existir)
    ensure_dir(outdir)

    # Informa que vai ler o CSV
    print(f"[i] lendo CSV: {csv_path}")
    # Carrega e prepara os dados do CSV
    df = carregar_dados(csv_path)

    # Gera gráficos do tipo histograma
    print("[i] gerando histogramas...")
    gerar_histogramas(df, outdir)

    # Gera gráficos do tipo dispersão
    print("[i] gerando dispersões...")
    gerar_dispersoes(df, outdir)

    # Gera gráficos do tipo pizza
    print("[i] gerando pizzas...")
    gerar_pizzas(df, outdir)

    # Gera gráficos do tipo barras
    print("[i] gerando barras...")
    gerar_barras(df, outdir)

    # Mensagem final informando conclusão e pasta de saída
    print("\nDone!")
    print(f"📂arquivos salvos em: {os.path.abspath(outdir)}")

# Ponto de entrada: se o arquivo for executado diretamente, chama a função main()
if __name__ == "__main__":
    main()
