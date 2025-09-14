# Carregamento e preparo do CSV
import pandas as pd

def carregar_dados(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, sep=";")

    # Normalizações
    df["year"]  = df["date"].astype(str).str.slice(0, 4).astype(int)
    df["month"] = df["date"].astype(str).str.slice(5, 7).astype(int)

    region_map = {
        # Norte
        "ACRE": "Norte", "AMAPÁ": "Norte", "AMAZONAS": "Norte", "PARÁ": "Norte",
        "RONDÔNIA": "Norte", "RORAIMA": "Norte", "TOCANTINS": "Norte",
        # Nordeste
        "ALAGOAS": "Nordeste", "BAHIA": "Nordeste", "CEARÁ": "Nordeste", "MARANHÃO": "Nordeste",
        "PARAÍBA": "Nordeste", "PERNAMBUCO": "Nordeste", "PIAUÍ": "Nordeste",
        "RIO GRANDE DO NORTE": "Nordeste", "SERGIPE": "Nordeste",
        # Centro-Oeste
        "DISTRITO FEDERAL": "Centro-Oeste", "GOIÁS": "Centro-Oeste",
        "MATO GROSSO": "Centro-Oeste", "MATO GROSSO DO SUL": "Centro-Oeste",
        # Sudeste
        "ESPÍRITO SANTO": "Sudeste", "MINAS GERAIS": "Sudeste",
        "RIO DE JANEIRO": "Sudeste", "SÃO PAULO": "Sudeste",
        # Sul
        "PARANÁ": "Sul", "RIO GRANDE DO SUL": "Sul", "SANTA CATARINA": "Sul",
    }
    df["regiao"] = df["uf"].map(region_map)

    df["classe_simplificada"] = df["class"].replace({
        "Fogo em áreas de desmatamento consolidado": "Desmatamento consolidado",
        "Fogo em áreas de desmatamento recente": "Desmatamento recente",
        "Fogo em áreas de vegetação nativa": "Vegetação nativa",
    })

    return df
