# Carregamento e preparo do CSV
import pandas as pd  # importa a biblioteca pandas para manipulação de dados em tabelas

def carregar_dados(csv_path: str) -> pd.DataFrame:  # define a função carregar_dados que recebe o caminho de um CSV e retorna um DataFrame
    df = pd.read_csv(csv_path, sep=";")  # lê o arquivo CSV usando ponto e vírgula como separador e armazena no DataFrame df

    # Normalizações
    df["year"]  = df["date"].astype(str).str.slice(0, 4).astype(int)  # cria uma coluna 'year' extraindo os 4 primeiros caracteres da coluna 'date'
    df["month"] = df["date"].astype(str).str.slice(5, 7).astype(int)  # cria uma coluna 'month' extraindo os caracteres de posição 5 a 7 da coluna 'date'

    region_map = {  # dicionário que mapeia os nomes dos estados (em maiúsculo) para suas respectivas regiões do Brasil
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
    df["regiao"] = df["uf"].map(region_map)  # cria uma nova coluna 'regiao' mapeando cada UF para sua região correspondente

    df["classe_simplificada"] = df["class"].replace({  # cria uma coluna 'classe_simplificada' renomeando as classes originais para nomes mais curtos
        "Fogo em áreas de desmatamento consolidado": "Desmatamento consolidado",
        "Fogo em áreas de desmatamento recente": "Desmatamento recente",
        "Fogo em áreas de vegetação nativa": "Vegetação nativa",
    })

    return df  # retorna o DataFrame processado
