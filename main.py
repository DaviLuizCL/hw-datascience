#!/usr/bin/env python3
import argparse
import os
from datetime import datetime

from loader import carregar_dados
from histogramas import gerar_histogramas
from dispersao import gerar_dispersoes
from pizza import gerar_pizzas
from barra import gerar_barras
from services import ensure_dir

def main():
    ap = argparse.ArgumentParser(description="Gera TODOS os gráficos a partir de um CSV (p/ montar PDF).")
    ap.add_argument("--path", required=True, help="Caminho para o CSV.")
    ap.add_argument("--outdir", default=None, help="Pasta de saída (default: ./outputs/<timestamp>/)")
    args = ap.parse_args()

    csv_path = args.path
    if not os.path.exists(csv_path):
        raise SystemExit(f"Arquivo não encontrado: {csv_path}")

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    outdir = args.outdir or os.path.join("outputs", ts)
    ensure_dir(outdir)

    print(f"[i] lendo CSV: {csv_path}")
    df = carregar_dados(csv_path)

    print("[i] gerando histogramas...")
    gerar_histogramas(df, outdir)

    print("[i] gerando dispersões...")
    gerar_dispersoes(df, outdir)

    print("[i] gerando pizzas...")
    gerar_pizzas(df, outdir)

    print("[i] gerando barras...")
    gerar_barras(df, outdir)

    print("\nDone!")
    print(f"📂arquivos salvos em: {os.path.abspath(outdir)}")

if __name__ == "__main__":
    main()
